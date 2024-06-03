from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name='aligner',
    version='1.3.0',
    description='Package for alignment',
    author='Alisa Vu',
    author_email='ahvu@ucsd.edu',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aligner=aligner.aligner:main'
        ],
    },
)