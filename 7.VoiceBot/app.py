

from resources.query_service import QueryService
from flask_restful import Api, Resource, reqparse
from flask import Flask, render_template, send_from_directory


app = Flask(__name__)
api = Api(app)
api.add_resource(QueryService, '/news_urls')


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    from os import path
    return send_from_directory(path.join(app.root_path, "static"), "favicon.ico", mimetype = "image/vnd.microsoft.icon")


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    try:
        app.run('localhost', port = 5000, debug = True, use_reloader = False)
    except Exception, e:
        print e
