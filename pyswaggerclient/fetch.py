import json
import yaml
from urllib import request
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

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

def read_spec(spec_file):
    try:
        return yaml.load(spec_file)
    except:
        return json.load(spec_file)

def fetch_spec(spec_url, **kwargs):
    req = request.urlopen(
      request.Request(
        spec_url,
        **kwargs
      )
    )
    spec = read_spec(req)
    if spec.get('swagger', '').startswith('2'):
        return get_spec_v2(spec)
    if spec.get('openapi', '').startswith('3'):
        return get_spec_v3(spec)
    raise Exception('Spec version could not be identified')

def fetch_spec_raw(*args, **kwargs):
    return json.dumps(fetch_spec(*args, **kwargs))
