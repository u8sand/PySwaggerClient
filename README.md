# PySwaggerClient
A pyswagger wrapper for pythonic swagger client bindings. Exposes the API to python complete with tab-completion, documentation, and seamless programatic access.

## Installation
```python
pip install https://github.com/u8sand/PySwaggerClient/archive/master.zip
```

### Usage
```
from pyswaggerclient import SwaggerClient

client = SwaggerClient('your_swagger_url', headers={
  'auth': 'whatever',
  'if': 'necessary'
})
client.actions.your_op_id.call(your=params)
```

## Development

### Install dependencies
```python
pip install -r requirements.txt
```
