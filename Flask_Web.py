from flask import Flask
from flask_wtf import CSRFProtect
from app.cms import bp as cms_bp
from app.front import bp as front_bp
from app.common import bp as common_bp
import config
from exts import db, mail, alidayu
from utils.captcha import Captcha


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)

    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    alidayu.init_app(app)

    return app


# Captcha.gene_graph_captcha()

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)
