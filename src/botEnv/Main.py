import threading, os
from flask import Flask, request, redirect, render_template

from .RaidBot import RaidBot
from ..utils.Logger import Logger

logger:Logger = Logger()
bots:list[RaidBot] = []

class Web:
    _app = Flask(__name__, template_folder=os.path.abspath("templates/bot/"))
    _app.config['TEMPLATES_AUTO_RELOAD'] = True
    _app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    def run(self, host:str="127.0.0.1", port:int=8080):
        self._app.run(host, port)

    @_app.route("/")
    def index(self):
        return render_template("index.html")

    @_app.route("/getLog", methods=["GET"])
    def getLog(self):
        return logger.toStr()

    @_app.route("/stop", methods=["GET"])
    def stop(self):
        [bot.stop() for bot in bots]
        bots.clear()
        logger.clear()
        return redirect(request.referrer)

    @_app.route("/nuke", methods=["GET", "POST"])
    def nuke(self):
        if request.method == "POST":
            logger.other("Start\n\n")

            token = request.form["token"]
            guildId = int(request.form["guildId"])
            channelName = request.form["channelName"]
            latency = int(request.form["latency"])
            message = request.form["message"]
            allUserBan = "allUserBan" in request.form
            allChannelDelete = "allChannelDelete" in request.form

            logger.other(
f"""
-- Value you entered --
ServerID:{guildId}
ChannelName:{channelName}
Latency:{latency}ms, {latency*0.001}s
-- Options --
AllUserBan:{allUserBan}
AllChannelDelete:{allChannelDelete}

"""
            )

            bot = RaidBot(logger, token, RaidBot.Nuke, (guildId, channelName, latency, [message], allUserBan, allChannelDelete))
            threading.Thread(target=bot.runBot, daemon=True).start()
            bots.append(bot)
        return render_template("nuke.html")

if __name__ == "__main__":
    Web().run()