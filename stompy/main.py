"""Defines the main entrypoint for the Discord bot."""

import logging
import os
from typing import Final

from discord import Client, Intents, Message

logger = logging.getLogger(__name__)

# Gets the Stompy Discord token.
TOKEN: Final[str] = os.environ["STOMPY_DISCORD_TOKEN"]

# Creates the client with the default intents.
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


async def get_response(user_message: str) -> str:
    return user_message.replace("?", "!")


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        logger.info("Message was empty because intents were not enabled probably")
        return
    if is_private := user_message[0] == "?":
        user_message = user_message[1:]
    try:
        response = await get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        logger.error("Error: %s", e)


@client.event
async def on_ready() -> None:
    logger.info("%s is now running", client.user)


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    logger.info('[%s] %s: "%s"', channel, username, user_message)
    await send_message(message, user_message)


def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    # python -m stompy.main
    main()
