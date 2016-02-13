import os
import sys

from shell import shell

from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import storage_get
from charmhelpers.core.hookenv import storage_list


def node_dist_dir():
    """ Absolute path of Node.js application dir

    Returns:
    Absolute string of node application directory
    """
    storage_id = storage_list('app')[0]
    return storage_get('location', storage_id)


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
    status_set(
        'maintenance',
        'installing NPM dependencies for {}'.format(node_dist_dir()))
    os.chdir(node_dist_dir())
    if not isinstance(cmd, str):
        status_set('blocked', '{}: should be a string'.format(cmd))
        sys.exit(0)
    cmd = ("npm {}".format(cmd))
    sh = shell(cmd)
    if sh.code > 0:
        status_set("blocked", "NPM error: {}".format(sh.errors()))
        sys.exit(0)
