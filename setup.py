from setuptools import setup, find_packages
from os.path import join, dirname


with open(join(dirname(__file__), 'README.rst')) as f:
    readme = f.read()

setup(
    name='pyandi',
    description='A query language wrapper around XPath, with some ' +
                'IATI-related helpers included.',
    url='https://github.com/andylolz/pyandi',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    version='1.4.0',
    packages=find_packages(),
    license='MIT',
    keywords='IATI',
    long_description=readme,
    install_requires=[
        'certifi',
        'chardet',
        'idna',
        'lxml',
        'requests',
        'urllib3',
    ],
)
