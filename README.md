1.) Please install the required python libraries specified in requirements.txt (pip install -r requirements.txt).

2.) If error is encountered when installing the required dependencies, please use do the following: pip install praw, pip install configparser, pip install pandas and pip install telebot.

3.) You will need to have or create the following in order for the program to work: reddit api key, telegram bot and bot token and telegram channel or group id (chat_id) which you want to send notification to. The reddit_config.ini file will be used to store the credentials (e.g. api key). 

4.) The program searches Reddit for keywords and identifies relevant posts within 7 days (can be adjusted within reddit_monitor(main).py) from the instance the program is ran. 

5.) The main program to run is reddit_monitor(main).py which will call functions from the rest of the python files in the code repository.

6.) Keywords are to be added to search_query_keywords.txt which the program will query. 

7.) Subreddits are to be added to subreddits_list.txt which the program will query.

8.) The excel file (reddit_posts.xlsx) acts as a database to store reddit posts so same post does not get alerted to your Telegram group.

9.) Please take note that this is a very basic program, feel free to make modification according to your needs and provide feedback.
