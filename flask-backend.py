from flask import Flask
from flask import request

class Profile:
    """
    Represents a user profile.

    Attributes:
        user_id (int): The unique identifier of the user.
        name (str): The name of the user.
        follower_of (str): The user that this profile follows.
        tweets_count (int): The number of tweets made by the user.
        score (float): The score of the user profile from 0 to 100 (default is -1.0).
        posts (list): A list of posts made by the user (default is empty).
    """

    def __init__(self, user_id, name, follower_of, tweets_count):
        """
        Initializes a new instance of the Profile class.

        Args:
            user_id (int): The unique identifier of the user.
            name (str): The name of the user.
            follower_of (str): The user that this profile follows.
            tweets_count (int): The number of tweets made by the user.
        """
        self.user_id = user_id
        self.name = name
        self.follower_of = follower_of
        self.tweets_count = tweets_count
        self.score = -1.0  # -1 is an invalid score and means that the score has not been calculated yet
        self.posts = []
        self.posts_true_or_not = []

    @staticmethod
    def create_profiles_from_database(database):
        """
        Creates and populates profiles from a database.

        Args:
            database (list): A list of dictionaries representing profile data from the database.

        Returns:
            None
        """
        # Iterate over the database data and create profile objects
        for data in database:
            user_id = data.get('user_id')
            if not user_exists(user_id):
                name = data.get('name')
                follower_of = data.get('follower_of')
                tweets_count = data.get('tweets_count')
                profile = Profile(user_id, name, follower_of, tweets_count)
                profiles.append(profile)
            profile.posts.append(data.get('text'))

        # Determine if the posts are true or not by running the model
        for profile in profiles:
            for post in profile.posts:
                profile.posts_true_or_not.append(true_or_not(post))
            profile.score = calculate_score(profile)

        return

profiles = []
app = Flask(__name__)

def user_exists(user_id):
    """
    Check if a user with the given user_id exists in the profiles list.

    Args:
        user_id (int): The ID of the user to check.

    Returns:
        Union[Profile, bool]: The profile object if a user with the given user_id exists, False otherwise.
    """
    for profile in profiles:
        if profile.user_id == user_id:
            return profile
    return False

def get_user_score(user_id):
    """
    Get the score for a given user ID.

    Parameters:
    user_id (int): The ID of the user.

    Returns:
    int: The score of the user. Returns -1.0 if the user ID is not found.
    """
    for profile in profiles:
        if profile.user_id == user_id:
            return profile.score
    return -1.0

def true_or_not(post):
    # TODO: Implement function that uses model to determine if a post is true or not
    return

def calculate_score(profile):
    # TODO: Implement function that calculates the score of a profile
    return

def new_post(post_content, profile):
    profile.posts.append(post_content)
    profile.posts_true_or_not.append(true_or_not(post_content))
    profile.score = calculate_score(profile)

@app.route('/getScore', methods=['GET'])
def get_score():
    """
    Retrieves the score for a user based on the provided data.

    Returns:
        int: The score of the user (Adds given profile and returns -1.0 if user does not exist).
    """
    data = request.get_json()
    user_id = data.get('user_id')
    if user_exists(user_id):
        return get_user_score(user_id)
    else:
        # If user not found, add the user to the profiles list
        name = data.get('name')
        follower_of = data.get('follower_of')
        tweets_count = data.get('tweets_count')
        post_content = data.get('text')
        profile = Profile(user_id, name, follower_of, tweets_count)
        profiles.append(profile)
        new_post(post_content, profile)
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
            new_post(post_content, profile)
            return "Post added successfully."

    return "User not found."

if __name__ == '__main__':
    app.run()