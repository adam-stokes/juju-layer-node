import sys
from subprocess import Popen, PIPE

from charms.reactive import (
    hook,
    set_state,
    is_state,
    remove_state,
    main
)

from charmhelpers.core import hookenv
from charmhelpers.fetch import (
    apt_install
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
    }
}


@hook('install')
def install():
    if is_state('nodejs.installed'):
        return

    hookenv.status_set('maintenance',
                       'Installing Node.js {}'.format(config['node-version']))

    if config['node-version'] not in ['0.12', '0.10', '4.x']:
        status_msg = ('Unknown Node.js version specified: {}'.format(
            config['node-version']))

        hookenv.status_set('error', status_msg)
        hookenv.log(status_msg, 'error')
        remove_state('nodejs.installed')
        sys.exit(1)

    url = node_version_map[config['node-version']]['remote']
    hookenv.status_set('maintenance',
                       'Installing Node.js: {}'.format(url))
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

    apt_install(['nodejs'])
    hookenv.status_set('maintenance', 'Installing Node.js completed.')

    hookenv.status_set('active', 'ready')
    set_state('nodejs.installed')

if __name__ == "__main__":
    main()
