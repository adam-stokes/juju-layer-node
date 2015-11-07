import os
import sys
from subprocess import Popen, PIPE
from shell import shell

from charms.reactive import (
    hook,
    set_state,
    remove_state,
    main
)

from charmhelpers.core import hookenv
from charmhelpers.fetch import (
    apt_install,
    apt_purge
)

config = hookenv.config()
node_version_map = {
    '0.10': {
        'remote': 'https://deb.nodesource.com/setup_0.10'
    },
    '0.12': {
        'remote': 'https://deb.nodesource.com/setup_0.12'
    },
    '4.x': {
        'remote': 'https://deb.nodesource.com/setup_4.x'
    },
    '5.x': {
        'remote': 'https://deb.nodesource.com/setup_5.x'
    }
}


@hook('install')
def install_nodejs():
    """ Installs defined node runtime

    You should use node_switch('version') to make use of this reactor.

    Emits:
    nodejs.available: Emitted once the runtime has been installed
    """
    remove_state('nodejs.available')
    hookenv.status_set('maintenance',
                       'Installing Node.js {}'.format(config['node-version']))

    if os.path.isfile('/etc/apt/sources.list.d/nodesource.list'):
        os.remove('/etc/apt/sources.list.d/nodesource.list')

    url = node_version_map[config['node-version']]['remote']
    hookenv.status_set('maintenance',
                       'Using Node.js Repo: {}'.format(url))
    try:
        curl_cmd = ['curl', '-sl', url]
        bash_cmd = ['bash', '-e']
        pipe1 = Popen(curl_cmd, stdout=PIPE)
        pipe2 = Popen(bash_cmd, stdin=pipe1.stdout, stdout=PIPE)
        pipe1.stdout.close()
        output = pipe2.communicate()[0]
        hookenv.log('Added nodesource archive, output: {}'.format(output),
                    'debug')
    except:
        hookenv.log('Problem installing: {}'.format(output),
                    'debug')
        sys.exit(1)

    apt_purge(['nodejs'])
    shell('apt-get install -qy nodejs')
    hookenv.status_set('maintenance', 'Installing Node.js completed.')

    hookenv.status_set('active', 'Node.js is ready!')
    set_state('nodejs.available')


if __name__ == "__main__":
    main()
