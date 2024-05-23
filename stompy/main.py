"""Defines the main entrypoint for the Discord bot."""

from typing import Final
import os
import sys
from discord import Intents, Client, Message
import logging
import requests
from openai import OpenAI
from dotenv import load_dotenv
from stompy.src.scrape_arxiv import scrape_arxiv2
from typing import List

logger = logging.getLogger(__name__)
load_dotenv()
# Gets the Stompy Discord token.
TOKEN: Final[str] = os.getenv("STOMPY_DISCORD_TOKEN")
ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Creates the client with the default intents.
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# instead of humanoid search : cs.ro
# time based : every day
# author affiliation
# one sentence summary
# no publish date
# embed link into the titlegit


async def get_response(user_message: str) -> List[str]:
    response = []
    if user_message == "humanoid":
        list = scrape_arxiv2()
        return_message = "\n"
        return_message += (
            "Within the last week there were " + str(len(list[0])) + " humanoid related papers published on arXiv!\n"
        )
        response.append(return_message)
        for i in range(0, len(list[0])):
            return_message = ""
            return_message += "## " + str(i + 1) + ". " + list[4][i] + "\n"
            return_message += "**Authors:** " + list[2][i] + "\n"
            return_message += "**Published:** " + list[1][i] + "\n"
            completion = ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "summarize the following article in 2 sentences: " + list[3][i]},
                ],
            )
            summary = completion.choices[0].message.content
            return_message += "**Summary:** " + summary + "\n"
            return_message += "**Read more:** " + list[0][i] + "\n"
            response.append(return_message)
    else:
        completion = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "summarize the following article in 2 sentences: " + list[3][i]},
            ],
        )
        response.append(completion.choices[0].message.content)
    return response


async def send_message(message: Message, user_message: str) -> None:

    if not user_message:
        logger.info("Message was empty because intents were not enabled probably")
        return
    if user_message[0] != "!" and user_message[0] != "?":
        return
    is_private = user_message[0] == "?"
    user_message = user_message[1:]
    try:
        response = await get_response(user_message)
        for i in range(0, len(response)):
            try:
                await message.author.send(response[i]) if is_private else await message.channel.send(response[i])
            except Exception as e:
                logger.error("Error: %s", e)
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
    if not TOKEN:
        logger.error("Stompy Discord token is not set")
        return
    client.run(token=TOKEN)


if __name__ == "__main__":
    # python -m stompy.main
    main()
