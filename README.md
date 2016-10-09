# ansible-ghq-module

[![Build Status](https://travis-ci.org/suzuki-shunsuke/ansible-ghq-module.svg?branch=master)](https://travis-ci.org/suzuki-shunsuke/ansible-ghq-module)

Manage remote repository with [motemen/ghq](https://github.com/motemen/ghq).

## Notice

* This module doesn't support the check mode.
* If this module succeeds, the result's changed attribute is always true.

## Requirements

* Go
* motemen/ghq

## Install

In the following example this module is installed in ~/ansible/modules directory.

```
$ mkdir -p ~/ansible/modules
$ export ANSIBLE_LIBRARY=~/ansible/modules
$ git clone suzuki-shunsuke/ansible-ghq-module ~/ansible/modules/ansible-ghq-module
```

## Options

parameter | required | default | choices | comments
--- | --- | --- | --- | ---
name | no | | | The repository path
executable | no | | | The executable path of ghq command
root | no | | | The environment variable GHQ_ROOT
update | no | no | bool | If yes, the -u option is added
ssh | no | no | bool | If yes, the -p option is added
shallow | no | no | bool | If yes, the -shallow option is added
src | no | | | The source path of "ghq import" command
subcommand | no | get | get | The subcommand of "ghq import" command

## Example

```yaml
# Clone suzuki-shunsuke/zsh.conf
ghq:
  name: suzuki-shunsuke/zsh.conf

# Specify the path of ghq command
ghq:
  name: suzuki-shunsuke/zsh.conf
  executable: {{ ansible_env.HOME }}/.go/bin/ghq

# Update
go:
  name: suzuki-shunsuke/zsh.conf
  update: yes

# Via ssh
ghq:
  name: suzuki-shunsuke/zsh.conf
  ssh: yes

# Specify the ghq.root
ghq:
  name: suzuki-shunsuke/zsh.conf
  root: {{ ansible_env.HOME }}/.repos

# Shallow clone
ghq:
  name: suzuki-shunsuke/zsh.conf
  shallow: yes

# Import from file
ghq:
  src: repos.txt

# Import via subcommand
ghq:
  subcommand: starred motemen

# Subcommand is either str or list of str
ghq:
  subcommand: ["starred", "motemen"]
```

## Licence

MIT

## For developers

### Local Test with Vagrant

```
$ sh _setup.sh
$ export ANSIBLE_LIBRARY=$PWD:$ANSIBLE_LIBRARY  # if you use direnv, it is automatically set.
$ vagrant up --provision
```
