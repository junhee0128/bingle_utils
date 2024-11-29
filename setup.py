from setuptools import setup, find_packages

setup(
    name='bingle',
    version='0.1.1',
    author='junhee',
    packages=find_packages(include=['file_db', 'utils']),
    install_requires=[
        'pandas>=2.2.3',
        'pyarrow>=18.1.0',
        'numpy>=1.26.2'
    ]
)