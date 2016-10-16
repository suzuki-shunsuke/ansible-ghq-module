from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    TRANSFERS_FILES = True


    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if self._play_context.check_mode:
            result["skipped"] = True
            result["msg"] = "check mode not supported for this module"
            return result

        remote_user = task_vars.get("ansible_ssh_user") or self._play_context.remote_user
        if not tmp:
            tmp = self._make_tmp_path(remote_user)
            self._cleanup_remote_tmp = True

        new_module_args = self._task.args.copy()

        src = self._task.args.get("src")
        if src:
            if self._remote_file_exists(src):
                self._remove_tmp_path(tmp)
                return dict(skipped=True, msg=("skipped, since %s exists" % src))

            if self._task._role is not None:
                source = self._loader.path_dwim_relative(self._task._role._role_path, "files", src)
            else:
                source = self._loader.path_dwim_relative(self._loader.get_basedir(), "files", src)

            if not os.path.exists(source):
                return dict(failed=True, msg="Source {} not found".format(source))
            if not os.access(source, os.R_OK):
                return dict(failed=True, msg="Source {} not readable".format(source))
            if os.path.isdir(source):
                return dict(failed=True, msg="Source must be file, not directory")

            # transfer the file to a remote tmp location
            tmp_src = self._connection._shell.join_path(tmp, os.path.basename(source))
            self._transfer_file(source, tmp_src)

            # set file permissions, more permissive when the copy is done as a different user
            self._fixup_perms2((tmp, tmp_src), remote_user, execute=True)
            new_module_args["src"] = tmp_src

        result.update(self._execute_module(module_name="ghq", module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False))
        # clean up after
        self._remove_tmp_path(tmp)

        return result
