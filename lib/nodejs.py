import os
import sys
from shell import shell

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
    if not isinstance(cmd, str):
        hookenv.status_set('blocked', '{}: should be a string'.format(cmd))
        sys.exit(0)
    os.chdir(os.getenv('CHARM_DIR'))
    cmd = ("npm {}".format(cmd))
    sh = shell(cmd)
    if sh.code > 0:
        hookenv.status_set("blocked", "NPM error: {}".format(sh.errors()))
        sys.exit(0)
