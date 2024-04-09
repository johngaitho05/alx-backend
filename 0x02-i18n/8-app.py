#!/usr/bin/env python3
""" Basic Flask app- to get locale from request"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from datetime import datetime


class Config(object):
    """ Config class for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(login_as: int) -> dict:
    """Get user from dict"""
    return users.get(login_as, None)


@app.before_request
def before_request():
    """Performs actions before request"""
    login_as = request.args.get('login_as')
    g.user = get_user(int(login_as)) if login_as else None


@babel.localeselector
def get_locale() -> str:
    """Check if 'locale' parameter is in the request and is a
    supported locale
    """
    if 'locale' in request.args and \
            request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']

    """Locale from user settings"""
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']

    """Locale from request header"""
    if request.accept_languages:
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    """Default locale"""
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone() -> str:
    """Check if 'timezone' parameter is in the request and is a
    valid time zone
    """
    if 'timezone' in request.args:
        try:
            pytz.timezone(request.args['timezone'])
            return request.args['timezone']
        except pytz.UnknownTimeZoneError:
            pass

    """Time zone from user settings"""
    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.UnknownTimeZoneError:
            pass

    """Default to UTC"""
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def get_index() -> str:
    """ GET /
    Return:
        - template 8-index.html
    """
    return render_template('8-index.html', user=g.user)


def get_current_time(user):
    """Get the current time based on user's time zone"""
    if user and user.get('timezone'):
        try:
            timezone = pytz.timezone(user['timezone'])
            localized_time = datetime.now(
                timezone).strftime("%b %d, %Y, %I:%M:%S %p")
            return localized_time
        except pytz.UnknownTimeZoneError:
            pass

    """Default to UTC if no valid time zone is found"""
    return datetime.utcnow().strftime("%b %d, %Y, %I:%M:%S %p")


if __name__ == "__main__":
    app.debug = True
    """Enable debug mode"""
    app.run(host="0.0.0.0", port="5000")
