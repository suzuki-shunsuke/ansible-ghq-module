# ansible-ghq-module

[![Build Status](https://travis-ci.org/suzuki-shunsuke/ansible-ghq-module.svg?branch=master)](https://travis-ci.org/suzuki-shunsuke/ansible-ghq-module)

Manage remote repository with the [motemen/ghq](https://github.com/motemen/ghq).
Although this is distributed in the Ansible Galaxy,
this is not an Ansible role but an Ansible Module and Action Plugin.

https://galaxy.ansible.com/suzuki-shunsuke/ghq-module/

## Notice

* This module doesn't support the check mode.

## Requirements

* Go
* motemen/ghq

## Install

This module is distributed in the Ansible Galaxy.
So you can install this with tha `ansible-galaxy` command.

```
$ ansible-galaxy install suzuki-shunsuke.ghq-module
```

```yaml
# playbook.yml

- hosts: default
  roles:
  # After you call this module, you can use this
  - suzuki-shunsuke.ghq-module
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
# Empty lines and started with sharp("#") lines are ignored
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

### Requirements

* Vagrant
* Ansible

### Setup test

```
$ cd tests
$ ansible-galaxy install -r roles.yml
```

### Test in Vagrant Provisioning

```
$ cd tests
$ vagrant up --provision-with=ansible
$ vagrant up --provision-with=ansible_local
```

### Test in localhost

```
$ ansible-playbook test.yml
```
