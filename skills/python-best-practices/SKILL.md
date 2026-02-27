---
name: python-best-practices
description: Comprehensive Python coding standards, type hints, testing patterns, and PEP 8 compliance for AI-assisted development.
license: Apache-2.0
metadata:
  category: best-practices
  tags: [python, testing, code-quality, type-hints]
---

# Python Best Practices

This skill provides comprehensive guidance for writing clean, maintainable, and testable Python code, especially when working with AI-assisted development.

## Code Style and Formatting

### 1. PEP 8 Compliance
```python
# Use 4 spaces for indentation
def calculate_total(items):
    total = 0
    for item in items:
        total += item.value
    return total

# Line length: max 79 characters (soft), 88 (hard)
long_variable_name = "this_is_acceptable"  # 27 chars
acceptable_but_longer = "this_name_is_still_within_limits"  # 36 chars

# Import order: standard library → third party → local
import os  # standard library
import tempfile  # standard library
import openai  # third party
from .local_module import local_function  # local
```

### 2. Type Hints
```python
from typing import List, Dict, Optional, TypedDict, Union
from datetime import datetime

def process_data(
    items: List[Dict[str, Union[str, int]]],
    timestamp: Optional[datetime] = None
) -> List[str]:
    """Process data items and return results."""
    results = []
    for item in items:
        processed = str(item.get("value", 0))
        results.append(processed)

    return results

# TypedDict for structured data
class UserProfile(TypedDict):
    name: str
    age: int
    email: Optional[str]
```

### 3. Docstrings
```python
def complex_function(param1: str, param2: int) -> bool:
    """
    Perform complex calculation on input parameters.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        bool: True if calculation succeeds, False otherwise

    Raises:
        ValueError: If param2 is negative

    Examples:
        >>> complex_function("test", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")

    return True
```

## Error Handling

### 1. Specific Exceptions
```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class APIError(Exception):
    """Raised when API calls fail."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

def validate_input(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValidationError("Input must be a dictionary")

    if not data.get("required_field"):
        raise ValidationError("required_field is missing")

    return data
```

### 2. Context Managers
```python
from contextlib import contextmanager

@contextmanager
def database_connection():
    """Context manager for database connections."""
    conn = create_connection()

    try:
        yield conn
    finally:
        conn.close()

# Usage
with database_connection() as conn:
    result = conn.execute("SELECT * FROM users")
```

### 3. Logging
```python
import logging
from datetime import datetime

def setup_logging(name: str = __name__):
    """Set up structured logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    return logging.getLogger(name)

logger = setup_logging(__name__)

def process_item(item: dict) -> None:
    logger.info(f"Processing item: {item.get('id')}")
    logger.debug(f"Item details: {item}")

    try:
        result = complex_operation(item)
        logger.info(f"Successfully processed item {item.get('id')}")
    except Exception as e:
        logger.error(f"Failed to process item {item.get('id')}: {e}", exc_info=True)
```

## Data Structures and Algorithms

### 1. List Comprehensions
```python
# Good
squares = [x ** 2 for x in range(10)]
filtered = [x for x in numbers if x % 2 == 0]
mapped = [x * 3 for x in numbers]

# Avoid for complex logic
bad = []
for x in range(10):
    bad.append(x ** 2)
```

### 2. Generator Functions
```python
def read_large_file(file_path: str):
    """Read large file efficiently using generator."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

# Usage
for line in read_large_file("large_file.txt"):
    process_line(line)
```

### 3. Dataclasses
```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

# Usage
user = User(id=1, name="John Doe")
print(user.email)  # None
```

## File I/O

### 1. Path Operations
```python
from pathlib import Path

def read_config(config_path: Path) -> dict:
    """Read configuration file using pathlib."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    return json.loads(config_path.read_text())

def write_output(data: dict, output_path: Path) -> None:
    """Write output data atomically."""
    temp_path = output_path.with_suffix('.tmp')

    # Write to temp file
    with open(temp_path, 'w') as f:
        json.dump(data, f, indent=2)

    # Atomic rename
    temp_path.replace(output_path)
```

### 2. Resource Management
```python
def process_file_safe(file_path: str) -> str:
    """Safely process file with proper resource cleanup."""
    file_obj = None
    result = ""

    try:
        file_obj = open(file_path, 'r')
        result = file_obj.read()

    finally:
        if file_obj:
            file_obj.close()

    return result
```

## Concurrency and Async

### 1. Async/Await Patterns
```python
import asyncio
from typing import List

async def fetch_multiple_urls(urls: List[str]) -> List[str]:
    """Fetch multiple URLs concurrently."""
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def fetch_url(url: str) -> str:
    """Fetch single URL."""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### 2. Threading
```python
from concurrent.futures import ThreadPoolExecutor
import time

