#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Dict, Union
import pytz


class Config:
    """ Babel configuration """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
# uncomment the following line and @babel.localeselector for checker
babel = Babel(app)
# babel = Babel(app, locale_selector=get_locale,
#               timezone_selector=get_timezone)
app.config.from_object(Config)
app.url_map.strict_slashes = False


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """ Get locale from request with the priority:
        1. URL parameter
        2. User setting
        3. Request header
        4. Application configuration (default)
    """
    locale_order = [request.args, g.user, request.headers, app.config]
    for source in locale_order:
        if source is None:
            continue
        locale = source.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """ Get timezone from request with the priority:
        1. URL parameter
        2. User setting
        3. Application configuration (default)
    """
    timezone_order = [request.args, g.user, app.config]
    for source in timezone_order:
        if source is None:
            continue
        timezone = source.get('timezone')
        if timezone:
            try:
                print(pytz.timezone(timezone).zone)
                return pytz.timezone(timezone).zone
            except pytz.exceptions.UnknownTimeZoneError:
                break
    return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user() -> Union[Dict, None]:
    """ returns a user dict or None if id cannot be found """
    try:
        id = request.args.get('login_as')
        return users[int(id)] if id else None
    except (ValueError, TypeError, KeyError):
        return None


@app.before_request
def before_request() -> None:
    """ Performs user initialization Before request """
    g.user = get_user()


@app.route('/')
def helloWorld() -> str:
    """ Home page """
    g.time = format_datetime()
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
