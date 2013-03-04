try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = __import__('cram_unit').get_version()

with open('README.md') as f:
    _long_description = f.read()

setup(
    name='CramUnit',
    version=version,
    packages=['cram_unit'],
    license='BSD',
    author='mpkocher',
    author_email='mkocher@pacificbiosciences.com',
    url="http://github.com/mpkocher/CramUnit",
    description='Tool to create Unittests/Xunit output from cram (*.t) tests.',
    scripts=['bin/run_cram_unit.py'],
    install_requires=['cram', 'nose'],
    long_description=_long_description,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Topic :: Software Development :: Bug Tracking']
)