def process_tasks_parallel(tasks: list, max_workers: int = 4) -> list:
    """Process tasks in parallel using thread pool."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_task, tasks))
    return results

def process_task(task: str) -> str:
    """Process single task."""
    time.sleep(1)  # Simulate work
    return f"Processed: {task}"
```

## Testing Patterns

### 1. Unit Tests
```python
import pytest
from unittest.mock import MagicMock, patch

class TestCalculator:

    def test_add_positive_numbers(self):
        result = add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        result = add(-1, -2)
        assert result == -3

    @patch('module.function_name')
    def test_with_mock(self, mock_function):
        mock_function.return_value = 42
        result = module.function_name()
        assert result == 42
        mock_function.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_function(self):
        result = await async_operation()
        assert result == "expected"
```

### 2. Fixtures
```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }

@pytest.fixture
def mock_database():
    """Provide mock database connection."""
    return MagicMock()

def test_with_fixtures(sample_data, mock_database):
    user = User(**sample_data)
    mock_database.add.assert_called_with(user)
```

### 3. Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (5, 10),
    (0, 0)
])
def test_multiplication(input, expected):
    assert multiply(input, 2) == expected
```

### 4. Integration Tests
```python
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.mark.asyncio
async def test_workflow_integration():
    async with WorkflowEnvironment() as env:
        client = await env.client()

        # Mock activities
        env.mock_activity("process_data", lambda x: f"Processed: {x}")

        result = await client.execute_workflow(
            TestWorkflow.run,
            "test input",
            id="integration-test"
        )

        assert result == "Processed: test input"
```

## Performance Optimization

### 1. Caching
```python
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=100)
def expensive_calculation(x: int, y: int) -> int:
    """Cache expensive calculation results."""
    import time
    time.sleep(0.1)  # Simulate expensive operation
    return x * y

# Alternative: disk-based cache
def cache_to_disk(key: str, data: any) -> None:
    """Cache data to disk."""
    cache_file = f".cache/{hashlib.md5(key.encode()).hexdigest()}"
    os.makedirs(".cache", exist_ok=True)

    with open(cache_file, 'w') as f:
        json.dump(data, f)

def load_from_cache(key: str) -> any:
    """Load data from cache."""
    cache_file = f".cache/{hashlib.md5(key.encode()).hexdigest()}"
    if not os.path.exists(cache_file):
        return None

    with open(cache_file, 'r') as f:
        return json.load(f)
```

### 2. Lazy Loading
```python
class DataLoader:
    """Lazy load data only when needed."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._data = None

    @property
    def data(self) -> list:
        if self._data is None:
            self._load_data()
        return self._data

    def _load_data(self) -> None:
        with open(self.file_path, 'r') as f:
            self._data = json.load(f)
```

### 3. Memory Efficiency
```python
import gc
import sys

def process_large_dataset(items: list):
    """Process large dataset with memory efficiency."""
    batch_size = 1000
    results = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_result = process_batch(batch)
        results.extend(batch_result)

        # Explicitly clean up
        del batch
        gc.collect()

    return results
```

## Security Best Practices

### 1. Input Validation
```python
import re
from typing import Any

def sanitize_input(input_data: Any) -> str:
    """Sanitize user input to prevent injection attacks."""
    if isinstance(input_data, str):
        # Remove SQL injection patterns
        sanitized = re.sub(r'["\';--]', '', input_data)

        # Remove HTML tags
        sanitized = re.sub(r'<.*?>', '', sanitized)

        return sanitized.strip()

    raise ValueError("Invalid input type")

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

### 2. Secrets Management
```python
import os
from dotenv import load_dotenv
import keyring

def get_secret(secret_name: str) -> str:
    """Get secret securely from environment or keyring."""
    # Try environment variable first
    secret = os.getenv(secret_name)

    if secret:
        return secret

    # Try keyring for more sensitive secrets
    try:
        secret = keyring.get_password("myapp", secret_name)
        if secret:
            return secret
    except:
        raise ValueError(f"Secret {secret_name} not found")

# Usage
api_key = get_secret("OPENAI_API_KEY")
database_url = get_secret("DATABASE_URL")
```

### 3. File Permissions
```python
import os
import stat

def ensure_secure_file_permissions(file_path: str) -> None:
    """Set secure file permissions."""
    # Owner read/write only
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)

    # No permissions for group or others
    # This is more restrictive than 0o600
```

## Documentation and Comments

### 1. Inline Comments
```python
# Bad: obvious comment
result = add(a, b)  # Add two numbers

# Good: comment explains why
result = add(a, b)  # Sum must be non-negative for business logic

# Bad: noisy
# Increment count
count += 1

# Good: contextual
# Track processed items for progress reporting
count += 1
```

### 2. Type Checking
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mymodule import ExternalClass

def process_data(data: list) -> None:
    if TYPE_CHECKING:
        # This allows type hints without circular imports
        process_with_external(data)
```

## AI-Assisted Development

### 1. Working with AI Output
```python
def clean_ai_response(response: str) -> str:
    """Clean up AI-generated code."""
    # Remove markdown formatting
    cleaned = response.replace('```python', '').replace('```', '')

    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())

    return cleaned.strip()

def validate_ai_code(code: str) -> bool:
    """Validate AI-generated Python code."""
    try:
        compile(code, '<string>')
        return True
    except SyntaxError as e:
        print(f"Invalid Python code generated: {e}")
        return False
```

### 2. Prompt Engineering
```python
def create_prompt(template: str, **kwargs) -> str:
    """Create structured prompt from template."""
    return template.format(**kwargs)

# Usage
prompt_template = """
Analyze the following data:
{data}

Provide insights in JSON format with these fields:
- summary
- key_points
- recommendations
"""

prompt = create_prompt(
    template=prompt_template,
    data="Sales data for Q3 2024"
)
```

## Project Structure

### 1. Package Organization
```
myproject/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── api/
│       ├── __init__.py
│       └── client.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── requirements.txt
├── setup.py
└── README.md
```

### 2. Configuration Management
```python
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import yaml

@dataclass
class Config:
    """Application configuration."""
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    log_level: str = "INFO"
    cache_dir: Optional[str] = None

    @classmethod
    def from_file(cls, path: Path) -> 'Config':
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)
```

## Tools and Utilities

### 1. Linting Setup
```ini
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra"

[tool.mypy]
python_version = "3.9"
warn_return_any = True
warn_unused_ignores = True
```

### 2. Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3.9
        types: [python]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        types: [python]
```

## References
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Formatter](https://github.com/psf/black)
- [Mypy Type Checker](https://mypy.readthedocs.io/)
