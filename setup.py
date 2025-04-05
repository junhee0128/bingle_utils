from setuptools import setup, find_packages

setup(
    name='bingle',
    version='0.1.8',
    author='junhee',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'bingle': ['ai_caller/api_spec/*.json']
    },
    include_package_data=True,
    install_requires=[
        'pandas>=2.2.3',
        'pyarrow>=19.0.1',
        'numpy>=2.2.4',
        'requests>=2.32.3',
        'natsort>=8.4.0',
        'tenacity>=9.0.0',
        'python-docx>=1.1.2'
    ]
)
