# Data Processing

The `winiutils.src.data` package provides utilities for data manipulation,
including a comprehensive DataFrame cleaning pipeline
and data structure helpers.

---

## DataFrame Cleaning Pipeline

**Module:** `winiutils.src.data.dataframe.cleaning`

The `CleaningDF` abstract base class provides an extensible framework
for cleaning and standardizing Polars DataFrames.

### Pipeline Stages

The cleaning pipeline executes in the following order:

1. **Column Renaming** — Standardize column names from raw input
2. **Column Dropping** — Remove columns not in schema
3. **Null Filling** — Fill null values with configurable defaults
4. **Type Conversion**
    — Convert to correct data types with custom transformations
5. **Null Subset Dropping**
    — Remove rows where specified column groups are all null
6. **Duplicate Handling** — Aggregate duplicate rows and sum specified columns
7. **Sorting** — Multi-column sorting with per-column direction control
8. **Validation** — Enforce data quality (correct dtypes, no nulls, no NaN)

### Abstract Methods

Subclasses must implement these methods to configure the cleaning behavior:

| Method | Return Type | Description |
|--------|-------------|-------------|
| `get_rename_map()` | `dict[str, str]` | Map standardized names to raw input names |
| `get_col_dtype_map()` | `dict[str, type[pl.DataType]]` | Define expected data types |
| `get_fill_null_map()` | `dict[str, Any]` | Default values for null filling |
| `get_col_converter_map()` | `dict[str, Callable]` | Custom column transformations |
| `get_drop_null_subsets()` | `tuple[tuple[str, ...], ...]` | Column subsets for null row deletion |
| `get_unique_subsets()` | `tuple[tuple[str, ...], ...]` | Duplicate detection criteria |
| `get_add_on_duplicate_cols()` | `tuple[str, ...]` | Columns to sum on duplicates |
| `get_sort_cols()` | `tuple[tuple[str, bool], ...]` | Sort order (column, descending) |
| `get_no_null_cols()` | `tuple[str, ...]` | Required non-null columns |
| `get_col_precision_map()` | `dict[str, int]` | Float rounding precision |

### Usage Example

```python
from winiutils.src.data.dataframe.cleaning import CleaningDF
import polars as pl
from typing import Any
from collections.abc import Callable

class UserDataCleaner(CleaningDF):
    """Clean and standardize user data."""

    # Define column constants for reusability
    USER_ID = "user_id"
    EMAIL = "email"
    SCORE = "score"
    ACTIVE = "active"

    @classmethod
    def get_rename_map(cls) -> dict[str, str]:
        return {
            cls.USER_ID: "UserId",
            cls.EMAIL: "Email_Address",
            cls.SCORE: "UserScore",
            cls.ACTIVE: "IsActive",
        }

    @classmethod
    def get_col_dtype_map(cls) -> dict[str, type[pl.DataType]]:
        return {
            cls.USER_ID: pl.Int64,
            cls.EMAIL: pl.Utf8,
            cls.SCORE: pl.Float64,
            cls.ACTIVE: pl.Boolean,
        }

    @classmethod
    def get_fill_null_map(cls) -> dict[str, Any]:
        return {
            cls.USER_ID: 0,
            cls.EMAIL: "",
            cls.SCORE: 0.0,
            cls.ACTIVE: False,
        }

    @classmethod
    def get_col_converter_map(
        cls
    ) -> dict[str, Callable[[pl.Series], pl.Series]]:
        return {
            cls.USER_ID: cls.skip_col_converter,
            cls.EMAIL: lambda s: s.str.to_lowercase(),
            cls.SCORE: cls.skip_col_converter,
            cls.ACTIVE: cls.skip_col_converter,
        }

    @classmethod
    def get_drop_null_subsets(cls) -> tuple[tuple[str, ...], ...]:
        return ((cls.USER_ID,),)

    @classmethod
    def get_unique_subsets(cls) -> tuple[tuple[str, ...], ...]:
        return ((cls.USER_ID,),)

    @classmethod
    def get_add_on_duplicate_cols(cls) -> tuple[str, ...]:
        return (cls.SCORE,)

    @classmethod
    def get_sort_cols(cls) -> tuple[tuple[str, bool], ...]:
        return ((cls.USER_ID, False),)

    @classmethod
    def get_no_null_cols(cls) -> tuple[str, ...]:
        return (cls.USER_ID,)

    @classmethod
    def get_col_precision_map(cls) -> dict[str, int]:
        return {cls.SCORE: 2}


# Usage
raw_data = {
    "UserId": [1, 2, 3],
    "Email_Address": ["USER@EXAMPLE.COM", "test@test.com", None],
    "UserScore": [85.5678, 92.1234, 78.9999],
    "IsActive": [True, False, True],
}

cleaned = UserDataCleaner(raw_data)
print(cleaned.df)
```

### Key Features

- **Kahan Summation**
    — Compensated rounding for floats to prevent accumulation errors
- **Automatic Logging** — Built-in method logging via `ABCLoggingMixin`
- **NaN Handling** — Automatic NaN to null conversion
- **Type Safety** — Full Polars type enforcement with validation

### Helper Methods

| Method | Description |
|--------|-------------|
| `strip_col(col)` | Remove leading/trailing whitespace from string column |
| `lower_col(col)` | Convert string column to lowercase |
| `round_col(col, precision)` | Round float column with Kahan summation |
| `skip_col_converter(col)` | Placeholder for columns without custom conversion |

---

## Data Structures

### Dictionary Utilities

**Module:** `winiutils.src.data.structures.dicts`

```python
from winiutils.src.data.structures.dicts import reverse_dict

original = {"a": 1, "b": 2, "c": 3}
reversed_dict = reverse_dict(original)
# {1: "a", 2: "b", 3: "c"}
```

### Text/String Utilities

**Module:** `winiutils.src.data.structures.text.string_`

| Function | Description |
|----------|-------------|
| `ask_for_input_with_timeout(prompt, timeout)` | Request user input with timeout enforcement |
| `find_xml_namespaces(xml)` | Extract namespace declarations from XML content |
| `value_to_truncated_string(value, max_length)` | Convert value to truncated string representation |
| `get_reusable_hash(value)` | Generate consistent SHA-256 hash for any object |

```python
from winiutils.src.data.structures.text.string_ import (
    value_to_truncated_string,
    get_reusable_hash,
    find_xml_namespaces,
)

# Truncate long strings
truncated = value_to_truncated_string(
    {"key": "very long value..."}, max_length=20
)

# Generate consistent hash
hash_value = get_reusable_hash({"user_id": 123, "action": "login"})

# Extract XML namespaces
xml = '<root xmlns:ns="http://example.com/ns">...</root>'
namespaces = find_xml_namespaces(xml)
# {"ns": "http://example.com/ns"}
```
