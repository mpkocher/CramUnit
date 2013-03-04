try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = __import__('cram_unit').get_version()

setup(
    name='CramUnit',
    version=version,
    packages=['cram_unit'],
    license='BSD',
    author='mpkocher',
    author_email='mkocher@pacificbiosciences.com',
    description='Tool to create Unittests/Xunit output from cram (*.t) tests.',
    scripts=['bin/run_cram_unit.py'],
    install_requires=['cram', 'nose']
)
