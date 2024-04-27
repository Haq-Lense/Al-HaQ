from flask import Flask
from flask import request

class Profile:
    """
    Represents a user profile.

    Attributes:
        userID (int): The unique identifier of the user.
        name (str): The name of the user.
        username (str): The username of the user.
        follower_of (str): The user that this profile follows.
        declared_location (str): The location declared by the user.
        tweets_count (int): The number of tweets made by the user.
        followers_count (int): The number of followers of the user.
        friend_count (int): The number of friends of the user.
        score (float): The score of the user profile from 0 to 100 (default is -1.0).
        posts (list): A list of posts made by the user (default is empty).
    """

    def __init__(self, user_id, name, username, follower_of, declared_location, tweets_count, followers_count, friend_count):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.follower_of = follower_of
        self.declared_location = declared_location
        self.tweets_count = tweets_count
        self.followers_count = followers_count
        self.friend_count = friend_count
        self.score = -1.0; # -1 is an invalid score and means that the score has not been calculated yet
        self.posts = []
        self.posts_true_or_not = []
        
    def create_profiles_from_database(profiles_database, posts_database):
        """
        Creates and populates profiles from a database.

        Returns:
            None
        """
        # Iterate over the database data and create profile objects
        for data in profiles_database:
            user_id = data.get('user_id')
            name = data.get('name')
            username = data.get('username')
            follower_of = data.get('follower_of')
            declared_location = data.get('declared_location')
            tweets_count = data.get('tweets_count')
            followers_count = data.get('followers_count')
            friend_count = data.get('friend_count')
            profile = Profile(user_id, name, username, follower_of, declared_location, tweets_count, followers_count, friend_count)
            profiles.append(profile)
            

        # Determine if the posts are true or not
        for post in profile.posts:
            true_or_not(post)

        return

profiles = []
app = Flask(__name__)

def user_exists(user_id):
    """
    Check if a user with the given user_id exists in the profiles list.

    Args:
        user_id (int): The ID of the user to check.

    Returns:
        bool: True if a user with the given user_id exists, False otherwise.
    """
    for profile in profiles:
        if profile.user_id == user_id:
            return True
    return False

def get_user_score(user_id):
    """
    Get the score for a given user ID.

    Parameters:
    user_id (int): The ID of the user.

    Returns:
    int: The score of the user. Returns -1 if the user ID is not found.
    """
    for profile in profiles:
        if profile.user_id == user_id:
            return profile.score
    return -1

@app.route('/getScore', methods=['GET'])
def get_score():
    """
    Retrieves the score for a user based on the provided data.

    Returns:
        int: The score of the user (Adds given profile and returns -1.0 if no score available).
    """
    data = request.get_json()
    user_id = data.get('user_id')
    if(user_exists(user_id)):
        return get_user_score(user_id)
    name = data.get('name')
    username = data.get('username')
    follower_of = data.get('follower_of')
    declared_location = data.get('declared_location')
    tweets_count = data.get('tweets_count')
    followers_count = data.get('followers_count')
    friend_count = data.get('friend_count')
    profile = Profile(user_id, name, username, follower_of, declared_location, tweets_count, followers_count, friend_count)
    profiles.append(profile)
    return -1.0

@app.route('/addPost', methods=['POST'])
def add_post():
    """
    Adds a post under a certain profile.

    Returns:
        str: A success message if the post is added successfully.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    post_content = data.get('post_content')

    for profile in profiles:
        if profile.user_id == user_id:
            profile.posts.append(post_content)
            
            calculate_score(profile)
            return "Post added successfully."

    return "User not found."

if __name__ == '__main__':
    app.run()