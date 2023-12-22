from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory,get_flashed_messages,session
from datetime import datetime
import praw
import soundfile as sf
import numpy as np
import os
import json
from speech_creator import execute_speech
from video_creator import execute_ffmpeg
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)


appConf={
    "client_id": "90823679653-4an32hnkfiecqh9t9fc4jbe4utudnl73.apps.googleusercontent.com",
    "client_secret": "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",
    "redirect_uri": "http://localhost:5000/callback",
    "metadata_url": "https://accounts.google.com/.well-known/openid-configuration"
}

oauth=OAuth(app)

myApp=oauth.register("Automated_Memer",
               client_id=appConf["client_id"],
               client_secret=appConf["client_secret"],
               server_metadata_url=appConf["metadata_url"],
               client_kwargs={"scope": "email https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.upload"}
               )

AUTHLIB_INSECURE_TRANSPORT=True

with app.app_context():     
    app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
    
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
        #token = oauth.Automated_Memer.authorize_access_token()
        #session['user_token'] = token
        flash('Success! You are logged in.', category='success')
        return redirect(url_for('welcome'))   
    

    @app.route('/welcome', methods=['GET', 'POST'])
    def welcome():
        if request.method == 'POST':
            link = request.form.get('link')
            voice= request.form.get('voice')
            session['link'] = link  # store link in session
            session['voice'] = voice
            return redirect(url_for('meme_link'))
        return render_template("welcome.html")
    
    
    @app.route('/meme_link')
    def meme_link():
        
        if( not os.path.exists("static/Audio/title.mp3") or not os.path.exists("static/screenshots/final_screenshots/title.jpg")):
            execute_speech()
            
        flash('Content Generated Successfully', category='success')    
        return redirect(url_for('Audio'))
    
    
    @app.route("/Audio",methods=["POST","GET"])
    def Audio():
        if request.method == 'POST':
            execute_ffmpeg()
            return redirect(url_for('final_video'))
        return render_template("Audio.html")
    
    
    @app.route("/delete", methods=["DELETE"])
    def delete():
        body = request.json
        os.remove(f'static/Audio/{body["commentId"]}.mp3')
        os.remove(f'static/screenshots/final_screenshots/{body["commentId"]}.jpg')
        pass
           
        
    @app.route("/final_video",methods=["POST","GET"])
    def final_video():
        T = os.path.exists("static/Final_Videos/Final_Video_2.mp4")
        if request.method == 'POST':
            return redirect(url_for('upload'))
        return render_template("final_video.html",T=T)
    
    @app.route("/upload", methods=["POST","GET"])
    def upload():
        for comment in os.listdir("static/Audio"):
            os.remove(f'static/Audio/{comment}')
            os.remove(f'static/screenshots/final_screenshots/{comment.replace(".mp3",".jpg")}')
        return render_template("upload.html")


    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', category='info')
        return redirect(url_for('home'))
    

    if __name__ == "__main__":
        app.run(debug=True)
