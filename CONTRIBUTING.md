# Contributing to Temporal-OpenAI Agents SDK

Thank you for your interest in contributing! This repository is meant for learning and experimentation.

## How to Contribute

### Adding Examples

1. Create a new Python file in the appropriate directory:
   - `examples/temporal/` for Temporal-specific examples
   - `examples/openai/` for OpenAI-specific examples
   - `examples/integration/` for combined examples

2. Follow the existing code style:
   - Use docstrings for modules, classes, and functions
   - Keep examples simple and well-commented
   - Include error handling for API keys and configuration

3. Update the relevant README.md file with:
   - Description of your example
   - How to run it
   - What users will learn

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Add comments for complex logic

### Testing

If you're adding non-trivial functionality:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-example`)
3. Commit your changes (`git commit -am 'Add example for X'`)
4. Push to the branch (`git push origin feature/my-example`)
5. Create a Pull Request

## Questions?

Feel free to open an issue for discussion!
