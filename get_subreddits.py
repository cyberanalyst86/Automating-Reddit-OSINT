def get_subreddits():

    with open('subreddits_list.txt', 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    return lines

