import discord, time
from discord.ext import commands, tasks
from sqlalchemy.orm import Session
from datetime import datetime

from vars import *
from logs import *
from database import engine
from models import User

class SafetyCog(commands.Cog):
    flag_role_id: int
    mod_role_id: int
    magic_color: discord.Colour
    magic_color_2: discord.Colour
    role_remove_queue: list[tuple[int, datetime]]

    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.magic_color = discord.Colour.dark_orange()
        self.magic_color_2 = discord.Colour.dark_gold()
        self.role_remove_queue = []

        self.initer.start()
        time.sleep(2)
        self.safety_checker.start()
        self.role_remover.start()

    @tasks.loop(seconds=5.0, count=1)
    async def initer(self):
        await self.init_flag_role()

    @tasks.loop(seconds=5.0)
    async def safety_checker(self):
        try:
            await self.ensure_dignity()
        except Exception as e:
            logger.warning(f"Error while doing safety check: {str(e)}")
            logger.warning("Ensuring dignity failed, possibly the roles have been deleted")
    
    @tasks.loop(seconds=5.0)
    async def role_remover(self):
        guild = self.bot.get_guild(SERVER_ID)
        flag_role = guild.get_role(self.flag_role_id)
        while not len(self.role_remove_queue) == 0:
            discord_id, get_time = self.role_remove_queue[0]
            if get_time + 60 <= time.time():
                # remove role
                self.role_remove_queue.pop(0)
                try:
                    member = guild.get_member(discord_id)
                    if flag_role in member.roles:
                        await member.remove_roles(flag_role)
                        logger.info(f"Removed bot role from user {member.name}")
                except Exception as e:
                    logger.warning(str(e))
                    logger.warning("Bot role removal failed, possibly the bot role has been deleted")
            else:
                break

    def cog_unload(self):
        self.initer.cancel()
        self.safety_checker.cancel()

    async def init_flag_role(self):
        # wait for the bot to be ready
        await self.bot.wait_until_ready()

        # get guilds and channels
        guild = self.bot.get_guild(SERVER_ID)

        roles = guild.roles
        flag_role, mod_role = None, None
        for role in roles:
            if role.name == "Bot" and role.color == self.magic_color:
                flag_role = role
                self.flag_role_id = role.id
            elif role.name == "Trial Moderator" and role.color == self.magic_color_2:
                mod_role = role
                self.mod_role_id = role.id

        if mod_role is None:
            mod_role = await guild.create_role(name="Trial Moderator", color=self.magic_color_2, permissions=discord.Permissions(1 << 28))
            self.mod_role_id = mod_role.id

        # create role and store it
        if flag_role is None:
            flag_role = await guild.create_role(name="Bot", color=self.magic_color)
            self.flag_role_id = flag_role.id

            await guild.edit_role_positions(positions={
                flag_role: 2,
                mod_role: 1
            })

        async for member in guild.fetch_members():
            if member.bot:
                await member.add_roles(flag_role)
        
        await guild.edit_role_positions(positions={
            flag_role: 1,
            mod_role: 2
        })

        # apply channel access to the roles
        await self.ensure_channel_access()

    async def ensure_lowest_priv(self):
        guild = self.bot.get_guild(SERVER_ID)
        flag_role: discord.Role = guild.get_role(self.flag_role_id)
        mod_role: discord.Role = guild.get_role(self.mod_role_id)

        all_roles = await guild.fetch_roles()
        positions = dict(zip(all_roles, [role.position for role in all_roles]))

        if flag_role >= mod_role:
            temp = positions[flag_role]
            positions[flag_role] = positions[mod_role]
            positions[mod_role] = temp

            await guild.edit_role_positions(positions=positions)
        
        if flag_role.permissions != discord.Permissions.none():
            await flag_role.edit(permissions=discord.Permissions.none())
        if mod_role.permissions != discord.Permissions(1 << 28):
            await mod_role.edit(permissions=discord.Permissions(1 << 28))
    
    async def ensure_misc(self):
        guild = self.bot.get_guild(SERVER_ID)
        flag_role: discord.Role = guild.get_role(self.flag_role_id)
        mod_role: discord.Role = guild.get_role(self.mod_role_id)

        # ensure color
        if flag_role.color != self.magic_color:
            await flag_role.edit(color=self.magic_color)
        if mod_role.color != self.magic_color_2:
            await mod_role.edit(color=self.magic_color_2)

        # check hoist
        if flag_role.hoist:
            await flag_role.edit(hoist=False)
        if mod_role.hoist:
            await mod_role.edit(hoist=True)

        # check name
        if flag_role.name != "Bot":
            await flag_role.edit(name="Bot")
        if mod_role.name != "Trial Moderator":
            await mod_role.edit(name="Trial Moderator")

    async def ensure_channel_access(self):
        guild = self.bot.get_guild(SERVER_ID)
        flag_role: discord.Role = guild.get_role(self.flag_role_id)
        mod_role: discord.Role = guild.get_role(self.mod_role_id)

        secret_channel = guild.get_channel(SECRET_CHANNEL_ID)
        mod_channel = guild.get_channel(MOD_CHANNEL_ID)

        await secret_channel.set_permissions(flag_role, read_messages=True, send_messages=False)
        await mod_channel.set_permissions(mod_role, read_messages=True, send_messages=True)

    async def ensure_dignity(self):
        await self.ensure_lowest_priv()
        await self.ensure_misc()
        await self.ensure_channel_access()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        if role.id == self.flag_role_id or role.id == self.mod_role_id:
            # someone deleted the critical role
            # alert admins
            channel: discord.TextChannel = self.bot.get_channel(ADMIN_CHANNEL_ID)
            guild = channel.guild
            entry = [entry async for entry in guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1)][0]

            if entry.user.id != self.bot.user.id:
                try:
                    mod_role = guild.get_role(self.mod_role_id)
                    await entry.user.remove_roles(mod_role)
                except:
                    pass
                with Session(engine) as session:
                    ret = session.query(User).filter(User.discordId == entry.user.id).first()
                    logger.fatal(f"User \"{ret.platformName}\" tries to prevent others from solving Secret Server! Revoke its trial moderator role.")
                    await channel.send(f"<@&1264120381711581245> User <@{entry.user.id}> (platform username: `{ret.platformName}`) deleted `{role.name}` at time `{entry.created_at}`!")
            else:
                logger.info("Self-delete mechanism activated")

            # recreate new one
            await self.init_flag_role()

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        guild = before.guild
        flag_role = guild.get_role(self.flag_role_id)
        all_roles = await guild.fetch_roles()
        if flag_role in all_roles:
            if before.bot and flag_role not in after.roles:
                logger.warning(f"Add back bot role to {before.name}")
                await after.add_roles(flag_role)
            elif not before.bot and flag_role in after.roles:
                now = time.time()
                self.role_remove_queue.append((before.id, now))
                logger.info(f"User {before.name} get bot role, will remove after 1 minute")
        else:
            logger.warning("Role deleted, cannot add back the role")

class VerificationCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.magic_color_2 = discord.Colour.dark_gold()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # sends a DM containing instructions to provide a CTFd token
        message_id, user_id, emoji = payload.message_id, payload.user_id, payload.emoji
        if message_id == VERIFY_MESSAGE_ID and emoji.name == "✅":
            user = await self.bot.fetch_user(user_id)
            logger.info("Sending instructions to user...")
            await user.send(instructions)
        elif message_id == COLOUR_MESSAGE_ID:
            user = await self.bot.fetch_user(user_id)
            await user.send("The colour roles are now in maintenance. Sorry for any inconvenience caused.")
        elif message_id == MOD_MESSAGE_ID and emoji.name == "✅":
            guild: discord.Guild = self.bot.get_guild(SERVER_ID)
            roles = guild.roles

            mod_role = None
            for role in roles:
                if role.name == "Trial Moderator" and role.color == self.magic_color_2:
                    mod_role = role
                    break
            
            if mod_role is None:
                await user.send("Currently there are some unpredictable errors. Please try again.")
                return
            
            member = await guild.fetch_member(user_id)
            await member.add_roles(mod_role)
