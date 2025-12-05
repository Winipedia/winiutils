# OOP Utilities

The `winiutils.src.oop` package provides metaclasses and mixins for automatic method instrumentation and class composition.

---

## Logging Mixins

Automatic method logging with performance tracking, zero boilerplate required.

### ABCLoggingMeta

**Module:** `winiutils.src.oop.mixins.meta`

A metaclass that automatically wraps all non-magic methods with logging functionality.

```python
from winiutils.src.oop.mixins.meta import ABCLoggingMeta
from abc import abstractmethod

class MyAbstractService(metaclass=ABCLoggingMeta):
    @abstractmethod
    def execute(self) -> None:
        pass

class ConcreteService(MyAbstractService):
    def execute(self) -> None:
        print("Executing...")
    
    def process(self, data: list) -> int:
        return len(data)

# All methods automatically logged
service = ConcreteService()
service.execute()
# Logs: "ConcreteService - Calling execute with () and {}"
# Logs: "ConcreteService - execute finished with 0.001 seconds -> returning None"
```

**Features:**

- Extends `ABCMeta` for abstract class support
- Wraps `classmethod`, `staticmethod`, and instance methods
- Excludes magic methods (`__init__`, `__str__`, etc.)
- Rate-limited logging (1 second threshold between same method calls)

### ABCLoggingMixin

**Module:** `winiutils.src.oop.mixins.mixin`

A ready-to-use mixin class with `ABCLoggingMeta` pre-configured.

```python
from winiutils.src.oop.mixins.mixin import ABCLoggingMixin

class MyService(ABCLoggingMixin):
    def process_data(self, data: list) -> dict:
        return {"processed": len(data)}

    @classmethod
    def validate(cls, value: str) -> bool:
        return len(value) > 0

    @staticmethod
    def helper(x: int) -> int:
        return x * 2

# All methods automatically logged
service = MyService()
result = service.process_data([1, 2, 3])
```

---

## How It Works

The metaclass intercepts class creation and wraps methods at definition time:

```
Class Definition
       ↓
ABCLoggingMeta.__new__()
       ↓
Iterate class attributes
       ↓
Identify callable, non-magic methods
       ↓
Wrap each with logging decorator
       ↓
Return modified class
```

### Logging Wrapper Behavior

For each method call:

1. Check if >1 second since last call to same method
2. If yes, log method name, class name, arguments, kwargs
3. Execute the original method
4. Log execution duration and return value
5. Update last call time for rate limiting

---

## Log Output

```
INFO - MyService - Calling process_data with ([1, 2, 3],) and {}
INFO - MyService - process_data finished with 0.001234 seconds -> returning {'processed': 3}
INFO - MyService - Calling validate with ('test',) and {}
INFO - MyService - validate finished with 0.000123 seconds -> returning True
```

---

## Configuration

### Rate Limiting

Logging is rate-limited to prevent spam in tight loops. The threshold is 1 second between identical method calls.

### Truncation

Arguments and return values are truncated to 20 characters for readability:

```python
# Long argument
service.process([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# Logs: "... with ([1, 2, 3, ...] and {}"
```

### Excluded Methods

Magic methods (starting with `__`) are not wrapped:

- `__init__`, `__str__`, `__repr__`
- `__eq__`, `__hash__`, `__len__`
- etc.

---

## Integration Example

The `CleaningDF` class uses `ABCLoggingMixin` for automatic pipeline logging:

```python
from winiutils.src.oop.mixins.mixin import ABCLoggingMixin

class CleaningDF(ABCLoggingMixin):
    def rename_cols(self, df):
        # Automatically logged
        ...
    
    def fill_nulls(self):
        # Automatically logged
        ...
    
    def clean(self):
        # Each step logged with timing
        self.rename_cols()
        self.fill_nulls()
        self.convert_cols()
        ...
```

Output during cleaning:
```
INFO - CleaningDF - Calling rename_cols with (...) and {}
INFO - CleaningDF - rename_cols finished with 0.002 seconds -> ...
INFO - CleaningDF - Calling fill_nulls with (...) and {}
INFO - CleaningDF - fill_nulls finished with 0.001 seconds -> ...
```

---

## Technical Details

| Aspect | Implementation |
|--------|----------------|
| Metaclass inheritance | Extends `ABCMeta` |
| Decorator preservation | Uses `@functools.wraps` |
| Performance | Caches `time.time` function reference |
| Thread safety | Per-method call time tracking |
| Memory | Call times stored in closure |

---

## Best Practices

1. **Use the mixin for simplicity:** `ABCLoggingMixin` is the easiest way to add logging

2. **Use metaclass for abstract classes:** When defining abstract base classes with logging

3. **Combine with other mixins:** `ABCLoggingMixin` works well in multiple inheritance

4. **Configure logging level:** Set logging level appropriately to control output

```python
import logging
logging.getLogger("winiutils.src.oop.mixins.meta").setLevel(logging.WARNING)
```

