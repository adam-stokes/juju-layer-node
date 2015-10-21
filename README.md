# layer-node
> Juju charms.reactive layer for NodeJS

# emitters

**nodejs.installed** - This state is emitted once Node.js has been installed.
Rely on this state to perform an application deployment when Node.js is ready
to be used.

# api

All helper modules are found in `lib/nodejs.py`

Example,

```

from nodejs import npm, node_dist_dir

print(node_dist_dir())
# /var/lib/juju/agents/unit-node-0/charm/dist

@when('nodejs.installed')
def install_deps():
    npm('install')

@when('<app>.installed')
def run_tests():
   npm('test')
   npm('run build')
```

# license

The MIT License (MIT)

Copyright (c) 2015 Adam Stokes <adam.stokes@ubuntu.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
