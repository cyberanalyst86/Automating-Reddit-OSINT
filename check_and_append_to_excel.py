import pandas as pd
import os
from alert_to_telegram import *

def check_and_append_to_excel(new_data_row):
    excel_path = "reddit_posts.xlsx"
    key_column = "title"

    """
    Checks if a row of data exists in an Excel file based on a specific key column.
    If the data does not exist, it appends the new data to the Excel file.

    Args:
        excel_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet to read/write.
        new_data_row (dict): A dictionary representing the new row of data to potentially append.
                             Keys should match column names in the Excel file.
        key_column (str): The name of the single column to use as the key for checking existence.
                            If a row with the same value in this column exists,
                            the new data is considered to already exist.
    """
    try:
        # Check if the Excel file exists
        if os.path.exists(excel_path):
            # Read the existing Excel file into a DataFrame
            # header=0 assumes the first row is the header
            df = pd.read_excel(excel_path, header=0)
            #print(f"Existing data loaded from '{excel_path}' (sheet: '{sheet_name}'):")
            #print(df)
        else:
            # If the file doesn't exist, create an empty DataFrame with column names
            # from new_data_row to ensure schema consistency.
            df = pd.DataFrame(columns=list(new_data_row.keys()))
            #print(f"'{excel_path}' does not exist. Creating a new DataFrame.")

        # Convert new_data_row to a DataFrame for easier appending later
        new_df_row = pd.DataFrame([new_data_row])

        # Flag to track if data exists
        data_exists = False

        # If the DataFrame is not empty, perform the existence check
        if not df.empty:
            # Check if the key_column exists in the DataFrame's columns
            if key_column not in df.columns:
                raise KeyError(f"Key column '{key_column}' not found in the Excel file's columns.")

            # Check if the value in the specified key_column of new_data_row
            # already exists in the corresponding column of the DataFrame.
            # .isin() is efficient for checking if a value is present in a Series.
            # .any() checks if any of the matches is True.
            data_exists = (df[key_column] == new_data_row[key_column]).any()

        if data_exists:
            print(f"\nData with '{key_column}' = '{new_data_row[key_column]}' already exists. No new data appended. \n")
            print("Telegram message not sent")
        else:
            # If data does not exist, append the new row to the DataFrame
            # use pd.concat for appending DataFrames
            post = new_data_row

            Subreddit = post['subreddit']
            Query = post['query']
            Title = post['title']
            Reddit_Link = post['reddit_link']
            URL = post['url']
            Score = post['score']
            Comments = post['num_comments']
            Created_Date = post['created_date']
            Content = post["content"]

            notification_message =  "~~~Reddit~~~\n\n"\
                                    "Subreddit: " + str(Subreddit) + "\n\n" + \
                                    str(Title) + " \n\n" + \
                                   "search keyword: " + str(Query) + " \n\n" + \
                                    str(Created_Date) + " \n\n" + \
                                    str(URL) + " \n\n" + \
                                    str(Reddit_Link) + " \n\n" + \
                                    "Score: " + str(Score) + " \n\n" + \
                                    "Comments: " + str(Comments) + " \n\n" + \
                                    "Content: " + str(Content) + " \n\n" + \
                                    "-" * 20 + "\n"

            alert_to_telegram(notification_message)


            df = pd.concat([df, new_df_row], ignore_index=True)
            print("\nNew data appended to the DataFrame.")

            # Save the updated DataFrame back to the Excel file
            # index=False prevents pandas from writing the DataFrame index as a column
            df.to_excel(excel_path, index=False)
            #print(f"Updated data saved to '{excel_path}' (sheet: '{sheet_name}'):")
            #print(df)

    except FileNotFoundError:
        print(f"Error: The file '{excel_path}' was not found.")
    except KeyError as e:
        print(f"Error: {e}. Please ensure the 'key_column' is present in your Excel file and 'new_data_row'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return