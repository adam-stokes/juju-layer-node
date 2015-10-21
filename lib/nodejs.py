import shlex
import os
import sys
from collections import deque
import subprocess

from charmhelpers.core import hookenv


def node_dist_dir():
    """ Absolute path of Node.js application dir

    Returns:
    Absolute string of node application directory
    """
    config = hookenv.config()
    return os.path.join(hookenv.charm_dir(), config['node-application-dir'])


def npm(cmd):
    """ Runs npm

    This layer relies on the use of npm scripts defined in `package.json`,
    see here https://docs.npmjs.com/misc/scripts for more information.

    Usage:

       npm('install')
       npm('run build')

    Arguments:
    cmd: Command to run can be string or list

    Returns:
    Will halt on error
    """
    hookenv.status_set('maintenance', 'Installing NPM dependencies')
    os.chdir(node_dist_dir())
    if isinstance(cmd, str):
        cmd = deque(shlex.split(cmd))
    else:
        cmd = deque(cmd)
    cmd.appendleft('npm')
    try:
        subprocess.check_call(cmd)
        os.chdir(os.getenv('CHARM_DIR'))
    except subprocess.CalledProcessError as e:
        hookenv.status_set("blocked", "NPM error: {}".format(e))
        sys.exit(1)
