# About
kibbe is a cli tool to ease common tasks when developing plugins for kibana.

# Installing

## Via PIP

The easiest way to install and keep kibbe up to date is by using pip.

- Make sure you have python3 installed
- Install [pip](https://pip.pypa.io/en/stable/installing/sure)

Install kibbe:

`pip3 install kibbe`

To upgrade

`pip install kibbe --upgrade`

Note: It might be possible you need to run pip with sudo in mac.


## Download the binary

- Download the [latest release](https://github.com/academo/kibbe/releases) from this repository.
- Give it running permissions `chmod +x kibbe`
- Add it to your path (e.g. `cp kibbe .local/bin`)

## Running it on MacOs

Kibbe is originally developed in Linux, also build and fully compatible with Mac but the release files are not signed with an apple certificate as they [cost up to 100 dollars](https://developer.apple.com/support/compare-memberships/).

Due to this you, mac will block kibbe from running and you need to grant running permissions to kibbe when you run it for the first time.

You can do this by going to `Preferences -> Security -> General` where you'll see the option to `allow anyway`. Once you allow it to run you can start using it.

![image](https://user-images.githubusercontent.com/227916/125635023-38bd54c9-5105-4301-95b2-55c259378812.png)

Note: It is likely you wil have to do this again for future updates.

## Building it yourself

You can build kibbe yourself, follow the instructions in the "Contributing" section

# Usage

Run `kibbe --help` to see a list of commands.

you can run `--help` on any subcommand to get more information about arguments, options and what subcommands do.

e.g.:

`kibbe check --help`

## Configuration file

Some kibbe subcommands can use persistent parameters from a configuration file.

The configuration file is read from ~/.kibbe and it should follow the format in [the configuration file example](https://github.com/academo/kibbe/blob/master/kibbe-conf-example)

# Contributing - Setting up development

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

## Releasing

To release a new version, you need to push a new incremental tag. That will trigger an auto-build and release.

There's a handy script to automate this process in `scripts/increment-version.sh` and you can use make to invoke it:

Minor release: `make minor-release`
Major release: `make major-relase`
