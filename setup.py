from setuptools import setup

setup(
  name='pyswaggerclient',
  version='1.3',
  packages=['pyswaggerclient'],
  license='Apache-2.0',
  long_description=open('README.md', 'r').read(),
  install_requires=[
    'pyaml',
    'pyswagger',
    'requests',
  ],
)
