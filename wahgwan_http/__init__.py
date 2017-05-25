# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from werkzeug.contrib.cache import MemcachedCache

app=Flask(__name__)
app.config.from_pyfile('config.py')

# set up a memcached Werkzeug cache, prefixing each key, with adjustable timeout
cache=MemcachedCache(servers=app.config['MEMCACHED_SERVERS'], key_prefix=app.config['MEMCACHED_KEYPREFIX'], default_timeout=app.config['MEMCACHED_TIMEOUT'])

import wahgwan_http.views
