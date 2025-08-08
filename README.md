# Video Converter Bot

A simple Telegram bot that converts video files to a streamable format.

## Features

*   Converts non-streamable videos to a streamable format.
*   Supports a wide range of video formats.
*   Adds the original file name as a caption.
*   Deletes the original message after download.
*   Cleans up temporary files after conversion.

## Getting Started

### Prerequisites

*   Python 3.8 or higher
*   A Telegram API key and hash
*   A Telegram bot token

### Installation

1.  **Clone the repository:**
    ```
    git clone https://github.com/your-username/video-converter-bot.git
    cd video-converter-bot
    ```

2.  **Install the dependencies:**
    ```
    pip install -r requirements.txt
    ```

3.  **Configure the bot:**
    *   Rename `config.py.sample` to `config.py`.
    *   Open `config.py` and fill in your `API_ID`, `API_HASH`, and `BOT_TOKEN`.

4.  **Run the bot:**
    ```
    python bot.py
    ```

## Deployment

For detailed deployment instructions, see [DEPLOY.md](DEPLOY.md).
