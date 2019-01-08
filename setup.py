from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

data = {}
with open(join(path, 'pyandi', '__version__.py')) as f:
    exec(f.read(), data)

test_deps = [
    'tox',
    'mock',
    'pytest',
    'pytest-cov',
    'coveralls',
    'freezegun',
]
extras = {'test': test_deps}

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
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=[
        'lxml',
        'requests',
        'unicodecsv',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_deps,
    extras_require=extras,
)
