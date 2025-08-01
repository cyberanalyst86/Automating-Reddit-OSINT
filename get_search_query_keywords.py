def get_search_query_keywords():

    with open('search_query_keywords.txt', 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    return lines

