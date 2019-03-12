from setuptools import setup, find_packages
from os.path import abspath, dirname, join


path = abspath(dirname(__file__))
with open(join(path, 'README.rst')) as f:
    readme = f.read()

data = {}
with open(join(path, 'iatikit', '__version__.py')) as f:
    exec(f.read(), data)

test_deps = [
    'tox',
    'mock',
    'pytest',
    'pytest-cov',
    'coveralls',
    'freezegun',
    'pylint<2.0.0',
]
extras = {'test': test_deps}

setup(
    name='iatikit',
    description='A toolkit for using IATI data.',
    url='https://iatikit.readthedocs.io',
    author='Andy Lulham',
    author_email='a.lulham@gmail.com',
    version=data.get('__version__'),
    packages=find_packages(),
    license='MIT',
    keywords='IATI',
    long_description=readme,
    install_requires=[
        'configparser',
        'lxml',
        'requests',
        'unicodecsv',
        'future',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    setup_requires=['pytest-runner'],
    tests_require=test_deps,
    extras_require=extras,
)
