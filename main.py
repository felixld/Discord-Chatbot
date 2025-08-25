import discord
from discord import app_commands
import requests
import asyncio
from config import DISCORD_BOT_TOKEN, OPENROUTER_API_KEY


GUILD_ID = None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)


def get_openrouter_response(prompt: str) -> str:
    """Sends a request to the OpenRouter API and returns the response."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        print(f"Sending request to OpenRouter AI with prompt: '{prompt}'")
        response = requests.post(url, headers=headers, json=data)
        
        # Improved debugging: Print the status code and response text.
        print(f"Response status code from OpenRouter: {response.status_code}")
        print(f"Response text from OpenRouter: {response.text}")

        response.raise_for_status()

        ai_text = response.json()['choices'][0]['message']['content']
        
        # The text is no longer truncated here.
        # Instead, the splitting logic is handled in the lumina_command function.
        
        return ai_text
    except requests.exceptions.RequestException as e:
        print(f"Error with the OpenRouter API request: {e}")
        return "Sorry, I couldn't reach OpenRouter AI."
    except KeyError:
        print("Error: Unexpected response from the OpenRouter API.")
        return "Sorry, I couldn't process the response from OpenRouter."


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    if GUILD_ID:
        try:
            guild_obj = discord.Object(id=GUILD_ID)
            await tree.sync(guild=guild_obj)
            print(f"Slash commands for server ID {GUILD_ID} synchronized!")
        except Exception as e:
            print(f"Error syncing for server ID {GUILD_ID}: {e}")
    else:
        await tree.sync()
        print("Global slash commands synchronized!")

@tree.command(
    name="lumina",
    description="Ask Lumina a question and get a response from OpenRouter AI."
)
async def lumina_command(interaction: discord.Interaction, question: str):
    """
    Handles the user's `/lumina` command.
    
    Args:
        interaction (discord.Interaction): The Discord interaction object.
        question (str): The question the user asked.
    """
    
    await interaction.response.defer()
    
    loop = asyncio.get_running_loop()
    response_text = await loop.run_in_executor(None, get_openrouter_response, question)

    # Discord has a character limit of 2000 characters per message.
    # This code splits long responses into multiple messages.
    
    max_discord_length = 2000
    
    # Prefix for the first message, which also contains the question.
    prefix = f"**Question:** {question}\n\n**Answer:** "
    
    # The available space for the first chunk is calculated
    # by subtracting the length of the prefix from the maximum length.
    available_length_first_chunk = max_discord_length - len(prefix)
    
    # Send the first part of the response.
    # We take only as much of the response as is available.
    first_chunk = response_text[:available_length_first_chunk]
    await interaction.followup.send(f"{prefix}{first_chunk}")
    
    # Send the remaining parts of the response in separate messages.
    # Since no prefix is needed here, we use the full maximum length
    # for the subsequent chunks.
    remaining_text = response_text[available_length_first_chunk:]
    for i in range(0, len(remaining_text), max_discord_length):
        chunk = remaining_text[i:i + max_discord_length]
        await interaction.channel.send(chunk)


if __name__ == "__main__":
    if DISCORD_BOT_TOKEN == "DEIN_DISCORD_BOT_TOKEN_HIER" or OPENROUTER_API_KEY == "DEIN_OPENROUTER_API_SCHLUESSEL_HIER":
        print("Error: Please replace the placeholders in config.py with your real tokens.")
    else:
        print("Attempting to start the bot...")
        try:
            client.run(DISCORD_BOT_TOKEN)
        except discord.LoginFailure as e:
            print(f"Login error: {e}")
            print("Possible causes:")
            print("- Your Discord token is invalid or incorrect.")
            print("- Bot intents are not enabled in the Discord Developer Portal.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")