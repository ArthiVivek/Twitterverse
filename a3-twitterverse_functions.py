"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this 
          user is following (a list of str)
       
Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)
       
"""

def process_data (data_file):
    """ (file open for reading) -> Twitterverse dictionary
    
    Read data_file and return information in the Twitterverse dictionary format.
    """
    twitter_file = data_file.readlines()
    twitter_dict = {}
    
    x = 0
    
    while x < (len(twitter_file) - 1):
        small_dict = {}
        small_dict['name'] = twitter_file[x + 1].strip('\n')
        small_dict['location'] = twitter_file[x + 2].strip('\n') 
        small_dict['web'] = twitter_file[x + 3].strip('\n') 

        n = x + 4 
        biography = ""

        while twitter_file[n] != 'ENDBIO\n': 
            biography += twitter_file[n]
            n += 1
        small_dict['bio'] = biography

        n += 1
        following_list = []
        while twitter_file[n] != 'END\n'and n < len(twitter_file) - 1:  
            following_list.append(twitter_file[n].strip('\n'))
            n += 1

        n += 1        
        small_dict['following'] = following_list
    
        username = twitter_file[x].strip('\n')
        twitter_dict[username] = small_dict
        x = n
        
    return twitter_dict 

def process_query(query_file): 
    """ (file open for reading) -> query dictionary
    
    Read query_file and return information in the query dictionary format.
    """
    query_data = query_file.readlines()
    query_dict = {}
    x = 1 
    search_dict = {}
    search_dict['username'] = query_data[x].strip('\n')
    x += 1
    operation_list = []
    
    while query_data[x] != 'FILTER\n': 
        operation_list.append(query_data[x].strip('\n'))
        x += 1
    
    search_dict['operations'] = operation_list  
    query_dict['search'] = search_dict 
    x += 1
    
    filter_dict = {}
    filter_format(filter_dict, query_data, 'name-includes', x)
    filter_format(filter_dict, query_data, 'location-includes', x)
    filter_format(filter_dict, query_data, 'follower', x)
    filter_format(filter_dict, query_data, 'following', x)
    query_dict['filter'] = filter_dict
    
    present_dict = {}
    sort_by = query_data[-2].strip('sort-by ')
    present_dict['sort-by'] = sort_by.strip('\n')
    
    format_type = query_data[-1].lstrip('format ')
    present_dict['format'] = format_type
    query_dict['present'] = present_dict
  
    return query_dict
    
def filter_format(filter_dict, query_data, filter_type, index): 
    """ (dict, list, str, int) -> dict
    
    Return a dict with key filter_type of query_data given the index. 
    """ 
        
    filter_list = ''
    count = 0 
     
    while query_data[index] != 'PRESENT\n': 
        if filter_type in query_data[index]: 
            count += 1
            filter_keyword = query_data[index].strip(filter_type)
            filter_list = (filter_keyword.strip('\n'))
                               
        index += 1 
        
    if count > 0: 
        filter_dict[filter_type] = filter_list
    return filter_dict 
    
def all_followers(twitter_dict, twitter_name): 
    """ (Twitterverse dictionary, str) -> list of str
    
    Return a list of all users following twitter_name in twitter_dict.
    
    >>> twitter_file = open('data.txt', 'r') 
    >>> twitter_dictionary = process_data(twitter_file) 
    >>> all_followers(twitter_dictionary, 'NicoleKidman') 
    ['PerezHilton', 'q', 'p', 'tomCruise']
    
    >>> twitter_file = open('data.txt', 'r') 
    >>> twitter_dictionary = process_data(twitter_file) 
    >>> all_followers(twitter_dictionary, 'katieH') 
    ['PerezHilton', 'tomCruise']
    """ 
    
    following_list = []
    for user in twitter_dict:
        f_list = twitter_dict[user]['following']
        if twitter_name in f_list:
            following_list.append(user) 
    return following_list 

def get_search_results(twitter_dict, search_dict): 
    """ (Twitterverse dictionary, search specification dictionary) -> list of 
    str
    
    Return a list of users from twitter_dict that fit the specification declared
    by search_dict.
    
    >>> data_file = open('data.txt', 'r') 
    >>> twitter_dict = process_data(data_file) 
    >>> query_file = open('query3.txt', 'r') 
    >>> query_dict = process_query(query_file) 
    >>> search_dict = query_dict['search']
    >>> get_search_results(twitter_dict, search_dict) 
    ['PerezHilton', 'tomCruise', 'q', 'p']
    
    >>> data_file = open('data.txt', 'r') 
    >>> twitter_dict = process_data(data_file) 
    >>> query_file = open('query2.txt', 'r') 
    >>> query_dict = process_query(query_file) 
    >>> search_dict = query_dict['search']
    >>> get_search_results(twitter_dict, search_dict)
    ['a', 'b']
    """

    search_list = [search_dict['username']] 
    search_specified_list = []

    for user in search_list:
        search_users_list = [user]
        
        for operation in search_dict['operations']:
            search_users_list = search_helper(search_users_list, operation,\
            twitter_dict)
        
        search_specified_list += search_users_list
    
    return search_specified_list  

def search_helper(name_list, operation, twitter_dict):
    """ (list of str, str, twitterverse dictionary) -> list of str 
    
    Return the list of users that result from operation having applied to 
    name_list from the twitter_dict. 
    
    >>> data_file = open('data.txt', 'r') 
    >>> twitter_dict = process_data(data_file)
    >>> query_file = open('query3.txt', 'r') 
    >>> query_dict = process_query(query_file) 
    >>> search_dict = query_dict['search']
    >>> search_list = [search_dict['username']]
    >>> operation = 'following'
    >>> search_helper(search_list, operation, twitter_dict)
    ['katieH', 'NicoleKidman']
    
    >>> data_file = open('data.txt', 'r') 
    >>> twitter_dict = process_data(data_file)
    >>> query_file = open('query2.txt', 'r') 
    >>> query_dict = process_query(query_file) 
    >>> search_dict = query_dict['search']
    >>> search_list = [search_dict['username']]
    >>> operation = 'followers'
    >>> search_helper(search_list, operation, twitter_dict)
    ['PerezHilton', 'tomfan']
    """ 
    return_list = []
                                  
    for name in name_list:
        if operation == 'following':
            search_specified_list = twitter_dict[name]['following']
            for following_names in search_specified_list: 
                if following_names not in return_list: 
                    return_list.append(following_names)  
                    
        elif operation == 'followers':
            followers = all_followers(twitter_dict, name)
            for followers_name in followers: 
                if followers_name not in return_list: 
                    return_list.append(followers_name) 
    
    return return_list

def get_filter_results(twitter_dict, username_list, filter_dict):
    """ (Twitterverse dictionary, list of str, filter specification dictionary) 
    -> list of str
    
    >>> data_file = open('data.txt', 'r') 
    >>> twitter_dict = process_data(data_file)
    >>> query_file = open('query2.txt', 'r') 
    >>> query_dict = process_query(query_file) 
    >>> username_list = get_search_results(twitter_dict, search_dict)
    >>> filter_dict = query_dict['filter']
    >>> get_filter_results(twitter_dict, username_list, filter_dict)
    
    """
    twitter_handles = username_list 
    name_filtered_list = []
    upper_user = []
    
    if 'name_includes' in filter_dict: 
        for user in twitter_handles: 
            user = user.upper()
            upper_user.append(user)
        name = filter_dict['name_includes']
            
        for uName in username_list:
            if name.upper() == uName.upper():
                name_filtered_list.append(name) 
                
        twitter_handles = name_filtered_list   
            
    location_filtered_list = []
    if 'location_includes' in filter_dict: 
        for user in twitter_handles: 
            location = filter_dict['location_includes']
            if location.upper() == twitter_dict[user]['location'].upper(): 
                location_filtered_list.append(user) 
        twitter_handles = location_filtered_list
            
    follower_filtered_list = []
    if 'follower' in filter_dict:
        for user in twitter_handles:
            for follower in twitter_dict[user]['following']:
                if follower == filter_dict['follower']:
                #if follower in twitter_handles:
                    follower_filtered_list.append(user)
                    
        twitter_handles = follower_filtered_list 
            
    following_filtered_list = []
    if 'following' in filter_dict:
        for user in twitter_handles: 
            following_list = all_followers(twitter_dict, user)
            for follower in following_list: 
                if follower in twitter_handles: 
                    following_filtered_list.append(follower) 
        twitter_handles = following_filtered_list 
    
    return twitter_handles 

def get_present_string(twitter_dict, final_list, present_dict): 
    """ (Twitterverse dictionary, list of str, presentation specification
    dictionary) -> str
    
    Return final_list of users from twitter_dict in the order and format as 
    indicated by present_dict. 
    
    >>> data_file = open('data.txt', 'r') 
    >>> twitter_dict = process_data(data_file)
    >>> query_file = open('query2.txt', 'r') 
    >>> query_dict = process_query(query_file) 
    >>> username_list = get_search_results(twitter_dict, search_dict)
    >>> filter_dict = query_dict['filter']
    >>> final_list = get_filter_results(twitter_dict, username_list, 
    filter_dict)
    >>> present_dict = query_dict['present']
    >>> get_present_string(twitter_dict, final_list, present_dict)
    """ 
    
    if present_dict['sort-by'] == 'username':
        tweet_sort(twitter_dict, final_list, username_first)
        
    if present_dict['sort-by'] == 'name':
        tweet_sort(twitter_dict, final_list, name_first) 
        
    if present_dict['sort-by'] == 'popularity':
        tweet_sort(twitter_dict, final_list, more_popular) 
    
    present_output = ''
    format_long = ''
    format_short = []
    
    if 'long' in present_dict['format']:
       
        for user in final_list: 
            website = twitter_dict[user]["web"]
            bio = '\n' + twitter_dict[user]["bio"]
            if("web" in twitter_dict[user]):
                website = twitter_dict[user]["web"]
            format_long = ('----------\n' + user + '\n' + 'name: ' +\
                           twitter_dict[user]['name'] + '\n' + 'location: ' +\
                           twitter_dict[user]['location'] + '\n' + 'website: '\
                           + website + '\n' + 'bio:' + bio + '\n' +\
                           'following: '+\
                           str(twitter_dict[user]['following']) + '\n') 
            present_output += format_long
            
        present_output += '----------'
    elif 'short' in present_dict['format']: 
        present_output = str(final_list) 
    
    return present_output

# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType
    
    Sort the results list using the comparison function cmp and the data in 
    twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """
    
    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1 
        results[position] = current  
            
def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return -1 if user a has more followers than user b, 1 if fewer followers, 
    and the result of sorting by username if they have the same, based on the 
    data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """
    
    a_popularity = len(all_followers(twitter_data, a)) 
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)
    
def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return 1 if user a has a username that comes after user b's username 
    alphabetically, -1 if user a's username comes before user b's username, 
    and 0 if a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """
    
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
        
    Return 1 if user a's name comes after user b's name alphabetically, 
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """
    
    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)       


if __name__ == '__main__':
    data_file = open('data.txt', 'r') 
    twitter_dict = process_data(data_file) 
    query_file = open('query1.txt', 'r') 
    query_dict = process_query(query_file) 
    search_dict = query_dict['search']
    #print(get_search_results(twitter_dict, search_dict) )
    
    username_list = get_search_results(twitter_dict, search_dict)
    filter_dict = query_dict['filter']
    final_list = get_filter_results(twitter_dict, username_list, filter_dict)
    present_dict = query_dict['present']
    #print (query_dict['present']['format'])
    get_present_string(twitter_dict, final_list, present_dict)
    print(get_present_string(twitter_dict, final_list, present_dict))
    