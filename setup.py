import re
from os import path
from setuptools import setup

version_py = open('github_api/cli/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", version_py))

cur_dir = path.abspath(path.dirname(__file__))
with open(path.join(cur_dir, 'README.md')) as f:
    long_description = f.read()

setup(
    name='github-api-tools',
    version=metadata['version'],
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    url='',
    license='Apache License 2.0',
    author='Tetsuya Morimoto',
    author_email='tm@kazamori.jp',
    zip_safe=False,
    platforms='any',
    packages=['github_api'],
    namespace_packages=['github_api'],
    include_package_data=True,
    install_requires=[
        'PyGithub',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
    ],
    tests_require=[
        'tox', 'pytest', 'pytest-flake8',
    ],
    entry_points={
        'console_scripts': [
            'gh-cli-pulls=github_api.cli.pulls.main:main',
        ],
    },
)
