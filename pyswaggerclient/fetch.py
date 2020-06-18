import re
import json
import yaml
from urllib import request
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from .util import slugify

def get_spec_v2(spec_v2):
    # Use v2 spec as-is
    return spec_v2

def get_spec_v3(spec_v3):
    # Convert v3 spec to v2 with api-spec-converter
    with NamedTemporaryFile('w') as spec_v3_file:
        json.dump(spec_v3, spec_v3_file)
        spec_v3_file.flush()
        process = Popen(
            [
                'api-spec-converter',
                '--from=openapi_3',
                '--to=swagger_2',
                spec_v3_file.name
            ],
            stdout=PIPE,
        )
        spec_v2 = json.load(process.stdout)
        return spec_v2

def repair_spec(spec_v2):
    # Fill in sane default operationIds if not present or broken
    op_ids = set()
    for path in spec_v2['paths'].keys():
        for method in [
            'get',
            'put',
            'post',
            'delete',
            'options',
            'head',
            'patch',
        ]:
            endpoint = spec_v2['paths'][path].get(method)
            if not endpoint:
                continue
            # Get current operationId
            op_id = endpoint.get('operationId')
            # operationId not actually specified, or we have a duplicate
            if not op_id or op_id in op_ids:
                # Generate operation id {path}_{method}
                op_id = path + '_' + method
            # Ensure operationId is properly slugified
            op_id = slugify(op_id).strip('_')
            # Ensure we don't have any duplicates
            assert op_id not in op_ids, 'Duplicate operation id could not be resolved! (%s)' % (op_id)
            # Add the operation id to the set
            op_ids.add(op_id)
            # Update the spec
            spec_v2['paths'][path][method]['operationId'] = op_id

    # add leading slash on paths if not present
    spec_v2['paths'] = {
        ('/' + path) if not path.startswith('/') else path: op
        for path, op in spec_v2['paths'].items()
    }

    if spec_v2.get('basePath') is not None:
        spec_v2['basePath'] = spec_v2['basePath'].rstrip('/')

    return spec_v2

def parse_spec(spec_file):
    try:
        return yaml.load(spec_file)
    except:
        return json.load(spec_file)

def read_spec(spec):
    if spec.get('swagger', '').startswith('2'):
        return get_spec_v2(spec)
    if spec.get('openapi', '').startswith('3'):
        return get_spec_v3(spec)
    raise Exception('Spec version could not be identified')

def fetch_spec(spec_url, **kwargs):
    return request.urlopen(
      request.Request(
        spec_url,
        **kwargs
      )
    )

def resolve_spec(spec_file_or_url, **kwargs):
    ''' Resolves the spec whether it's a url to, json of, or file containing
    spec in v3 / v2, json / yaml format. Note that a string is assumed to
    be a url, so parse your JSON if it's serialized.
    '''
    if type(spec_file_or_url) == str:
        return repair_spec(read_spec(parse_spec(fetch_spec(spec_file_or_url, **kwargs))))
    elif type(spec_file_or_url) == dict:
        return repair_spec(read_spec(spec_file_or_url))
    else:
        return repair_spec(read_spec(parse_spec(spec_file_or_url)))
