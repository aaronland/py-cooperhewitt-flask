# py-cooperhewitt-flask

Cooper Hewitt utility functions for Flask applications.

## cooperhewitt.flask.http_pony

The most important thing to remember about things in this class is that they are utility functions. They simply wrap some of the boilerplate tasks required to set up a Flask application.

### setup_flask_app(name)

Creates a default `Flask` app object, validates and sets the application name
and invokes the `werkzeug.contrib.fixers.ProxyFix` method.

It also sets a `before_first_request` callback to ensure that if the application
was started without an explicit config file pointer on the command line then the
application's settings will be loaded from a file defined in the `app_name` +
`_CONFIG` environment variable.

### get_upload_path(app, key='file')

Create a temporary file and return a sanitized filename derived from the POST parameter `key`.

Temp files are written to the `http_pony.upload_path_root` directory as defined
in your config file.

### get_local_path(app)

Returns a sanitized filename derived from the GET parameter `key`.

Files must exist and must be parented by the directory defined by the 
`http_pony.local_path_root` setting in your config file.

### run_from_cli(app)

Parses command line arguments to load a `ini` style config file and update your
app's settings accordingly.

### Example

	# Let's pretend this file is called 'example-server.py'
	import cooperhewitt.flask.http_pony as http_pony

	app = http_pony.setup_flask_app('EXAMPLE_SERVER')

	@app.route('/example', methods=['GET', 'POST'])
	def example():

	    try:
	        if flask.request.method=='POST':
        	    path = http_pony.get_upload_path(app)
	        else:
        	    path = http_pony.get_local_path(app)

	    except Exception, e:
        	logging.error(e)
	        flask.abort(400)

	    # carry on and do something with path here

	if __name__ == '__main__':

	    http_pony.run_from_cli(app)

And then 

	$> python example-server.py -c example-server.cfg

## Config

The following settings should be added to a standard [ini style configutation
file](https://en.wikipedia.org/wiki/INI_file).

### [flask]

#### port

The TCP port you want your Flask server to listen on.

### [http_pony]

#### local_path_root

Used by the `get_local_path` function. If set then files sent using an `HTTP
GET` parameter will be limited to only those that are are parented by this
directory. 

If it is not set then `HTTP GET` requests will fail.

#### upload_path_root

Used by the `get_upload_path` function. If set then files sent as an `HTTP POST`
request will be first written to this directory before processing.

If not set then the operating system's temporary directory will be used.

#### allowed_extensions

A comma-separate list of valid file extensions for processing.

Used by the `get_local_path` and `get_upload_path` functions to ensure that
filenames have a specific extension.
	
## See also

* http://flask.pocoo.org/
