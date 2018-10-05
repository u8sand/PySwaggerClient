import re

def bind(func, *args, **kwargs):
  ''' Bind positional and named arguments to `func`.
  e.g.
  Input:
    new_print = bind(print, '>', sep=' ', end='!\n')
  Output:
    new_print('Test')
    > Test!
  '''
  # Create the 
  def func_wrapper(*_args, **_kwargs):
    return func(*args, *_args, **dict(kwargs, **_kwargs))
  return func_wrapper

def slugify(s):
  ''' Slugify string ensuring that the string is
  accessible as a variable name in python.
  '''
  # Normalize separators
  s = re.sub(
    r'[ \-_\./\\:]+', '_',
    s
  )
  # Remove completely non-standard characters
  s = re.sub(
    r'[^A-Za-z0-9_]+', '',
    s
  )
  # Ensure string doesn't start with number
  if re.match(r'^[0-9].+$', s):
    s = '_' + s
  return s
