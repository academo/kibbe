# Setting up development

Note: Everything in this readme and project assumes python 3

## Requirements

- Install python3
- Install [pip](https://pip.pypa.io/en/stable/installing/sure)
- Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) `pip install virtualenv` or `sudo apt install python3-virtualenv`
- Install make: `sudo apt install make` (linux). `xcode-select --install` (mac)

Note: In macos is probable you have to run pip using sudo depending on your setup

## Setup

- Clone this repo
- Setup and activate the virtualenv
- Install the project dependencies

> Note: **Do not use sudo for any of the following commands**

### Run make setup to setup dependencies
```bash
make setup
```

### Activate the virtualenv for the project

Inside the project:

```bash
. env/bin/activate
```

When you are done with development you can deactivate the venv with 

```bash
deactivate
```

You should now be able to run `kibbe` in your terminal.


## Run

To run the tool

```bash
python3 kibbe.py
```

or simply

```bash
./kibbe.py
```

## Linting and formatting

This project uses autopep8 and flake8 for formatting and linting. Make sure your editor has these tools installed and running.