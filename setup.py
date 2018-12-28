from setuptools import setup, find_packages
from os.path import join, dirname


with open(join(dirname(__file__), 'README.rst')) as f:
    readme = f.read()

setup(
    name='pyandi',
    description='A toolkit for using IATI data.',
    url='https://pyandi.readthedocs.io',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    version='1.5.2',
    packages=find_packages(),
    license='MIT',
    keywords='IATI',
    long_description=readme,
    install_requires=[
        'lxml',
        'requests',
    ],
)
