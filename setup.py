from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='kibbe',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    download_url='https://github.com/academo/kibbe/releases',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'kibbe = src.main:cli',
        ],
    },
)
