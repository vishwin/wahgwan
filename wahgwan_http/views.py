# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import render_template, Response, abort, send_file
import pkg_resources
from slimit import minify
from wahgwan_http import app, cache

@app.route('/static/css/<css>.css')
def send_css(css):
	return send_file(pkg_resources.resource_filename('wahgwan_http', 'generated/css/' + css + '.scss.css'), mimetype='text/css')

@app.route('/static/fonts/<fontfile>')
def fontawesome_file(fontfile):
	return send_file(pkg_resources.resource_filename('wahgwan_http', 'Font-Awesome/fonts/' + fontfile))

@app.route('/static/js/<js>')
def render_js(js):
	try:
		out=cache.get(js)
		if out is None:
			fd=open(pkg_resources.resource_filename('wahgwan_http', 'js/' + js), encoding='UTF-8')
			out=minify(fd.read(), mangle=True, mangle_toplevel=True)
			fd.close()
			cache.set(js, out)
		return Response(response=out, mimetype='text/javascript')
	except OSError:
		abort(404)

@app.route('/static/js/vendor/foundation.js')
def send_foundation_js():
	return send_file(pkg_resources.resource_filename('wahgwan_http', 'node_modules/foundation-sites/dist/js/foundation.min.js'), mimetype='text/javascript')

@app.route('/static/js/vendor/jquery.js')
def send_jquery_js():
	return send_file(pkg_resources.resource_filename('wahgwan_http', 'node_modules/foundation-sites/vendor/jquery/dist/jquery.min.js'), mimetype='text/javascript')

@app.route('/')
def index():
	return render_template('index.html')
