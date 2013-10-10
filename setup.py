import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = __import__('cram_unit').get_version()

_REQUIREMENTS_FILE = 'REQUIREMENTS.txt'
_README = 'README.md'


def _get_description():
    with open(_get_local_file(_README)) as f:
        _long_description = f.read()
    return _long_description


def _get_local_file(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def _get_requirements(file_name):
    with open(file_name, 'r') as f:
        reqs = [line for line in f if not line.startswith("#")]
    return reqs


setup(
    name='CramUnit',
    version=version,
    packages=['cram_unit'],
    license='BSD',
    author='mpkocher',
    author_email='mkocher@pacificbiosciences.com',
    url="http://github.com/mpkocher/CramUnit",
    download_url='https://github.com/mpkocher/CramUnit/tarball/0.7',
    description='Tool to create Unittests/Xunit output from cram (*.t) tests.',
    scripts=['bin/run_cram_unit.py'],
    install_requires=_get_requirements(_get_local_file(_REQUIREMENTS_FILE)),
    long_description=_get_description(),
    keywords='testing cram jenkins xunit'.split(),
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Topic :: Software Development :: Bug Tracking']
)
