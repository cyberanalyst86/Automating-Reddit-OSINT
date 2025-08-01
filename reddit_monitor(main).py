from get_subreddits import *
from get_search_query_keywords import *
from get_credentials_from_file import *
from get_reddit_posts import *
from check_and_append_to_excel import *

if __name__ == "__main__":

    # Specify the number of posts to retrieve (limit for search results)
    LIMIT = 20  # You can change this to any number (e.g., 25, 50, etc.)

    SUBREDDIT_LIST = get_subreddits()

    # List the keywords to search for within the subreddit
    SEARCH_QUERY_LIST = get_search_query_keywords()

    # Define your date filter
    # Example: posts from the last 7 days
    days = 7
    days_to_filter = days + 1

    reddit_creds_file = get_credentials_from_file()

    if reddit_creds_file:

        df_list = []

        for SUBREDDIT_NAME in SUBREDDIT_LIST:

            for SEARCH_QUERY in SEARCH_QUERY_LIST:

                # Call the function to get posts matching the search query
                cybersecurity_aviation_posts = get_reddit_posts_with_search(days_to_filter, reddit_creds_file, SUBREDDIT_NAME,
                                                                            SEARCH_QUERY, LIMIT)
                for posts in cybersecurity_aviation_posts:

                    check_and_append_to_excel(posts)

    else:
        print("\nCould not load credentials from config.ini.")




