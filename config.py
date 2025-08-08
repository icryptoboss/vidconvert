import os

class Config(object):
    # Get these values from my.telegram.org
    API_ID = int(os.environ.get("API_ID", 25679601))
    API_HASH = os.environ.get("API_HASH", "105e12ce694578ac241c66d267caee87")

    # Get this value from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "1631815313:AAEWsWX6cY_gSo5TUzHsFxqVlYhs3_hEtdU")

    # The directory where downloaded files will be stored
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./downloads")

    # List of supported video extensions
    VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm', 'mpg', 'mpeg', '3gp', 'ts', 'm4v', 'f4v', 'vob']
