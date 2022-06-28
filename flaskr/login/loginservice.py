import os

import requests as requests
from flask_login import login_user, login_manager

from flaskr.base import Session
from .user import User, FlaskUser
from oauthlib.oauth2 import WebApplicationClient


# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# @login_manager.user_loader
def load_user(user_id):
    session = Session()
    u = session.query(User).filter(User.gid == user_id).first()
    if u:
        print(u)
        return FlaskUser(user_id, u.name, u.email, u.profile_pic)
    return None


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def load_user_from_request(request):
    print("log from request")

    body = request.data.decode("UTF-8")
    print(body)
    if not body:
        return None

    # Parse the tokens!
    # tokens = token_response.json()
    # print(tokens)
    client.parse_request_body_response(body)

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = get_google_provider_cfg()["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = FlaskUser(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.

    session = Session()
    u = session.query(FlaskUser).get(unique_id)

    if not u:
        session.add(user)
        session.commit()
        print("Dodaje " + user)
    else:
        print("użytkownik jest w bazie")
    login_user(user)
    return user

    # Begin user session by logging the user in
    # login_user(user)
    # print("Zalogowano")
    # Send user back to homepage
    # return ""
