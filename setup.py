import subprocess
from setuptools import setup, find_packages

# takes the version from the latest current tag
version = subprocess.getoutput('git describe --tags --abbrev=0')[1:]

setup(
    name='kibbe',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    download_url='https://github.com/academo/kibbe/releases',
    url='https://github.com/academo/kibbe/',
    author="Esteban Beltran",
    author_email="kibbe@academo.me",
    install_requires=['click', 'termcolor'],
    entry_points={
        'console_scripts': [
            'kibbe = src.main:cli',
        ],
    },
)
