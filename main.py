from flask import Flask, render_template, request, url_for, redirect, send_from_directory,session,g
from datetime import datetime
import praw
import soundfile as sf
import numpy as np
import os
import json
from speech_creator import execute_speech
from video_creator import execute_ffmpeg
from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_oauth2 import current_token
from functools import wraps
from dotenv import load_dotenv
import ngrok
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user



app = Flask(__name__)

load_dotenv(dotenv_path='.env')


appConf={
    "client_id": os.getenv('CLIENT_ID'),
    "client_secret": os.getenv('CLIENT_SECRET'),
    "redirect_uri": "http://localhost:5000/callback",
    "metadata_url": "https://accounts.google.com/.well-known/openid-configuration"
}

oauth=OAuth(app)

myApp=oauth.register("Automated_Memer",
               client_id=appConf["client_id"],
               client_secret=appConf["client_secret"],
               server_metadata_url=appConf["metadata_url"],
               client_kwargs={"scope": "email"}
               )

AUTHLIB_INSECURE_TRANSPORT=True

login_manager = LoginManager(app)
login_manager.login_view = 'google_login'

@login_manager.user_loader
def load_user(user_id):
    # Load user from the session, or return None if the user ID is not valid
    return User(user_id)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


def require_oauth_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_token' not in session:
            return redirect(url_for('google_login'))
        return func(*args, **kwargs)
    return decorated_function


with app.app_context():     
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    @app.context_processor
    def inject_year():
        year = datetime.now().year
        return {'year': year}

    @app.route('/')
    def home():
        return render_template("index.html")   
    
    @app.route('/google_login')
    def google_login():
        return oauth.Automated_Memer.authorize_redirect(redirect_uri=url_for('callback', _external=True), scope=myApp.client_kwargs['scope'])
                   
    @app.route('/callback')
    def callback():
        token = myApp.authorize_access_token()
        session['token'] = token

        # Fetch user information using the obtained access token
        user_info = myApp.get('https://www.googleapis.com/oauth2/v2/userinfo')

        # Access user's name and email
        user_email = user_info.json().get('email')
        session['user_email'] = user_email
        user = User(user_email)
        login_user(user)
        os.makedirs(f'static/UserData/{user_email}', exist_ok=True)

        return redirect(url_for('welcome'))   
    

    @app.route('/welcome', methods=['GET', 'POST'])
    @login_required
    def welcome():
    
        if request.method == 'POST':
            link = request.form.get('link')
            voice= request.form.get('voice')
            session['link'] = link  # store link in session
            session['voice'] = voice
            return redirect(url_for('meme_link'))
        return render_template("welcome.html")
    
    
    @app.route('/meme_link')
    @login_required
    def meme_link(): 
        execute_speech()    
        return redirect(url_for('Audio'))
    
    
    @app.route("/Audio",methods=["POST","GET"])
    @login_required
    def Audio():
        user_email=session.get("user_email")
        if request.method == 'POST':
            execute_ffmpeg()
            return redirect(url_for('final_video'))
        return render_template("Audio.html",user_email=user_email)
    
    
    @app.route("/delete", methods=["DELETE"])
    def delete():
        body = request.json
        user_email=session.get("user_email")
        os.remove(f'static/UserData/{user_email}/Audio/{body["commentId"]}.mp3')
        os.remove(f'static/UserData/{user_email}/screenshots/{body["commentId"]}.jpg')
        pass
           
        
    @app.route("/final_video",methods=["POST","GET"])
    @login_required
    def final_video():
        user_email=session.get("user_email")
        return render_template("final_video.html",user_email=user_email)
    
    @app.route("/upload", methods=["POST","GET"])
    def upload():
        if os.path.exists("static/Audio/combined.mp3"):
            os.remove("static/Audio/combined.mp3")
        for comment in os.listdir("static/Audio"):
            os.remove(f'static/Audio/{comment}')
            os.remove(f'static/screenshots/final_screenshots/{comment.replace(".mp3",".jpg")}')
        return render_template("upload.html")


    @app.route('/logout')
    def logout():
        session.clear()
        logout_user()
        return redirect(url_for('home'))
    

    if __name__ == "__main__":
        app.run(debug=True)
