from setuptools import setup, find_packages

setup(
	name='wahgwan-http',
	version='17.10.29',
	description='The wahgwan.xyz HTTP interface',
	url='https://git.vishwin.info/site/wahgwan.git/',
	author='Charlie Li',
	license='MPL-2.0',
	packages=find_packages(),
	install_requires=['Flask', 'markdown', 'slimit', 'pylibmc', 'Pillow', 'exifread', 'cairosvg'],
	setup_requires=['libsass>=0.6.0'],
	sass_manifests={'wahgwan_http': ('scss', 'generated/css', 'static/css')},
	include_package_data=True,
	zip_safe=False
)
