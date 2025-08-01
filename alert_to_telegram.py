import telebot
import configparser
import os

def alert_to_telegram(message, config_file="reddit_config.ini"):

    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        print(f"ERROR: Configuration file '{config_file}' not found.")
        print("Please create a 'config.ini' file as described in the comments.")
        return None

    try:
        config.read(config_file)
        if 'reddit_api' in config:
            TOKEN = config['reddit_api']['telbot_token']
            chat_id = config['reddit_api']['telegram_chat_id']

        else:
            print(f"ERROR: Section '[reddit_api]' not found in '{config_file}'.")
            return None

    except KeyError as e:
        print(f"ERROR: Missing key in '{config_file}' under [reddit_api]: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred while reading '{config_file}': {e}")
        return None

    bot = telebot.TeleBot(TOKEN)

    bot.send_message(chat_id, message)

    return
