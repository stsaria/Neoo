import asyncio
import random
import string
import traceback
import typing

from discord import Member, TextChannel, VoiceChannel, Guild, Role, Status
from discord.abc import GuildChannel

from .Bot import Bot
from .Joiner import Joiner
from ..utils.Logger import Logger

class RaidBot(Bot):
    def __init__(self, logger:Logger, token:str, readyFunc:typing.Callable, readyFuncArgs:tuple):
        super().__init__(token)
        self._logger:Logger = logger
        self._channels:list[GuildChannel] = []

        self._readyFunc = readyFunc
        self._readyFuncArgs = readyFuncArgs

        self._stop = False
    def stop(self):
        self._stop = True
    async def _sendMessage(self, message:str, channel:GuildChannel):
        msg = f"{channel.name},{channel.id}"
        if not type(channel) in [TextChannel, VoiceChannel]:
            self._channels.remove(channel)
        self._logger.success(msg) if await self.sendMessage(message, channel) else self._logger.failed(msg)
    async def OneNuke(self, latency:int, messages:list[str], guild:Guild, channel:GuildChannel, randomMention:bool, roles:list[Role], members:list[Member]):
        for message in messages:
            if message == "":
                continue
            bMessage = message
            if message == messages[0]:
                bMessage = message+"\n"+"".join(random.choice(string.ascii_lowercase) for _ in range(30))+"\n"
            bMessage = bMessage.replace("!userId!", str(random.choice(guild.members).id))
            if randomMention:
                try:
                    bRoles = roles
                    if len(roles) >= 5:
                        bRoles = random.sample(roles, 5)
                    for role in bRoles:
                        bMessage += f"<@&{role.id}> "
                except:
                    pass
                bMessage += "\n"
                try:
                    bMembers = members
                    if len(members) >= 35:
                        bMembers = random.sample(members, 35)
                    for member in bMembers:
                        bMessage += f"<@{member.id}> "
                except:
                    pass
                bMessage += "\n"
            if message != messages[0]:
                bMessage = message
            await self._sendMessage(bMessage, channel)
            await asyncio.sleep(latency*0.001)
    async def Nuke(self, guildId:int, latency:int, messages:list[str], randomMention:bool, exclusionChannelIds:list[int], channelId:int | None=None, numberOfExecutions:int=50):
        guild = self.get_guild(guildId)
        if not guild:
            self._logger.failed(f"Guild not joined ID:{self.user.id}")
            await self.close()
            return
        if channelId:
            channel = guild.get_channel(channelId)
            if not channel:
                self._logger.failed(f"Channel not found ID:{self.user.id}")
                await self.close()
                return
            self._channels = [channel]
        else:
            self._channels = list(guild.channels)
        roles = list(guild.roles)
        members = list(guild.members)
        roles.remove(guild.default_role)
        for _ in range(numberOfExecutions):
            if self._stop:
                await self.close()
                return

            if len(self._channels) == 1:
                for i in range(10):
                    await self.OneNuke(latency, messages, guild, self._channels[0], randomMention, roles, members)
            else:
                random.shuffle(self._channels)
                for channel in self._channels:
                    if str(channel.id) in exclusionChannelIds:
                        continue
                    await self.OneNuke(latency, messages, guild, channel, randomMention, roles, members)
                    random.shuffle(self._channels)
        self._logger.other("End")
        await self.close()
    async def Typing(self, channelId:int):
        channel = self.get_channel(channelId)
        self._logger.other(f"Start typing ID:{self.user.id}")
        async with channel.typing():
            while not self._stop:
                await asyncio.sleep(20)
        self._logger.other("End")
        await self.close()
    async def ChangeStatus(self, statusId:int):
        msg = str(self.user.id)
        status = Status.online
        match statusId:
            case 1:
                status = Status.offline
            case 2:
                status = Status.idle
            case 3:
                status = Status.dnd
        self._logger.success(msg) if await self.changePresenceStatus(status) else self._logger.failed(msg)
        await self.close()
    async def ChangeNickName(self, guildId:int, name:str):
        msg = str(self.user.id)
        self._logger.success(msg) if await self.changeGuildNickName(guildId, name) else self._logger.failed(msg)
        await self.close()
    def JoinGuild(self, inviteId:str, goTime:int):
        joiner = Joiner(self._token, inviteId, goTime)
        r = joiner.join()
        match r:
            case 0:
                self._logger.success(f"Token: "+self._token.split(".")[0])
            case 1:
                self._logger.failed(f"Invite ID not found Token: "+self._token.split(".")[0])
            case 2:
                self._logger.failed(f"Token: "+self._token.split(".")[0])
            case 3:
                self._logger.failed(f"Recaptcha Token: "+self._token.split(".")[0])
    async def LeaveGuild(self, guildId:int):
        msg = str(self.user.id)
        self._logger.success(msg) if await self.leaveGuild(guildId) else self._logger.failed(msg)
        await self.close()
    async def Reaction(self, channelId:int, messageId:int, emoji:str, customEmoji:str):
        msg = str(self.user.id)
        self._logger.success(msg) if await self.reaction(channelId, messageId, emoji, customEmoji) else self._logger.failed(msg)
        await self.close()
    async def PushButton(self, channelId:int, messageId:int):
        msg = str(self.user.id)
        self._logger.success(msg) if await self.pushButton(channelId, messageId) else self._logger.failed(msg)
        await self.close()
    async def on_ready(self):
        self._logger.other(f"Ready ID:{self.user.id}, Name:{self.user.name}")
        await self._readyFunc(*((self,)+self._readyFuncArgs))