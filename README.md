### Discord AI Chatbot

This is a Discord chatbot that can be easily deployed on your server or run locally on your PC. It connects to various AI models via the OpenRouter API. All you need is a free Discord developer account, a free OpenRouter account, and either a server to host it on or a local machine to run it from.

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

### Step 4: Deployment

You can either deploy the bot on a server or run it on your own PC.

#### Option A: Deploying to a Server (Oracle Cloud)

To ensure your bot is online 24/7, you can deploy it on a server. The Oracle Cloud Free Tier provides a great option for this.

1.  **Create a Free Tier Instance**:
    If you don't have one, log in to your Oracle Cloud account and create a new **"Compute Instance"** under the **"Always Free"** options.

2.  **Connect via SSH**:
    Once your instance is running, find its public IP address and connect to it using SSH.

3.  **Clone the Repository**:
    Run the following commands in your terminal to get the bot's code:

    ```bash
    git clone https://github.com/felixld/Discord-Chatbot.git
    cd Discord-Chatbot
    ```

4.  **Create the `config.py` File**:
    Create a `config.py` file to store your sensitive API keys. **Do not add this file to your GitHub repository\!**

    ```python
    # config.py

    # Discord Bot Token
    DISCORD_BOT_TOKEN = "your_discord_bot_token_here"

    # OpenRouter API Key
    OPENROUTER_API_KEY = "your_openrouter_api_key_here"
    ```

5.  **Configure the AI Model**:
    Open the `main.py` file and find the line that defines the AI model. It will look similar to this:

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

6.  **Install Dependencies and Run**:
    Install the required libraries and then run the bot using `screen` to keep it online in the background.

    ```bash
    pip install -r requirements.txt
    sudo apt-get install screen  # Install screen for background operation
    screen -S discord-bot
    python main.py
    # To detach, press Ctrl + A, then D
    ```

#### Option B: Installing on Your Local PC

You can also run the bot directly on your computer. This is great for testing or a bot you don't need to have online all the time.

1.  **Install Python (if needed)**:

      * **macOS**: You can use `brew`: `brew install python`
      * **Windows**: Download the installer from the **[Python website](https://www.python.org/downloads/windows/)**. Make sure to check the box that says **"Add Python to PATH"** during installation.
      * **Ubuntu / Debian**: Use `apt`: `sudo apt update && sudo apt install python3 python3-pip`
      * **Arch / Manjaro**: Use `pacman`: `sudo pacman -S python`

2.  **Clone the Repository**:
    Open your terminal or command prompt and clone the repository:

    ```bash
    git clone https://github.com/felixld/Discord-Chatbot.git
    cd Discord-Chatbot
    ```

3.  **Create the `config.py` File**:
    Create a `config.py` file as described in the server deployment section and paste your Discord bot token and OpenRouter API key into it.

4.  **Configure the AI Model**:
    Open `main.py` and replace the model identifier string with your chosen model from OpenRouter, as described above.

5.  **Install Dependencies**:
    Install the required libraries with `pip`:

    ```bash
    pip install -r requirements.txt
    ```

6.  **Run the Bot**:
    Finally, run the bot from your terminal:

    ```bash
    python main.py
    ```

Your bot is now live and ready to go\! If you have any questions or need to troubleshoot, feel free to open an issue on GitHub.
