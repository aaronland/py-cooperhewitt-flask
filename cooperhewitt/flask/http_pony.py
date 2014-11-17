import sys

import os.path
import base64
import tempfile
import logging

import optparse
import ConfigParser

import flask
import werkzeug
import werkzeug.security
from werkzeug.contrib.fixers import ProxyFix

import re

def validate_app_name(name):

    pattern = re.compile("^[a-zA-Z_]+$")

    if not pattern.match(name):
        raise Exception, "invalid app name"

    return True

def run_from_cli(app):

    parser = optparse.OptionParser()

    parser.add_option("-c", "--config", dest="config", help="", action="store", default=None)
    parser.add_option("-v", "--verbose", dest="verbose", help="enable chatty logging; default is false", action="store_true", default=False)

    opts, args = parser.parse_args()

    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("verbose logging is enabled")
    else:
        logging.basicConfig(level=logging.INFO)

    kwargs = {}

    # if not the os.environ('<APP_NAME>_CONFIG')

    if opts.config:

        cfg = update_app_config_from_file(app, opts.config)

        port = cfg.get('flask', 'port')
        kwargs['port'] = int(port)

    app.run(**kwargs)

def setup_flask_app(name):

    validate_app_name(name)

    app = flask.Flask(name)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    config_flag = "%s_CONFIG" % name.upper()
    init_flag = "HTTP_PONY_INIT"

    """
    if not app.config.get(init_flag, None):

        cfg = os.environ.get(config_flag)

        if not cfg or not os.path.exists(cfg):
            raise Exception, "missing config file"
    """

    def before_first():

        try:

            if app.config.get(init_flag, None):
                return True

            if os.environ.get(config_flag):
            
                cfg = os.environ.get(config_flag)
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
