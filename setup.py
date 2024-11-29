from setuptools import setup, find_packages

setup(
    name='bingle',
    version='0.1.1',
    author='junhee',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.3',
        'pyarrow>=18.1.0',
        'numpy>=1.26.2'
    ]
)
