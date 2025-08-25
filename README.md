### Discord-Chatbot

This is a Discord chatbot that can be easily deployed on your server. You'll need a free Discord developer account, a free OpenRouter account, and a server to host it on, like a free tier instance from Oracle Cloud.

This guide will walk you through the entire setup process.

-----

### Step 1: Create a Discord Developer Account

First, you need to create an application in the Discord Developer Portal.

1.  Go to the **[Discord Developer Portal](https://www.google.com/search?q=https://discord.com/developers/applications)** and log in with your Discord account.
2.  Click **"New Application"** in the top left corner.
3.  Give your application a name and click **"Create"**. Your application is now the foundation for your bot.

-----

### Step 2: Create and Invite Your Bot

Now, let's create a bot from your application and get it ready to join your server.

1.  In the left-hand menu of your application, select **"Bot"**.
2.  Click **"Add Bot"** and confirm with **"Yes, do it\!"**.
3.  Scroll down to **"Privileged Gateway Intents"** and enable **`MESSAGE CONTENT INTENT`** if your bot needs to read message content.
4.  Next, go to **"OAuth2"** and then **"URL Generator"** in the left-hand menu.
5.  Under **Scopes**, select the **`bot`** option.
6.  Under **Bot Permissions**, select the necessary permissions for your bot (e.g., `Send Messages`).
7.  Copy the generated URL and paste it into your browser. You can then select your server from the dropdown to invite the bot.

-----

### Step 3: Setting up OpenRouter

OpenRouter provides access to various AI models via a single API.

1.  Go to the **[OpenRouter website](https://openrouter.ai)** and create a free account.
2.  After signing up, you will find your **API Access Token** in your dashboard. You will need this token to configure your bot.

-----

### Step 4: Deploying to an Oracle Cloud Server

To keep your bot online 24/7, you can deploy it to a free tier instance on Oracle Cloud.

1.  Make sure you have a Free Tier instance created in your Oracle Cloud console.

2.  Connect to your server via **SSH**.

3.  Copy the repository to your server using `git clone` by running the following command: `git clone https://github.com/felixld/Discord-Chatbot.git`

4.  Navigate into the new directory: `cd Discord-Chatbot`

5.  Create a file named `config.py` to store your API keys. **Do not put this file in your GitHub repository\!**

    ```python
    # config.py

    # Discord Bot Token
    DISCORD_BOT_TOKEN = "Place your Discord bot token here"

    # OpenRouter API Key
    OPENROUTER_API_KEY = "Place your OpenRouter API key here"
    ```

6.  Install the required Python libraries using `pip`: `pip install -r requirements.txt`

7.  To run the bot in the background, you can use `screen`. This is a useful tool that keeps your session running even after you disconnect from SSH.

      - Install `screen`: `sudo apt-get install screen`
      - Start a new `screen` session: `screen -S discord-bot`
      - Run your bot's main file: `python main.py`
      - To detach from the session, press `Ctrl + A`, then `D`. Your bot will continue to run in the background.

Your bot is now live on the server and ready to use\! Let me know if you'd like to adjust the instructions or need help with another step.
