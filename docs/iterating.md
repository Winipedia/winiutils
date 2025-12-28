# Iterating & Concurrency

The `winiutils.src.iterating` package provides utilities
for iteration and parallel execution.

---

## Concurrent Processing

A unified framework for parallel execution supporting both multiprocessing
(CPU-bound) and multithreading (I/O-bound) tasks
with automatic resource optimization.

### Multiprocessing

**Module:** `winiutils.src.iterating.concurrent.multiprocessing`

For CPU-bound tasks that benefit from bypassing Python's GIL.

#### `multiprocess_loop()`

Execute a function in parallel using a process pool.

```python
from winiutils.src.iterating.concurrent.multiprocessing import multiprocess_loop

def process_chunk(data, config):
    """CPU-intensive computation."""
    return heavy_computation(data, config)

results = multiprocess_loop(
    process_function=process_chunk,
    process_args=[(chunk,) for chunk in data_chunks],
    process_args_static=(config,),
    process_args_len=len(data_chunks),
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `process_function` | `Callable` | Function to execute in parallel |
| `process_args` | `Iterable[Iterable]` | Variable arguments per task |
| `process_args_static` | `Iterable` | Shared arguments for all tasks |
| `deepcopy_static_args` | `Iterable` | Arguments to deep-copy per process |
| `process_args_len` | `int` | Length hint for optimization |

#### `cancel_on_timeout()`

Decorator/wrapper to enforce execution time limits.

```python
from winiutils.src.iterating.concurrent.multiprocessing import cancel_on_timeout
import multiprocessing

# As a wrapper (recommended for pickle-able functions)
def slow_function():
    # Some potentially slow operation
    return result

timed_func = cancel_on_timeout(
    seconds=5, message="Operation timed out"
)(slow_function)

try:
    result = timed_func()
except multiprocessing.TimeoutError:
    result = default_value
```

**Note:** Only works with pickle-able functions. The function runs
in a separate process and is terminated if it exceeds the timeout.

#### `get_spwan_pool()`

Create a multiprocessing pool with spawn context (safer than fork).

```python
from winiutils.src.iterating.concurrent.multiprocessing import get_spwan_pool

with get_spwan_pool(processes=4) as pool:
    results = pool.map(my_function, items)
```

---

### Multithreading

**Module:** `winiutils.src.iterating.concurrent.multithreading`

For I/O-bound tasks like network requests, file I/O, or database queries.

#### `multithread_loop()`

Execute a function concurrently using a thread pool.

```python
from winiutils.src.iterating.concurrent.multithreading import multithread_loop

def fetch_url(url, headers):
    """I/O-bound operation."""
    return requests.get(url, headers=headers)

responses = multithread_loop(
    process_function=fetch_url,
    process_args=[(url,) for url in urls],
    process_args_static=(headers,),
    process_args_len=len(urls),
)
```

#### `imap_unordered()`

Apply a function to items in parallel, yielding results as they complete.

```python
from winiutils.src.iterating.concurrent.multithreading import imap_unordered
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    for result in imap_unordered(executor, process_item, items):
        handle_result(result)
```

#### `get_future_results_as_completed()`

Yield results from futures as they complete.

```python
from winiutils.src.iterating.concurrent.multithreading import (
    get_future_results_as_completed
)

futures = [executor.submit(func, arg) for arg in args]
for result in get_future_results_as_completed(futures):
    process(result)
```

---

### Shared Utilities

**Module:** `winiutils.src.iterating.concurrent.concurrent`

#### `find_max_pools()`

Calculate optimal worker pool size based on system resources.

```python
from winiutils.src.iterating.concurrent.concurrent import find_max_pools

# For multiprocessing
max_processes = find_max_pools(threads=False, process_args_len=100)

# For multithreading (typically CPU count × 4)
max_threads = find_max_pools(threads=True, process_args_len=100)
```

**Factors considered:**

- Available CPU cores
- Currently active processes/threads
- Number of tasks to process
- Ensures at least 1 worker

---

## Iteration Utilities

**Module:** `winiutils.src.iterating.iterate`

### `get_len_with_default()`

Get the length of an iterable with a fallback default.

```python
from winiutils.src.iterating.iterate import get_len_with_default

# Works with sized iterables
length = get_len_with_default([1, 2, 3], default=0)  # 3

# Falls back to default for generators
def gen():
    yield from range(10)

length = get_len_with_default(gen(), default=10)  # 10
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Automatic Worker Optimization** | Calculates optimal pool size based on system resources |
| **Progress Tracking** | Built-in tqdm integration for real-time progress bars |
| **Order Preservation** | Results returned in original input order |
| **Spawn Context** | Uses `spawn` instead of `fork` for safer multiprocessing |
| **Error Handling** | Graceful handling of timeouts and process failures |

---

## Best Practices

1. **Choose the right executor:**
   - Use `multiprocess_loop` for CPU-bound tasks
        (image processing, ML inference)
   - Use `multithread_loop` for I/O-bound tasks (API calls, file I/O)

2. **Provide length hints:**
    Pass `process_args_len` for better worker optimization

3. **Use deep-copy for mutables:**
    Use `deepcopy_static_args` for mutable objects in multiprocessing

4. **Handle timeouts:**
    Wrap potentially slow operations with `cancel_on_timeout`
