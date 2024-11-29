from setuptools import setup, find_packages

setup(
    name='bingle_utils',
    version='0.1.0',
    author='junhee',
    packages=find_packages(include=['file_db', 'utils']),
    install_requires=[
        'pandas>=2.2.3',
        'pyarrow>=18.1.0',
        'numpy>=1.26.2'
    ]
)