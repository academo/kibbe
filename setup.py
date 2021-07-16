from setuptools import setup, find_packages

setup(
    name="kibbe",
    packages=find_packages(),
    include_package_data=True,
    download_url="https://github.com/academo/kibbe/releases",
    url="https://github.com/academo/kibbe/",
    author="Esteban Beltran",
    author_email="kibbe@academo.me",
    install_requires=["click", "termcolor", "libtmux", "requests"],
    entry_points={
        "console_scripts": [
            "kibbe = src.main:cli",
        ],
    },
)
