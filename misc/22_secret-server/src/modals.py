import discord, aiohttp
from discord import ui
from sqlalchemy.orm import Session

from logs import *
from vars import *
from models import User
from database import engine

class GetTokenModal(ui.Modal, title='Submit Access Token'):
    access_token = ui.TextInput(label='Access Token')

    def __init__(self, url):
        self.url = url
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction):
        # test the token
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/api/v1/users/me", headers={ 'Authorization': f'Token {self.access_token}', 'Content-Type' : 'application/json' }) as resp:
                status_code = resp.status
                if status_code == 200 or status_code == 400:
                    try:
                        ret = await resp.json()
                        if not ret['success']:
                            logger.warning(data['error'])
                            await interaction.response.send_message(f"Verification failed. Please try again.", ephemeral=True)
                        else:
                            data = ret['data']
                            logger.info(f"{data['name']} <=> {interaction.user.name}")

                            # do database-related stuff
                            with Session(engine) as session:
                                # check if the user has been linked
                                row = session.query(User).filter(User.discordId == interaction.user.id).first()

                                if row is None:
                                    session.add(User(
                                        platformName=data['name'],
                                        discordId=interaction.user.id,
                                        discordTag=interaction.user.name
                                    ))
                                else:
                                    session.query(User).filter(User.discordId == interaction.user.id).update({
                                        User.platformName: data['name']
                                    })
                                session.commit()

                            try:
                                guild = await interaction.client.fetch_guild(SERVER_ID)
                                member = await guild.fetch_member(interaction.user.id)
                                await member.add_roles(discord.Object(id=VERIFIED_ROLE_ID))
                            except Exception as e:
                                logger.fatal(str(e))
                                logger.fatal("Failed to add verified role!")
                                await interaction.response.send_message("Verification succeeded but cannot add verified role. Please contact admin.", ephemeral=True)
                                return

                            await interaction.response.send_message(f'Verification succeeded. You can safely delete the token now.', ephemeral=True)
                    except Exception as e:
                        logger.error(str(e.with_traceback(None)))
                        await interaction.response.send_message(f"Verification failed (possibly the bot is not working). Please try contact admin for help.", ephemeral=True)
                else:
                    logger.error(f"Sent API request with received status code {status_code}")
                    await interaction.response.send_message(f"Verification failed with HTTP status code {status_code}. Please try contact admin for help.", ephemeral=True)
