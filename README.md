# PySwaggerClient
A pyswagger wrapper for pythonic swagger client bindings. Exposes the API to python complete with tab-completion, documentation, and seamless programatic access.

## Installation
```bash
# stable
pip install https://github.com/u8sand/PySwaggerClient/archive/v1.0.zip
# optional for openapi-3 version handling
npm install -g api-spec-converter
```

### Edge
```bash
pip install --upgrade https://github.com/u8sand/PySwaggerClient/archive/master.zip
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
