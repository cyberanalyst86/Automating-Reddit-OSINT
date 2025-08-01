import praw  # The Python Reddit API Wrapper
import datetime

# Function to convert time to required format
def convert_timestamp_to_datetime(timestamp: float) -> str:
    """
    Converts a Unix timestamp to a human-readable datetime string.

    Args:
        timestamp (float): The Unix timestamp.

    Returns:
        str: A formatted datetime string (e.g., "YYYY-MM-DD HH:MM:SS UTC").
    """
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

# Function to get posts from subreddits
def get_reddit_posts_with_search( days_to_filter, reddit_creds_file, subreddit_name: str, search_query: str, limit: int):
    CLIENT_ID = reddit_creds_file['client_id']
    CLIENT_SECRET = reddit_creds_file['client_secret']
    USERNAME = reddit_creds_file['username']
    PASSWORD = reddit_creds_file['password']
    USER_AGENT = reddit_creds_file['user_agent']

    """
    Connects to Reddit API and performs a search within a specified subreddit
    for posts matching a given query.

    Args:
        subreddit_name (str): The name of the subreddit (e.g., "cybersecurity").
        search_query (str): The keyword or phrase to search for within the subreddit.
                            Reddit's search will look in both title and content.
        limit (int): The maximum number of search results to retrieve.

    Returns:
        list: A list of dictionaries, each representing a post with its title, URL,
              score, number of comments, creation date, and content (selftext).
              Returns an empty list if an error occurs.
    """

    cutoff_timestamp = (
            datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days_to_filter)).timestamp()


    try:
        # Initialize Reddit instance for authentication
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            username=USERNAME,
            password=PASSWORD
        )

        print(f"Searching for '{search_query}' in r/{subreddit_name}...")

        subreddit = reddit.subreddit(subreddit_name)
        posts_data = []

        # Use subreddit.search() to find posts matching the query
        # 'sort' can be 'relevance', 'hot', 'top', 'new', 'comments'
        # 'time_filter' can be 'all', 'day', 'hour', 'month', 'week', 'year'
        # for submission in subreddit.search(query=search_query, limit=limit, sort='relevance'):

        for submission in subreddit.search(query=search_query, limit=limit, sort='new'):
            # Get the creation date and convert it to a readable format

            if submission.created_utc >= cutoff_timestamp:


                created_date = convert_timestamp_to_datetime(submission.created_utc)

                # Get the selftext (content) of the post; if it's a link post, selftext will be empty
                post_content = submission.selftext if submission.selftext else "[No selftext content for this post]"

                reddit_link = "https://www.reddit.com" + str(submission.permalink)


                posts_data.append({
                    "subreddit" : subreddit_name,
                    "query" :  search_query,
                    "title": submission.title,
                    "reddit_link": reddit_link,
                    "url": submission.url,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "created_date": created_date,
                    'created_utc': submission.created_utc,
                    "content": post_content
                })

            else:

                #print(f"No posts found matching '{SEARCH_QUERY}' within the last {days_to_filter} days.")
                continue


        print(f"Successfully fetched {len(posts_data)} posts matching '{search_query}' from r/{subreddit_name}.")

        return posts_data

    except praw.exceptions.RedditAPIException as e:
        print(f"Reddit API Error: {e}")
        print("Please check your API credentials and ensure they are correct.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
