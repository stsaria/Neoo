import os
from flask import Flask, request, render_template

class Web:
    _app = Flask(__name__, template_folder=os.path.abspath("templates/main/"), static_folder=os.path.abspath("static/"))
    _app.config['TEMPLATES_AUTO_RELOAD'] = True
    _app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    def run(self, host:str="0.0.0.0", port:int=8080):
        self._app.run(host, port)

    @staticmethod
    @_app.route("/stop")
    def stop():
        os._exit(0)

    @staticmethod
    @_app.route("/")
    def index():
        return render_template("index.html")

    @staticmethod
    @_app.route("/tools")
    def tools():
        return render_template("tools.html")

    @staticmethod
    @_app.route("/toSelfBot", methods=["GET"])
    def toSelfBot():
        return render_template("to.html", port=8081, page=request.args.get("page"))

    @staticmethod
    @_app.route("/toBot", methods=["GET"])
    def toBot():
        return render_template("to.html", port=8082, page=request.args.get("page"))

if __name__ == "__main__":
    Web().run()