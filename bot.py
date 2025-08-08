import asyncio
import logging
import os
import random
import time
import math

from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import Config

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# In-memory storage for active conversions
active_conversions = {}

# Helper Functions

async def progress_for_pyrogram(
    current: int,
    total: int,
    ud_type: str,
    message: Message,
    start: float
):
    """
    Custom progress bar for Pyrogram.
    """
    user_id = message.chat.id
    if user_id not in active_conversions:
        # If the conversion was canceled, stop the progress bar
        bot.stop_transmission()
        return

    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff)
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        time_to_completion_str = time.strftime("%H:%M:%S", time.gmtime(time_to_completion))

        progress = "[{0}{1}] \n**Progress**: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "**Total Size**: {0}\n**Completed**: {1}\n**Speed**: {2}/s\n**ETA**: {3}\n".format(
            humanbytes(total),
            humanbytes(current),
            humanbytes(int(speed)),
            time_to_completion_str
        )

        try:
            await message.edit(
                text=f"{ud_type}\n{tmp}"
            )
        except:
            pass

def humanbytes(size: int | float) -> str:
    """
    Converts bytes to a human-readable format.
    """
    if not size:
        return ""
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"

async def take_screen_shot(video_file: str, output_directory: str, ttl: int):
    """
    Takes a screenshot of a video file.
    """
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = os.path.join(
        output_directory,
        f"{time.time()}.jpg"
    )
    if video_file.upper().endswith(("MKV", "MP4", "WEBM")):
        file_gen_cmd = [
            "ffmpeg",
            "-ss", str(ttl),
            "-i", video_file,
            "-vframes", "1",
            out_put_file_name
        ]
        #
        process = await asyncio.create_subprocess_exec(
            *file_gen_cmd,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
    else:
        # TODO: Add support for other file types
        return None
    
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

# Initialize the bot
bot = Client(
    "VideoConverterBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """
    Handles the /start command.
    """
    await message.reply_text(
        "**Welcome to the Video Converter Bot!**\n\n"
        "I can convert any video file into a streamable format.\n\n"
        "Simply send me a video file and I will do the rest.\n\n"
        "For more information, use the /help command."
    )

@bot.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """
    Handles the /help command.
    """
    await message.reply_text(
        "**Video Converter Bot Help**\n\n"
        "**How to use:**\n"
        "1. Send any video file to me.\n"
        "2. I will download it, convert it to a streamable format, and send it back to you.\n\n"
        "**Commands:**\n"
        "/start - Display the welcome message.\n"
        "/help - Display this help message.\n"
        "/cancel - Cancel the current operation."
    )

@bot.on_message(filters.command("cancel"))
async def cancel_command(client: Client, message: Message):
    """
    Handles the /cancel command.
    """
    user_id = message.from_user.id
    if user_id in active_conversions:
        status_message = active_conversions[user_id]
        del active_conversions[user_id]
        bot.stop_transmission()
        await status_message.edit_text("Process canceled.")
    else:
        await message.reply_text("You have no active process to cancel.")

@bot.on_message(filters.video | filters.document)
async def convert_video(client: Client, message: Message):
    """
    Handles incoming video files and converts them to a streamable format.
    """
    user_id = message.from_user.id
    if user_id in active_conversions:
        await message.reply_text("You already have an active process. Please wait for it to complete or use /cancel.")
        return

    if message.document:
        if not message.document.file_name:
            return
        if not message.document.file_name.split('.')[-1].lower() in Config.VIDEO_EXTENSIONS:
            return

    # Create download directory if it doesn't exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    # Download the video file
    status_message = await message.reply_text("Downloading your video...", quote=True)
    active_conversions[user_id] = status_message
    c_time = time.time()
    
    file_name = ""
    if message.video:
        file_name = message.video.file_name
    elif message.document:
        file_name = message.document.file_name

    downloaded_file_path = await client.download_media(
        message=message,
        file_name=os.path.join(Config.DOWNLOAD_LOCATION, file_name),
        progress=progress_for_pyrogram,
        progress_args=("Downloading...", status_message, c_time)
    )
    
    # Delete the original message
    await message.delete()

    if downloaded_file_path and isinstance(downloaded_file_path, str):
        await status_message.edit_text("Processing your video...")

        # Extract metadata
        duration = 0
        width = 0
        height = 0
        metadata = extractMetadata(createParser(downloaded_file_path))
        if metadata:
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")

        # Generate thumbnail
        thumbnail_path = None
        if duration > 0:
            screenshot_time = 10 if duration > 10 else 1
            thumbnail_path = await take_screen_shot(
                downloaded_file_path,
                Config.DOWNLOAD_LOCATION,
                screenshot_time
            )

        if thumbnail_path and os.path.exists(thumbnail_path):
            # Resize and save the thumbnail
            img = Image.open(thumbnail_path)
            img.resize((90, height))
            img.save(thumbnail_path, "JPEG")

        # Upload the converted video
        await status_message.edit_text("Uploading the converted video...")
        c_time = time.time()
        
        # Get the file name and caption
        file_name = ""
        if message.video:
            file_name = message.video.file_name
        elif message.document:
            file_name = message.document.file_name
            
        caption = f"{file_name}"
        if message.caption:
            caption = f"{file_name}\n\n{message.caption}"

        send_video_args = {
            "chat_id": message.chat.id,
            "video": downloaded_file_path,
            "duration": duration,
            "width": width,
            "height": height,
            "supports_streaming": True,
            "caption": caption,
            "progress": progress_for_pyrogram,
            "progress_args": ("Uploading...", status_message, c_time)
        }
        if thumbnail_path and os.path.exists(thumbnail_path):
            send_video_args["thumb"] = thumbnail_path

        await client.send_video(**send_video_args)

        # Clean up files
        await asyncio.sleep(2) # Add a delay to allow the OS to release file locks
        try:
            if os.path.exists(downloaded_file_path):
                os.remove(downloaded_file_path)
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
        except Exception as e:
            logger.error(f"Error cleaning up files: {e}")

        await status_message.delete()
    else:
        await status_message.edit_text("Failed to download the video.")

    if user_id in active_conversions:
        del active_conversions[user_id]


if __name__ == "__main__":
    bot.run()
