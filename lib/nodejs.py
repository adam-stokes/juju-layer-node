import shlex
import os
import sys
from collections import deque
import subprocess

from charmhelpers.core import hookenv
from charms.reactive import (
    set_state,
    remove_state
)


def node_dist_dir():
    """ Absolute path of Node.js application dir

    Returns:
    Absolute string of node application directory
    """
    config = hookenv.config()
    return os.path.join(hookenv.charm_dir(), config['node-application-dir'])


def node_switch(ver):
    """ Switches installed version of Node.js

    Arguments:
    ver: Version string of Node.js (0.10, 0.12, 4.x)
    """
    config = hookenv.config()
    if config['node-version'] not in ['0.12', '0.10', '4.x']:
        status_msg = ('Unknown Node.js version specified: {}'.format(
            config['node-version']))

        hookenv.status_set('blocked', status_msg)
        hookenv.log(status_msg, 'error')
        remove_state('nodejs.install_runtime')
        sys.exit(1)
    config['node-version'] = ver
    set_state('nodejs.install_runtime')


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
