import sys
from subprocess import check_output

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
    if is_state('node.installed') and not is_state('node.upgrade'):
        return

    hookenv.status_set('maintenance',
                       'Installing Node.js {}'.format(config['node-version']))

    if config['node-version'] not in ['0.12', '0.10', '4.x']:
        status_msg = ('Unknown Node.js version specified: {}'.format(
            config['node-version']))

        hookenv.status_set('maintenance', status_msg)
        hookenv.log('ERROR', status_msg)
        remove_state('node.installed')
        sys.exit(1)

        try:
            hookenv.status_set('maintenance', 'Installing Node.js')
            url = node_version_map[config['node-version']]
            cmd = ['curl -sL {} | bash -e'.format(url)]
            check_output(cmd)
            apt_install(['nodejs'])
        except:
            status_msg = ('Problem install Node.js')
            hookenv.status_set('maintenance', status_msg)
            hookenv.log('ERROR', status_msg)
        hookenv.status_set('active', 'ready')
        set_state('node.installed')

if __name__ == "__main__":
    main()
