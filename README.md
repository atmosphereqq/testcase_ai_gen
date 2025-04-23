# Swagger Test Case Generator

Automatically generate test cases from Swagger/OpenAPI specifications.

## Features

- Generate normal flow test cases
- Generate error flow test cases  
- Generate boundary value test cases
- Generate security test cases (OWASP Top 10)
- Output JSON and HTML reports

## Installation (Original - May Not Work)

```bash
pip install -e .
```

## Standalone Usage (Recommended)

Due to potential package installation issues, we recommend using the standalone runner:

```bash
python3 standalone_runner.py path/to/swagger.yaml
```

Example with included sample file:

```bash
python3 standalone_runner.py examples/petstore.yaml
```

Requirements:
- Python 3.x
- PyYAML (`pip install pyyaml`)
- Jinja2 (`pip install jinja2`)

## Original Usage (If Package Works)

```bash
swagger-testgen path/to/swagger.yaml
```

This will generate:
- `output/test_cases.json` - All test cases in JSON format
- `output/report.html` - HTML report of test cases

## Output Format

Test cases follow this JSON schema:

```json
{
  "name": "string",
  "type": "normal|error|boundary|security",
  "request": {
    "method": "string",
    "path": "string",
    "parameters": {}
  },
  "expect": {
    "status": "number|array",
    "not_contains": ["string"]
  }
}
```

## Development

Run tests:
```bash
pytest
