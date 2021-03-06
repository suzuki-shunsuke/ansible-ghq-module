#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

DOCUMENTATION = '''
---
module: ghq
short_description: Manage remote repository with motemen/ghq.
options:
  name:
    description:
    - A repository url.
    required: no
    type: str
  executable:
    description:
      - The executable location for ghq.
    required: no
    type: str
  update:
    description:
      - When this option is yes, the -u option is added.
    required: no
    type: bool
    default: no
  ssh:
    description:
      - When this option is yes, the -p option is added.
    required: no
    type: bool
    default: no
  shallow:
    description:
      - When this option is yes, the -shallow option is added.
    required: no
    type: bool
    default: no
  src:
    description:
      - The source file path of ghq import command.
    required: no
    type: str
  subcommand:
    description:
      - subcommand of ghq import. It includes arguments.
    required: no
    type: str or str[]
requirements:
- go
- motemen/ghq
author: "Suzuki Shunsuke"
'''

EXAMPLES = '''
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
'''

RETURN = '''
'''

from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec={
            "name": {"default": None, "type": "str"},
            "executable": {"default": "ghq", "type": "str"},
            "update": {"default": False, "type": "bool"},
            "ssh": {"default": False, "type": "bool"},
            "shallow": {"default": False, "type": "bool"},
            "src": {"default": None},
            "subcommand": {"default": None},
        },
        add_file_common_args=True
    )
    params = module.params
    name = params["name"]
    executable = params["executable"]
    update = params["update"]
    ssh = params["ssh"]
    shallow = params["shallow"]
    src = params["src"]
    subcommand = params["subcommand"]

    # name and src and subcommand are specified only one and .
    if sum(1 for a in [name, src, subcommand] if a) != 1:
        module.fail_json(msg="name and src and subcommand must be specified only one.")

    # subcommand is either str or list
    if subcommand:
        if not isinstance(subcommand, [str, list]):
            module.fail_json(msg="subcommand must be str or list of str.")
        if isinstance(subcommand, list) and not all(isinstance(s, str) for s in subcommand):
            module.fail_json(msg="subcommand must be str or list of str.")

    options = {}

    cmd = [executable, "get" if name else "import"]
    if update:
        cmd.append("-u")
    if ssh:
        cmd.append("-p")
    if shallow:
        cmd.append("-shallow")

    if name:
        cmd.append(name)
    elif src:
        src = os.path.expanduser(src)
        if not os.path.exists(src):
            module.fail_json(msg="Source {} not found".format(src))
        if not os.access(src, os.R_OK):
            module.fail_json(msg="Source {} not readable".format(src))
        if os.path.isdir(src):
            module.fail_json(msg="Source must be file, not directory")
        with open(src) as r:
            options["data"] = _parse_source(r.read())
    elif subcommand:
        cmd += subcommand if isinstance(subcommand, list) else subcommand.split(" ")

    # module.fail_json(msg=err, cmd=cmd, options=options)
    rc, out, err = module.run_command(cmd, **options)
    if rc:
        module.fail_json(msg=err, stdout=out, cmd=cmd, options=options)
    else:
        module.exit_json(changed=is_changed(out), stdout=out, stderr=err)


def is_line_changed(line):
    return line.startswith("Updating") or "  clone" in line


def is_changed(out):
    return any(is_line_changed(line.strip()) for line in out.split("\n"))


def _filter_line(line):
    return line and not line.startswith("#")


def _parse_source(text):
    return "\n".join(line.strip() for line in text.split("\n") if _filter_line(line.strip()))


if __name__ == '__main__':
    main()
