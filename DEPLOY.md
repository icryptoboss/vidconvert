# Deployment Guide

This guide provides instructions on how to deploy the Video Converter Bot to various platforms.

## Prerequisites

*   A GitHub repository with the bot's code.
*   Your `API_ID`, `API_HASH`, and `BOT_TOKEN` ready.

## Koyeb

1.  **Create a Koyeb account:** If you don't have one, sign up at [koyeb.com](https://www.koyeb.com/).
2.  **Create a new App:**
    *   Click on the "Create App" button.
    *   Choose "GitHub" as the deployment method and select your repository.
3.  **Configure the Service:**
    *   **Service Type:** Worker
    *   **Builder:** Docker
    *   **DockerfilePath:** ./Dockerfile (We will create this file next)
    *   **Run Command:** `python bot.py`
4.  **Add Environment Variables:**
    *   Click on the "Environment Variables" tab.
    *   Add the following variables:
        *   `API_ID`: Your Telegram API ID.
        *   `API_HASH`: Your Telegram API hash.
        *   `BOT_TOKEN`: Your Telegram bot token.
5.  **Deploy:** Click on the "Deploy" button.

### Dockerfile for Koyeb

Create a file named `Dockerfile` in the root of your repository with the following content:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

## Render

1.  **Create a Render account:** If you don't have one, sign up at [render.com](https://www.render.com/).
2.  **Create a new Web Service:**
    *   Click on the "New +" button and select "Web Service".
    *   Connect your GitHub account and select your repository.
3.  **Configure the Service:**
    *   **Name:** A name for your service (e.g., `video-converter-bot`).
    *   **Region:** Choose a region close to you.
    *   **Branch:** The branch you want to deploy (e.g., `main`).
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `python bot.py`
4.  **Add Environment Variables:**
    *   Click on the "Environment" tab.
    *   Add the following variables:
        *   `API_ID`: Your Telegram API ID.
        *   `API_HASH`: Your Telegram API hash.
        *   `BOT_TOKEN`: Your Telegram bot token.
5.  **Deploy:** Click on the "Create Web Service" button.

## VPS (Virtual Private Server)

1.  **Connect to your VPS:** Use SSH to connect to your server.
2.  **Install Dependencies:**
    *   **Python:** Make sure you have Python 3.8 or higher installed.
    *   **Git:** Install Git if it's not already installed.
    *   **pip:** Install pip for Python 3.
3.  **Clone the Repository:**
    ```
    git clone https://github.com/your-username/video-converter-bot.git
    cd video-converter-bot
    ```
4.  **Install Python Dependencies:**
    ```
    pip3 install -r requirements.txt
    ```
5.  **Set Environment Variables:**
    *   It's recommended to use a `.env` file or export the variables directly in your shell.
    *   **Example using `.env`:**
        *   Create a `.env` file: `touch .env`
        *   Add your credentials to the `.env` file:
            ```
            API_ID=your_api_id
            API_HASH=your_api_hash
            BOT_TOKEN=your_bot_token
            ```
        *   You will need to modify `config.py` to load these variables from the `.env` file using a library like `python-dotenv`.
    *   **Example exporting variables:**
        ```
        export API_ID=your_api_id
        export API_HASH=your_api_hash
        export BOT_TOKEN=your_bot_token
        ```
6.  **Run the Bot:**
    *   **In the foreground:**
        ```
        python3 bot.py
        ```
    *   **In the background (using `nohup`):**
        ```
        nohup python3 bot.py &
        ```
    *   **Using a process manager (like `pm2` or `systemd`):** This is the recommended way to run the bot in production. It will automatically restart the bot if it crashes.
