import shlex
import os
import subprocess

from charmhelpers.core import hookenv


def node_dist_dir():
    """ Absolute path of Node.js application dir
    """
    config = hookenv.config()
    return os.path.join(hookenv.charm_dir(), config['node-application-dir'])


def npm(cmd):
    """ Runs npm

    This layer relies on the use of npm scripts defined in `package.json`,
    see here https://docs.npmjs.com/misc/scripts for more information.

    :param str cmd: Command to run can be string or list
    :rtype bool: Returns True/False of npm execution status
    """
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    return subprocess.call(cmd) == 0
