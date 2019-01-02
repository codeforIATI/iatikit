from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

data = {}
with open(join(path, 'pyandi', '__version__.py')) as f:
    exec(f.read(), data)

setup(
    name='pyandi',
    description='A toolkit for using IATI data.',
    url='https://pyandi.readthedocs.io',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    version=data.get('__version__'),
    packages=find_packages(),
    license='MIT',
    keywords='IATI',
    long_description=readme,
    install_requires=[
        'lxml',
        'requests',
        'unicodecsv',
    ],
)
