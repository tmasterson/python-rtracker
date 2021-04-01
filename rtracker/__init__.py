import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'equipment.db'),
            REPORT_PATH=os.path.join(app.instance_path, 'reports'),
            )
    if test_config is None:
        # load normal config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config
        app.config.from_mapping(test_config)

    # Create the instance path is it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Create the rport path if it does not exist.
    try:
        os.makedirs(app.config["REPORT_PATH"])
    except OSError:
        pass
    
    # register the database commands
    from rtracker import db
    db.init_app(app)
    from rtracker import tracker, reports
    app.register_blueprint(tracker.bp)
    app.register_blueprint(reports.bp)
    
    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")
    return app
