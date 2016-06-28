import sys

from subprocess import Popen, PIPE

from charmhelpers.core import hookenv
from charmhelpers.core import host


def node_dist_dir():
    """ Absolute path of Node.js application dir

    Returns:
    Absolute string of node application directory
    """
    storage_id = hookenv.storage_list('app')[0]
    return hookenv.storage_get('location', storage_id)


def npm(*cmd):
    """ Runs npm

    This layer relies on the use of npm scripts defined in `package.json`,
    see here https://docs.npmjs.com/misc/scripts for more information.

    Usage:

       npm('install')
       npm('run', 'build')

    Arguments:
    cmd: Command to run.  The list of all positional args will be passed in
      as the first arg to `subprocess.run`.

    Returns:
    Will halt on error
    """
    dist_dir = node_dist_dir()
    hookenv.status_set(
        'maintenance',
        'installing NPM dependencies for {}'.format(dist_dir))
    with host.chdir(dist_dir):
        with Popen(['npm'] + list(cmd), stderr=PIPE) as process:
            _, errout = process.communicate()
            retcode = process.poll()
    if retcode != 0:
        hookenv.log('NPM error: {}'.format(errout))
        hookenv.status_set("blocked", "NPM error: {}".format(errout))
        sys.exit(0)
