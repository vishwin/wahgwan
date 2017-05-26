# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import render_template, Response, abort, send_file
import pkg_resources
from wahgwan_http import app, cache

from slimit import minify
from mimetypes import guess_type
import os.path
from PIL import Image
import xml.etree.ElementTree as ET
from cairosvg import svg2png

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

@app.route('/static/img/<imgfile>')
def return_img(imgfile):
	imgpath=pkg_resources.resource_filename('wahgwan_http', 'img/' + imgfile)
	try:
		return send_file(imgpath, mimetype=guess_type(imgpath)[0])
	except OSError:
		abort(404)

@app.route('/static/img/<width>px-<svgfile>.svg.png')
def svg_thumb(width, svgfile):
	try:
		imgpath=pkg_resources.resource_filename('wahgwan_http', 'img/' + svgfile + '.svg')
		thumbfile=width + 'px-' + svgfile + '.svg.png'
		thumbpath=pkg_resources.resource_filename('wahgwan_http', 'generated/thumb/' + thumbfile)
		# get file modified time for original; will throw exception if not found
		mtime_orig=os.path.getmtime(imgpath)
		if not (os.path.isfile(thumbpath)) or (os.path.getmtime(thumbpath) < mtime_orig):
			width_orig=float(ET.parse(imgpath).getroot().get('width'))
			svg2png(url=imgpath, write_to=thumbpath, scale=(int(width) / width_orig))
		return send_file(thumbpath, mimetype='image/png')
	except OSError:
		abort(404)

@app.route('/static/img/<width>px-<imgfile>')
def render_thumb(width, imgfile):
	try:
		imgpath=pkg_resources.resource_filename('wahgwan_http', 'img/' + imgfile)
		# if original image does not exist, immediately 404
		img=Image.open(imgpath)
		imgformat=img.format
		thumbfile=width + 'px-' + imgfile
		thumbpath=pkg_resources.resource_filename('wahgwan_http', 'generated/thumb/' + thumbfile)
		mtime_orig=os.path.getmtime(imgpath)
		if not (os.path.isfile(thumbpath)) or (os.path.getmtime(thumbpath) < mtime_orig):
			img.thumbnail((int(width), int(width) / (img.width / img.height)))
			img.save(thumbpath, imgformat)
		img.close()
		return send_file(thumbpath, mimetype=imgformat)
	except OSError:
		abort(404)

@app.route('/')
def index():
	return render_template('index.html')
