import os
import configparser

# Get credentials from config file
def get_credentials_from_file(config_file="reddit_config.ini"):
    """
    Retrieves Reddit API credentials from a specified configuration file.
    Useful for local development environments where environment variables
    might be less convenient. Ensure the config file is NOT committed
    to version control.
    """
    #print(f"\n--- Attempting to retrieve credentials from '{config_file}' ---")
    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        print(f"ERROR: Configuration file '{config_file}' not found.")
        print("Please create a 'config.ini' file as described in the comments.")
        return None

    try:
        config.read(config_file)
        if 'reddit_api' in config:
            client_id = config['reddit_api']['client_id']
            client_secret = config['reddit_api']['client_secret']
            username = config['reddit_api']['username']
            password = config['reddit_api']['password']
            user_agent = config["reddit_api"]['user_agent']

            #print(f"Successfully retrieved credentials from '{config_file}'.")
            return {
                "client_id": client_id,
                "client_secret": client_secret,
                "username": username,
                "password": password,
                "user_agent": user_agent
            }
        else:
            print(f"ERROR: Section '[reddit_api]' not found in '{config_file}'.")
            return None
    except KeyError as e:
        print(f"ERROR: Missing key in '{config_file}' under [reddit_api]: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading '{config_file}': {e}")
        return None