''' Usage:
python3 -m pyswaggerclient your_swagger_url > your_client.py

This has the added benefit of being statically introspectable by i.e. jedi.
'''
import os
import re
from jinja2 import Environment, FileSystemLoader
from pyswaggerclient.client import SwaggerClient

def slugify(val):
  return re.sub(r'[^A-Za-z0-9_]+', '', val).lower()

type_lookup = {
  None: lambda o: 'None',
  'string': lambda o: 'str',
  'number': lambda o: 'float',
  'integer': lambda o: 'int',
  'boolean': lambda o: 'bool',
  'array': lambda o: 'List[{}]'.format(swagger_type_to_python_type(o.items)),
  'object': lambda o: 'Dict[str, {}]'.format(swagger_type_to_python_type(o.additionalProperties or 'Any')),
}
def swagger_type_to_python_type(o):
  if type(o) == list:
    if len(o) > 1:
      return 'Union[{}]'.format(','.join(map(swagger_type_to_python_type, o)))
    else:
      return swagger_type_to_python_type(o[0])
  elif type(o) == dict:
    if 'type' not in o and 'schema' in o:
      return swagger_type_to_python_type(o['schema'])
    if 'type' not in o and 'content' in o:
      return swagger_type_to_python_type(o['content'])
    return type_lookup[o['type']](o)
  elif type(o) == bool:
    return 'Any'
  else:
    if getattr(o, 'type', None) is None and getattr(o, 'schema', None) is not None:
      return swagger_type_to_python_type(getattr(o, 'schema'))
    if getattr(o, 'type', None) is None and getattr(o, 'content', None) is not None:
      return swagger_type_to_python_type(getattr(o, 'content'))
    return type_lookup[o.type](o)

def generate_static_client(classname, url):
  client = SwaggerClient(url)
  return Environment(
    loader=FileSystemLoader(
      os.path.realpath(os.path.dirname(__file__)),
    ),
  ).get_template('./client.py.in').render(
    swagger_type_to_python_type=swagger_type_to_python_type,
    list=list,
    slugify=slugify,
    classname=classname,
    client=client,
  )
