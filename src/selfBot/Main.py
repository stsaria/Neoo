import threading
import os
import time

from flask import Flask, request, redirect, render_template

from src.selfBot.ChromeSetuper import ChromeSetuper
from src.selfBot.RaidBot import RaidBot
from src.utils.Logger import Logger

logger:Logger = Logger()
bots:list[RaidBot] = []

def clear():
    [bot.stop() for bot in bots]
    logger.clear()
    bots.clear()

class Web:
    _app = Flask(__name__, template_folder=os.path.abspath("templates/selfBot/"), static_folder=os.path.abspath("static/"))
    _app.config['TEMPLATES_AUTO_RELOAD'] = True
    _app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    def run(self, host:str="0.0.0.0", port:int=8081):
        self._app.run(host, port)
    @staticmethod
    @_app.route("/getLog", methods=["GET"])
    def getLog():
        return logger.toStr()
    @staticmethod
    @_app.route("/stop", methods=["GET"])
    def stop():
        clear()
        return redirect(request.referrer)
    @staticmethod
    @_app.route("/changeStatus", methods=["GET", "POST"])
    def changeStatus():
        if request.method == "POST":
            clear()
            logger.other("Start Pman StatusChanger P3G\n\n")

            tokens = request.form["tokens"].split("\r\n")
            status = int(request.form["status"])

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.ChangeStatus, (status,))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("changeStatus.html")
        return render_template("changeStatus.html")
    @staticmethod
    @_app.route("/changeNickName", methods=["GET", "POST"])
    def changeNickName():
        if request.method == "POST":
            clear()
            logger.other("Start Pman ChangeNickName P3P\n\n")

            tokens = request.form["tokens"].split("\r\n")
            guildId = int(request.form["guildId"])
            newName = request.form["newName"]

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.ChangeNickName, (guildId, newName))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("changeNickName.html")
        return render_template("changeNickName.html")

    @staticmethod
    @_app.route("/joinGuild", methods=["GET", "POST"])
    def joinGuild():
        if request.method == "POST":
            clear()
            logger.other("Start Pman Joiner PPP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            guildInviteCode = request.form["guildInviteCode"]
            goTime = int(request.form["goTime"])

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.JoinGuild, (guildInviteCode, int(time.time())+goTime))
                threading.Thread(target=RaidBot.JoinGuild, args=(bot, guildInviteCode, int(time.time())+goTime), daemon=True).start()
                bots.append(bot)
            return render_template("joinGuild.html")
        return render_template("joinGuild.html")

    @staticmethod
    @_app.route("/leaveGuild", methods=["GET", "POST"])
    def leaveGuild():
        if request.method == "POST":
            clear()
            logger.other("Start Pman Leaver PPP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            guildId = int(request.form["guildId"])

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.LeaveGuild, (guildId,))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("leaveGuild.html")
        return render_template("leaveGuild.html")

    @staticmethod
    @_app.route("/reaction", methods=["GET", "POST"])
    def reaction():
        if request.method == "POST":
            clear()
            logger.other("Start Pman Reaction PwP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            channelId = int(request.form["channelId"])
            messageId = int(request.form["messageId"])
            emoji = request.form['emoji']
            customEmoji = request.form['customEmoji']

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.Reaction, (channelId, messageId, emoji, customEmoji))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("reaction.html")
        return render_template("reaction.html")

    @staticmethod
    @_app.route("/pushButton", methods=["GET", "POST"])
    def pushButton():
        if request.method == "POST":
            clear()
            logger.other("Start Pman PushButton PeP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            channelId = int(request.form["channelId"])
            messageId = int(request.form["messageId"])

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.PushButton, (channelId, messageId))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("pushButton.html")
        return render_template("pushButton.html")

    @staticmethod
    @_app.route("/typing", methods=["GET", "POST"])
    def typing():
        if request.method == "POST":
            clear()
            logger.other("Start Pman Typer PzP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            channelId = int(request.form["channelId"])

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.Typing, (channelId,))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("typing.html")
        return render_template("typing.html")


    @staticmethod
    @_app.route("/channelNuke", methods=["GET", "POST"])
    def channelNuke():
        if request.method == "POST":
            clear()
            logger.other("Start Pman ChannelNuke PQP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            guildId = int(request.form["guildId"])
            channelId = int(request.form["channelId"])
            latency = int(request.form["latency"])
            message = request.form["message"]
            subMessages  = request.form["subMessages"].split("\r\n")
            randomMention = "randomMention" in request.form

            logger.other(
f"""-- Value you entered --
GuildId:{guildId}
ChannelID:{channelId}
Latency:{latency}ms, {latency*0.001}s
message:\n{message}\n
subMessages:{subMessages}
-- Options --
RandomMention:{randomMention}""")

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.Nuke, (guildId, latency, [message]+subMessages, randomMention, [], channelId))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("channelNuke.html")
        return render_template("channelNuke.html")
    @staticmethod
    @_app.route("/nuke", methods=["GET", "POST"])
    def nuke():
        if request.method == "POST":
            clear()
            logger.other("Start Pman Nuke PPP\n\n")

            tokens = request.form["tokens"].split("\r\n")
            guildId = int(request.form["guildId"])
            latency = int(request.form["latency"])
            message = request.form["message"]
            subMessages  = request.form["subMessages"].split("\r\n")
            exclusionChannelIdsTmp = request.form["exclusionChannelIds"].split(",")
            exclusionChannelIds = []
            try:
                for sId in exclusionChannelIdsTmp:
                    exclusionChannelIds.append(int(sId))
            except:
                pass
            randomMention = "randomMention" in request.form

            logger.other(
f"""-- Value you entered --
ServerID:{guildId}
Latency:{latency}ms, {latency*0.001}s
message:\n{message}\n
subMessages:{subMessages}
exclusionChannelIDs:{exclusionChannelIds}
-- Options --
RandomMention:{randomMention}""")

            for token in tokens:
                bot = RaidBot(logger, token, RaidBot.Nuke, (guildId, latency, [message]+subMessages, randomMention, exclusionChannelIds))
                threading.Thread(target=bot.runBot, daemon=True).start()
                bots.append(bot)
            return render_template("nuke.html")
        return render_template("nuke.html")

if __name__ == "__main__":
    ChromeSetuper.setup()
    Web().run()

