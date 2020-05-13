''' Usage:
from pyswaggerclient import SwaggerClient

client = SwaggerClient('your_swagger_url', headers={'auth': 'whatever', 'if': 'necessary'})
client.actions.your_op_id.call(your=params)
'''

import json
from urllib import request
from pyswagger import App
from pyswagger.getter import SimpleGetter
from pyswagger.contrib.client.requests import Client
from .fetch import resolve_spec
from .util import bind, slugify

class SwaggerClient:
  def __init__(self, url, headers=None):
    self._headers = headers or {}
    self._url = url
    self._update()

  def update(self, url=None, headers=None):
    if url is not None:
      self._url = url
    if headers is not None:
      self._headers = headers
    self._update()

  def request(self, url, headers=None, response_as_json=True):
    response = request.urlopen(
      request.Request(
        url,
        headers=headers or self._headers,
      )
    ).read()
    if response_as_json:
      try:
        return json.loads(response)
      except:
        pass
    return response

  def _client_request(self, path, *args, **kwargs):
    response = self._client.request(
      self._app.op[path if type(path) == str else '!##!'.join(path)](
        *args,
        **kwargs,
      ),
      headers=self._headers,
    )
    try:
      return json.loads(response.raw.decode())
    except:
      pass
    try:
      return json.loads(response.decode())
    except:
      pass
    return response

  def _update(self):
    self._app = self._create_app(self._url, headers=self._headers)
    self._client = self._create_client()
    self._update_magic()

  def _update_magic(self):
    setattr(self, 'models', type('Models', (object,), dict(self._create_models())))
    setattr(self, 'actions', type('Actions', (object,), dict(self._create_actions())))
  
  def _create_models(self):
    for model_name, model in self._app.m.items():
        yield (model_name, type(model_name, (object,), model.properties))

  def _create_actions(self):
    for k, v in self._app.op.items():
      name = slugify(k.split('!##!')[-1])
      v.call = bind(self._client_request, k)
      v.call.__name__ = name
      v.__doc__ = v.call.__doc__ = self._create_doc(v)
      yield (name, v)
  
  def _create_doc(self, obj):
    return '\n'.join(
      map(lambda s: s.strip(' '),
        '''
        {description}

        Parameters
        ==========
        {parameters}

        Response
        ==========
        {responses}
        '''.format(
          description=obj.description if obj.description else '',
          parameters='\n'.join(
            self._create_param_doc(param)
            for param in obj.parameters
          ),
          responses='\n'.join(
            self._create_response_doc(*resp)
            for resp in obj.responses.items()
          )
        ).splitlines()
      )
    ).strip('\n')
  
  def _create_param_doc(self, param):
    return '\n'.join(
      map(lambda s: s.strip(' '),
        '''
        {name}: {type}
        {description}
        '''.format(
          name=param.name,
          type=param.type,
          description=param.description,
        ).splitlines()
      )
    ).strip('\n')
  
  def _create_response_doc(self, code, resp):
    return '\n'.join(
      map(lambda s: s.strip(' '),
        '''
        {code}: {description}
        '''.format(
          code=code,
          description=resp.description,
        ).splitlines()
      )
    ).strip('\n')

  def _create_app(self, url, headers):
    app = App.load(url,
      getter=self._create_getter(headers=headers),
    )
    app.prepare(strict=False)
    return app

  def _create_getter(self, headers):
    class Getter(SimpleGetter):
      __simple_getter_callback__ = bind(
        resolve_spec,
        headers=headers,
      )
    return Getter

  def _create_client(self):
    return Client()
