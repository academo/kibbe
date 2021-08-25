
# About

![Peek 2021-08-23 13-40](https://user-images.githubusercontent.com/227916/130441509-cf3f2f57-54a0-43fb-8b22-30f1e1725935.gif)

kibbe is a cli tool to ease common tasks when developing plugins for kibana.

## Features

* Run elasticsearch for kibana with persistent configuration across clones
* Run kibana with persistent configuration across clones
* Run elasticsearch and kibana in a tmux session automated
* Run fast checks for your code before committing
* Manage git worktree paths
* Custom configuration across kibana clones or git worktrees
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

Create a configuration file in your home `~/.kibberc` or you can create it directly on your kibana
clone/worktree with a `.kibberc` file. (make sure to add it to your git ignore)

Some kibbe subcommands can use persistent parameters from a configuration file.

The configuration file should follow the format in [the configuration file example](https://github.com/academo/kibbe/blob/master/kibbe-conf-example)

### Custom configuration files

you can generate custom configurations files with kibbe. If you specify a section in the configuration file prefixed with `file-[name]` it will
create a `[name]` file on the current kibana clone and put the content on it (see the configuration file example)

This is very useful when you work with git worktrees.

Note: kibbe only supports top-level configuration files

## Context manager

Kibbe makes use of [git worktrees](https://git-scm.com/docs/git-worktree) to manage "contexts". Kibbe adds some easy to use commands
to switch between git worktrees without having to worry about remembering paths or all git worktree parameters.

If you use a `~/.kibberc` configuration file, kibbe will pick it up to run elastic and kibana so you don't need to re-configure your elastic, kibana or
other configuration files in your git worktrees. This make it easier to keep the same configuration across all your worktrees.

If you want to have a custom configuration on an specific worktree you can create a `.kibberc` in that worktree and kibbe will pick up and merge
with the main configuration

## Terminal Autocomplete

Kibbe offers autocomplete for some of its commands. you can enable it depending on your terminal by adding this to your
configuration dotfile:


### ZSH: Add to `~/.zshrc`  (default in Macos)
`eval "$(_KIBBE_COMPLETE=zsh_source kibbe)"`


### BASH Add to `~/.bashrc`
`eval "$(_KIBBE_COMPLETE=bash_source kibbe)"`

## Tmux integration

Kibbe can integrate with tmux to quickly run elasticsearch and kibana. Simply run kibbe inside an existing tmux window.

You can know more about tmux [in this article](https://linuxize.com/post/getting-started-with-tmux/)

### Tmux and iterm2

Tmux and iterm2 have a [special integration](https://iterm2.com/documentation-tmux-integration.html). When you start your tmux session you can pass the `-CC` option and that will make tmux panels and windows turn into native iterm tabs and splits. Kibbe will work just as fine with it.

With mac and iterm2 run tmux like this:
```bash
tmux -CC
```

# Contributing

Follow the [contributing guide](CONTRIBUTING.md)
