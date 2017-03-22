# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import render_template, Response, abort, send_file
from flask_libsass import *
import pkg_resources
from slimit import minify
from wahgwan_http import app, cache

Sass(
	{'app': 'scss/app.scss'},
	app,
	url_path='/static/css',
	include_paths=[pkg_resources.resource_filename('wahgwan_http', 'scss')],
	output_style='compressed'
)

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

@app.route('/')
def index():
	return render_template('index.html')
