### Discord AI Chatbot

This is a Discord chatbot that can be easily deployed on your server. It connects to various AI models via the OpenRouter API. All you need is a free Discord developer account, a free OpenRouter account, and a server to host it on, like a free tier instance from Oracle Cloud. 

This guide will walk you through the entire setup process.

-----

### Step 1: Create a Discord Bot

First, you need to set up a new application and bot in the Discord Developer Portal.

1.  Go to the **[Discord Developer Portal](https://www.google.com/search?q=https://discord.com/developers/applications)** and log in with your Discord account.
2.  Click **"New Application"** in the top-left corner, give it a name, and click **"Create"**.
3.  Navigate to the **"Bot"** section in the left-hand menu. Click **"Add Bot"** and confirm with **"Yes, do it\!"**.
4.  Under **"Privileged Gateway Intents"**, enable the **`MESSAGE CONTENT INTENT`** if your bot needs to read message content.

-----

### Step 2: Invite Your Bot to a Server

Now, let's generate an invite link to add your bot to a server.

1.  In the left-hand menu, go to **"OAuth2"** and then **"URL Generator"**.
2.  Under **"Scopes"**, select the **`bot`** option.
3.  Under **"Bot Permissions"**, choose the necessary permissions, such as **`Send Messages`**.
4.  Copy the generated URL from the bottom of the page and paste it into your browser. You can then select your desired server from the dropdown to invite the bot.

-----

### Step 3: Configure OpenRouter

OpenRouter gives you access to multiple AI models through a single API. This is also where you'll choose the specific AI model for your bot.

1.  Go to the **[OpenRouter website](https://openrouter.ai)** and create a free account.
2.  Once logged in, navigate to your dashboard to find your **API Access Token**. You'll need this token for your bot's configuration.
3.  While you're there, browse the **"Models"** section and choose an AI model for your bot.
      * Look for models marked as **"free"**.
      * Consider factors like **latency** (for quick responses) and **quality** (for better answers) when making your choice.
4.  Copy the model's identifier, for example, `google/gemini-2.5-flash-image-preview:free`. You will use this identifier to configure your bot.

-----

### Step 4: Deploy the Bot

To ensure your bot is online 24/7, you can deploy it on a server. This guide uses an Oracle Cloud free tier instance, which is perfect for this.

1.  Connect to your server via **SSH**.

2.  Clone the repository using `git clone`:

    ```bash
    git clone https://github.com/felixld/Discord-Chatbot.git
    cd Discord-Chatbot
    ```

3.  Create a `config.py` file to store your sensitive API keys. **Do not add this file to your GitHub repository\!**

    ```python
    # config.py

    # Discord Bot Token
    DISCORD_BOT_TOKEN = "your_discord_bot_token_here"

    # OpenRouter API Key
    OPENROUTER_API_KEY = "your_openrouter_api_key_here"
    ```

4.  Open the `main.py` file and find the line(47) that defines the AI model. It will look like this:

    ```python
    # ... other code ...
    "model": "tngtech/deepseek-r1t2-chimera:free",
    # ... rest of the code ...
    ```

    Replace the model identifier with the one you copied from OpenRouter. For example:

    ```python
    # ... other code ...
    "model": "your_chosen_model_identifier",
    # ... rest of the code ...
    ```

5.  Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

6.  To run the bot in the background, use `screen`. This keeps the bot running even after you close your SSH session.

      * Install `screen`: `sudo apt-get install screen`
      * Start a new session: `screen -S discord-bot`
      * Run your bot: `python main.py`
      * Detach from the session by pressing **`Ctrl + A`**, then **`D`**.

Your bot is now live and ready to go\! If you have any questions or need to troubleshoot, feel free to open an issue on GitHub.
