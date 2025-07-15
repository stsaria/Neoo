from discord.abc import GuildChannel
from discord import Client, Member, Guild, TextChannel, VoiceChannel, Status, Button, ActionRow

class Bot(Client):
    def __init__(self, token:str):
        super().__init__()
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
    async def createChannel(self, channelName:str, guild:Guild) -> bool:
        try:
            await guild.create_text_channel(channelName)
        except:
            return False
        return True
    async def changePresenceStatus(self, status:Status) -> bool:
        try:
            await self.change_presence(status=status)
        except:
            return False
        return True
    async def changeGuildNickName(self, guildId:int, name:str) -> bool:
        try:
            guild = self.get_guild(guildId)
            i = guild.get_member(self.user.id)
            await i.edit(nick=name)
        except:
            return False
        return True
    async def leaveGuild(self, guildId:int) -> bool:
        try:
            guild = self.get_guild(guildId)
            await guild.leave()
        except:
            return False
        return True
    async def reaction(self, channelId:int, messageId:int, emoji:str, customEmoji:str) -> bool:
        try:
            channel = self.get_channel(channelId)
            message = await channel.fetch_message(messageId)
            if customEmoji.replace(" ", "") == "":
                await message.add_reaction(emoji)
            else:
                await message.add_reaction(customEmoji)
        except:
            return False
        return True
    async def pushButton(self, channelId:int, messageId:int):
        try:
            channel = self.get_channel(channelId)
            message = await channel.fetch_message(messageId)
            for component in message.components:
                if type(component) == Button:
                    await component.click()
                elif type(component) == ActionRow:
                    for child in component.children:
                        if type(child) == Button:
                            await child.click()
        except:
            return False
        return True
    def runBot(self):
        self.run(self._token, reconnect=True)