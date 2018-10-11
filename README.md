# PySwaggerClient
A pyswagger wrapper for pythonic swagger client bindings. Exposes the API to python complete with tab-completion, documentation, and seamless programatic access.

## Installation
```bash
pip install https://github.com/u8sand/PySwaggerClient/archive/master.zip
# optional for openapi-3 version handling
npm install -g api-spec-converter
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
```bash
pip install -r requirements.txt
```

`api-spec-converter` is an optional npm dependency for openapi 3 spec conversions. You can get it with:
```bash
npm install -g api-spec-converter
```
