# About

![image](https://user-images.githubusercontent.com/227916/125775833-cb2ceb2a-07bd-4eea-888b-ba05c3b41f0c.png)

kibbe is a cli tool to ease common tasks when developing plugins for kibana.

## Features

* Run elasticsearch for kibana with persistent configuration across clones
* Run kibana with persistent configuration across clones
* Run fast checks for your code before committing
* Discover tools and helpers you might not know
* More coming: [open an issue](https://github.com/academo/kibbe/issues/new) with your suggestions

> *Use `--help` when running kibbe to know more about its features*

# Installing

There are 3 ways to install kibbe:

* via PIP (recommended) `pip install kibbe --upgrade`
* Downloading the binary
* Building it

## Via PIP

The easiest way to install and keep kibbe up to date is by using pip.

- Make sure you have python3 installed
- Install [pip](https://pip.pypa.io/en/stable/installing/) (you probably don't have to)

Install kibbe:

`pip3 install kibbe`

To upgrade

`pip install kibbe --upgrade`

Note: It might be possible you need to run pip with sudo in mac.

## Download the binary

- Download the [latest release](https://github.com/academo/kibbe/releases) from this repository.
- Give it running permissions `chmod +x kibbe`
- Add it to your path (e.g. `cp kibbe .local/bin`)

MacOS users dowloading the release [see this](docs/mac_issue.md)

## Building it yourself

You can build kibbe yourself, follow the instructions in the [contributing](CONTRIBUTING.md) guide.

# Usage

Always run `kibbe` in the root of your kibana clone.

Run `kibbe --help` to see a list of commands.

you can run `--help` on any subcommand to get more information about arguments, options and what subcommands do.

e.g.:

`kibbe check --help`

## Configuration file

Create a configuration file in your home `~/.kibbe`

Some kibbe subcommands can use persistent parameters from a configuration file.

The configuration file is read from ~/.kibbe and it should follow the format in [the configuration file example](https://github.com/academo/kibbe/blob/master/kibbe-conf-example)

# Contributing

Follow the [contributing guide](CONTRIBUTING.md)