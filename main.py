# Import necessary libraries.
# `discord` is the main library for interacting with the Discord API.
# `discord.app_commands` is used for creating slash commands.
# `requests` is a library for making HTTP requests to external APIs.
# `asyncio` is used to run asynchronous operations, which is crucial for Discord bots.
# `config` is a custom file where sensitive information (like API keys) is stored.
import discord
from discord import app_commands
import requests
import asyncio
from config import DISCORD_BOT_TOKEN, OPENROUTER_API_KEY


# Define a global variable for the guild (server) ID.
# If this is set to a specific ID, the slash commands will be synced only to that guild.
# If it's `None`, the commands will be synced globally, which can take up to an hour.
GUILD_ID = None

# Set up the bot's intents.
# Intents are permissions that tell Discord which events your bot wants to listen to.
# `intents.message_content = True` is necessary to read message content.
intents = discord.Intents.default()
intents.message_content = True
# Create the Discord client instance.
client = discord.Client(intents=intents)

# Create a `CommandTree` object.
# This tree will manage all the slash commands for the bot.
tree = app_commands.CommandTree(client)


def get_openrouter_response(prompt: str) -> str:
    """
    Sends a request to the OpenRouter API and returns the AI's response.
    This is a synchronous function, so it will block until the API responds.
    It's designed to be run in a separate thread to prevent blocking the bot's event loop.
    """
    # Define the API endpoint URL.
    url = "https://openrouter.ai/api/v1/chat/completions"
    # Define the headers for the API request, including the authorization token.
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    # Define the JSON payload for the request, including the AI model and the user's prompt.
    data = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        print(f"Sending request to OpenRouter AI with prompt: '{prompt}'")
        # Send the POST request to the API.
        response = requests.post(url, headers=headers, json=data)
        
        # Log the response status and content for debugging purposes.
        print(f"Response status code from OpenRouter: {response.status_code}")
        print(f"Response text from OpenRouter: {response.text}")

        # Raise an exception for bad status codes (e.g., 4xx or 5xx).
        response.raise_for_status()

        # Parse the JSON response and extract the AI's generated text.
        ai_text = response.json()['choices'][0]['message']['content']
        
        return ai_text
    
    # Catch any exceptions that occur during the request.
    except requests.exceptions.RequestException as e:
        print(f"Error with the OpenRouter API request: {e}")
        return "Sorry, I couldn't reach OpenRouter AI."
    except KeyError:
        print("Error: Unexpected response from the OpenRouter API.")
        return "Sorry, I couldn't process the response from OpenRouter."


# `on_ready` is a Discord event that fires when the bot successfully logs in.
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    # Check if a specific `GUILD_ID` is set.
    if GUILD_ID:
        try:
            # Sync commands to a specific guild to make them available immediately.
            guild_obj = discord.Object(id=GUILD_ID)
            await tree.sync(guild=guild_obj)
            print(f"Slash commands for server ID {GUILD_ID} synchronized!")
        except Exception as e:
            print(f"Error syncing for server ID {GUILD_ID}: {e}")
    else:
        # Sync commands globally. This can take some time.
        await tree.sync()
        print("Global slash commands synchronized!")

# Define a slash command using a decorator.
# `name` is the command name (e.g., `/lumina`).
# `description` is the text that appears in the Discord UI.
@tree.command(
    name="lumina",
    description="Ask Lumina a question and get a response from OpenRouter AI."
)
async def lumina_command(interaction: discord.Interaction, question: str):
    """
    Handles the user's `/lumina` command.
    """
    
    # Immediately defer the interaction response.
    # This tells Discord that the bot is working on the request,
    # preventing a "timeout" error for long-running tasks.
    await interaction.response.defer()
    
    # Get the current event loop.
    loop = asyncio.get_running_loop()
    # Run the synchronous `get_openrouter_response` function in a separate thread.
    # This prevents the bot from freezing while waiting for the API response.
    response_text = await loop.run_in_executor(None, get_openrouter_response, question)

    # Discord's message character limit is 2000.
    max_discord_length = 2000
    
    # Define a prefix for the first message, including the original question.
    prefix = f"**Question:** {question}\n\n**Answer:** "
    
    # Calculate how much space is left for the first message chunk.
    available_length_first_chunk = max_discord_length - len(prefix)
    
    # Get the first part of the response text that fits into the first message.
    first_chunk = response_text[:available_length_first_chunk]
    # Send the first message using `followup.send`, as the interaction was deferred.
    await interaction.followup.send(f"{prefix}{first_chunk}")
    
    # Handle splitting and sending the rest of the response in separate messages.
    remaining_text = response_text[available_length_first_chunk:]
    # Loop through the remaining text in chunks of `max_discord_length`.
    for i in range(0, len(remaining_text), max_discord_length):
        chunk = remaining_text[i:i + max_discord_length]
        # Send each chunk to the same channel.
        await interaction.channel.send(chunk)


# This block ensures the code only runs when the script is executed directly.
if __name__ == "__main__":
    # Check if the placeholder API tokens have been replaced.
    if DISCORD_BOT_TOKEN == "DEIN_DISCORD_BOT_TOKEN_HIER" or OPENROUTER_API_KEY == "DEIN_OPENROUTER_API_SCHLUESSEL_HIER":
        print("Error: Please replace the placeholders in config.py with your real tokens.")
    else:
        print("Attempting to start the bot...")
        try:
            # Start the bot by logging in with the token.
            client.run(DISCORD_BOT_TOKEN)
        # Handle specific exceptions for clearer error messages.
        except discord.LoginFailure as e:
            print(f"Login error: {e}")
            print("Possible causes:")
            print("- Your Discord token is invalid or incorrect.")
            print("- Bot intents are not enabled in the Discord Developer Portal.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
