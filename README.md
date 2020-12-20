# py-har

HTTP Archive parser and mutator for Python >= 3.8.

## Usage

```python
import py_har
import json

har = py_har.Har(**json.loads(open('file.har').read()))
har.get('log').get('entries')[1].set('startedDateTime', '2020-01-01')
print(json.dumps(har.get('log').get('entries')[1].to_dict(), indent=4))
```

## License

MIT
