import json

import requests
from flask import Blueprint, redirect, request, url_for, make_response, Response
from flask_login import current_user, login_user, logout_user
from pip._internal import req

from flaskr.base import Session
from flaskr.login import loginservice
from flaskr.login.user import User, FlaskUser

bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route("", methods=['GET'])
def home_page():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/login/logout">Logout</a>'
            '<a class="button" href="/login/login">Google Login</a>'
                '<a href="https://127.0.0.1:5000/card/random/10">karty</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login/login">Google Login</a>'


@bp.route("login", methods=['GET'])
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = loginservice.get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = loginservice.client.prepare_request_uri(
        authorization_endpoint,
        #  TODO OGarnąć to
        redirect_uri="https://127.0.0.1:5000/login/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@bp.route("callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    print(code)

    google_provider_cfg = loginservice.get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = loginservice.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(loginservice.GOOGLE_CLIENT_ID, loginservice.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    tokens = token_response.json()
    print(tokens)
    loginservice.client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = loginservice.client.add_token(userinfo_endpoint)
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
    fuser = FlaskUser(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    session = Session()
    u = session.query(User).filter(User.gid == unique_id).first()

    # print("test " + u)
    if not u:
        user = User(gid=unique_id, name=users_name, email=users_email, profile_pic=picture)
        session.add(user)
        session.commit()
        print("Dodaje " + user.name)
    else:
        print("użytkownik jest w bazie")
    if login_user(fuser):
        print("login fucking user " + fuser.name)
    else:
        print("shit")

    # Send user back to homepage

    # response = make_response(token_response.json(), 200)
    # response.mimetype = "text/plain"
    # return response
    # return token_response
    return Response(response=json.dumps(token_response.json()), status=200, mimetype="application/json")
    # return Response(json.dumps(token_response.json()), status=201, mimetype='application/json')

    # return "asd"
    # return token_response.json()


@bp.route("logout", methods=['GET'])
def logout():
    logout_user()
    return redirect("/")
