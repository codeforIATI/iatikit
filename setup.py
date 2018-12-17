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
    version='1.3.1',
    packages=find_packages(),
    license='MIT',
    keywords='IATI',
    long_description=readme,
    install_requires=[
        'certifi>=2017.4.17',
        'chardet>=3.0.2,<3.1.0',
        'idna>=2.5,<2.8',
        'lxml>=4.2.5',
        'requests>=2.20.0',
        'urllib3>=1.21.1,<1.25',
    ],
)
