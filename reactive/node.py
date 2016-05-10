from charms.reactive import (
    hook,
    set_state,
    remove_state,
    main,
    when_not,
    when,
)

from charmhelpers.core import (
    hookenv,
    unitdata,
)

from charms import apt


config = hookenv.config()
kv = unitdata.kv()


@when_not('nodejs.available')
def install_nodejs():
    """ Installs defined node runtime

    Emits:
    nodejs.available: Emitted once the runtime has been installed
    """

    kv.set('nodejs.url', config.get('install_sources'))
    kv.set('nodejs.key', config.get('install_keys'))

    apt.queue_install(['nodejs', 'npm'])


@when('apt.installed.nodejs')
@when_not('nodejs.available')
def node_js_ready():
    hookenv.status_set('active', 'node.js is ready')
    set_state('nodejs.available')


@hook('config-changed')
def version_check():
    url = config.get('install_sources')
    key = config.get('install_keys')

    if url != kv.get('nodejs.url') or key != kv.get('nodejs.key'):
        apt.purge(['nodejs'])
        remove_state('nodejs.available')


if __name__ == "__main__":
    main()
