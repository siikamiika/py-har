# py-har

HTTP Archive parser for Python >= 3.8.

## Usage

```python
import py_har
import json

with open('file.har') as f:
    har_data = json.loads(f.read())

har = py_har.Har(**har_data)
```

## License

MIT
