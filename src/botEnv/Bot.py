from discord import Intents, Member, TextChannel, VoiceChannel, Guild
from discord.abc import GuildChannel
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, token:str):
        super().__init__(intents=Intents.default(), command_prefix="!", description="Yaa so good bot\n<<sound:1>>")
        self._token:str = token
    async def banUser(self, user:Member) -> bool:
        try:
            await user.ban(reason="Fuck Server User")
        except:
            return False
        return True
    async def deleteChannel(self, channel:GuildChannel) -> bool:
        try:
            await channel.delete()
        except:
            return False
        return True
    async def sendMessage(self, message:str, channel:TextChannel | VoiceChannel) -> bool:
        try:
            await channel.send(message)
        except:
            return False
        return True
    async def createChannel(self, channelName:str, guild:Guild):
        try:
            await guild.create_text_channel(channelName)
        except:
            return False
        return True
    def runBot(self):
        self.run(self._token, reconnect=True)