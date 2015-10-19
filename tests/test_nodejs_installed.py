import os


class TestNodeJSInstalled:
    def test_node_is_installed(self):
        """ Test to make sure node.js was installed
        """
        assert os.path.isfile('/usr/bin/node')

    def test_npm_is_installed(self):
        """ Test to make sure npm was installed
        """
        assert os.path.isfile('/usr/bin/npm')
