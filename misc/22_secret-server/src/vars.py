import os

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
SERVER_ID = int(os.environ.get("SERVER_ID"))
SECRET_CHANNEL_ID = int(os.environ.get("SECRET_CHANNEL_ID"))
ADMIN_CHANNEL_ID = int(os.environ.get("ADMIN_CHANNEL_ID"))
VERIFY_MESSAGE_ID = int(os.environ.get("VERIFY_MESSAGE_ID"))
VERIFY_CHANNEL_ID = int(os.environ.get("VERIFY_CHANNEL_ID"))
COLOUR_MESSAGE_ID = int(os.environ.get("COLOUR_MESSAGE_ID"))
MOD_MESSAGE_ID = int(os.environ.get("MOD_MESSAGE_ID"))
MOD_CHANNEL_ID = int(os.environ.get("MOD_CHANNEL_ID"))
VERIFIED_ROLE_ID = int(os.environ.get("VERIFIED_ROLE_ID"))

with open("instructions.txt") as f:
    instructions = f.read()
