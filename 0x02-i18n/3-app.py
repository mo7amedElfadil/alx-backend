#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """ Babel configuration """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# @babel.localeselector
def get_locale() -> str:
    """ Get locale from request """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


app = Flask(__name__)
# uncomment the following line and @babel.localeselector for checker
# babel = Babel(app)
babel = Babel(app, locale_selector=get_locale)
app.config.from_object(Config)
app.url_map.strict_slashes = False


@app.route('/', strict_slashes=False)
def helloWorld() -> str:
    """ Home page for the Flask app
    """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(debug=True)
