import os.path
import base64
import tempfile
import logging
import ConfigParser

import flask
import werkzeug
import werkzeug.security
from werkzeug.contrib.fixers import ProxyFix

# not tested

def setup_flask_app(name):

    app = flask.Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    def before_first():

        try:

            if app.config.get('HTTP_PONY_INIT', None):
                return True

            if os.environ.get("PALETTE_SERVER_CONFIG"):
            
                cfg = os.environ.get("PALETTE_SERVER_CONFIG")
                cfg = update_app_config_from_file(app, cfg)

                return True

        except Exception, e:

            logging.error("failed to load config file, because %s" % e)
            flask.abort(500)

        logging.error("missing config file")
        flask.abort(500)

    app.before_first_request(before_first)
    return app

def update_app_config_from_file(app, file):

    cfg = ConfigParser.ConfigParser()
    cfg.read(file)
    
    update_app_config(app, cfg)
    return cfg

def update_app_config(app, cfg):

    update = {}

    for k, v in cfg.items('http_pony'):

        k = "HTTP_PONY_%s" % k.upper()
        update[k] = v

    update['HTTP_PONY_INIT'] = True
    app.config.update(**update)

def get_local_path(app, key='file'):

    path = flask.request.args.get(key)
    logging.debug("request path is %s" % path)

    if not path:
        raise Exception, "there's nothing to process"

    root = app.config.get('HTTP_PONY_LOCAL_PATH_ROOT', None)
    logging.debug("image root is %s" % root)

    if not root:
        raise Exception, "image root is not defined"


    if root:

        safe = werkzeug.security.safe_join(root, path)

        if not safe:
            raise Exception, "'%s' + '%s' considered harmful" % (root, path)

        path = safe

    logging.debug("final request path is %s" % path)
    
    if not os.path.exists(path):
        raise Exception, "%s does not exist" % path

    return path

def get_upload_path(app, key='file'):

    file = flask.request.files[key]

    if file and allowed_file(app, file.filename):

        root = app.config.get('HTTP_PONY_UPLOAD_PATH_ROOT', None)

        if not root:
            root = tempfile.gettempdir()

        rand = base64.urlsafe_b64encode(os.urandom(12))
        secure = werkzeug.secure_filename(file.filename)
        fname = "http-pony-%s-%s" % (rand, secure)

        safe = werkzeug.security.safe_join(root, fname)

        if not safe:
            e = "'%s' + '%s' considered harmful" % (root, fname)
            raise Exception, e

        logging.debug("save upload to %s" % safe)

        file.save(safe)
        return safe

    raise Exception, "Missing or invalid file"

def allowed_file(app, filename):

    allowed = app.config.get('HTTP_PONY_ALLOWED_EXTENSIONS', '')
    allowed = allowed.split(',')

    return '.' in filename and filename.rsplit('.', 1)[1] in allowed
