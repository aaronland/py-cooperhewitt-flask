# py-cooperhewitt-flask

Cooper Hewitt utility functions for Flask applications.

## cooperhewitt.flask.http_pony

The most important thing to remember about things in this class is that they are utility functions. They simply wrap some of the boilerplate tasks required to set up a Flask application.

### setup_flask_app(name)

### get_upload_path(app, key='file')

### get_local_path(app)

### run_from_cli(app)

### Example

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
	
## See also
