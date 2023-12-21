from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory,get_flashed_messages,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from gtts import gTTS
import praw
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset
import numpy as np
import os
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
from video_creator import execute_ffmpeg


app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager(app)
#login_manager.init_app(app)

bcrypt=Bcrypt(app)


reddit=praw.Reddit(client_id='mKBb_5vNtJixA9lMtTI4iw',
                   client_secret='iDOvkQdfQGe49_VZq0Ul6yyyAeTHhA',
                   username='Rishabh01289',
                   password='Myaccount@123',
                   user_agent='prawtutorialv1'
)


with app.app_context():
    app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    ##CREATE TABLE IN DB
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
    #Line below only required once, when creating DB. 
    #db.create_all()
    
    
    ''' @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password)
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password) '''
    
    

    # Define the user_loader function for the LoginManager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Set the login view for the LoginManager
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'danger'
    
    @app.context_processor
    def inject_year():
        year = datetime.now().year
        return {'year': year}

    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            new_user = User(
                email=request.form.get('email'),
                name=request.form.get('name'),
                password=request.form.get('password') 
            )
            
            # Check if the user already exists
            user = User.query.filter_by(email=new_user.email).first()
            if user:
                flash('You\'ve already signed up with that email, log in instead!', category='danger')
                return redirect(url_for('login'))
            
            ''' new_user.password = bcrypt.generate_password_hash(password).decode('utf-8') '''
            
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            
            # Redirect the user to the secrets page
            flash(f'Account created successfully! Welcome {new_user.name}', category='success')
            login_user(new_user)
            return redirect(url_for('welcome'))
        
        return render_template("register.html")
    


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                login_user(user)
                flash('Success! You are logged in.', category='success')
                return redirect(url_for('welcome'))
            else:
                flash('Invalid email or password',category='danger')
                return redirect(url_for('login'))
            
        return render_template("login.html")

        
        

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
        link = session.get('link')  # retrieve link from session
        voice= session.get('voice')
        submission = reddit.submission(url=link)
        title = submission.title
        session['title'] = title
        submission.comment_sort = 'top'
        submission.comments.replace_more(limit=0)
        all_comments = submission.comments.list()
        length=min(10, len(all_comments)-1)
        
        if voice=='female_1':
            tts = gTTS(text=title, lang='en-us')
            tts.save('static/Audio/title.mp3')
            for id, comment in enumerate(all_comments):
                index=id+1
                tts = gTTS(text=comment.body, lang='en-us')
                tts.save(f'static/Audio/comment{index}.mp3')
                if index == length:
                    break
        else:
            processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
            model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
            vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
            voice_dict = {
                'male_1': 5507,
                'male_2': 6109,
                'female_2': 7512
            }
            inputs = processor(text=title, return_tensors="pt")

            # load xvector containing speaker's voice characteristics from a dataset
            embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
            speaker_embeddings = torch.tensor(embeddings_dataset[voice_dict[voice]]["xvector"]).unsqueeze(0)
            speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
            sf.write('static/Audio/title.mp3', speech.numpy(), samplerate=16000)
            for id, comment in enumerate(all_comments):
                index=id+1
                
                inputs = processor(text=comment.body[:512], return_tensors="pt")
                speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
                sf.write(f'static/Audio/comment{index}.mp3', speech.numpy(), samplerate=16000)
                if index == length:
                    break
    
        
        def add_text_to_image(background_path, text, output_path, x,y,max_line_length,font_size = 50,text_color = (0, 0, 0)):
            
            # Open the white background image
            background = Image.open(background_path)

            # Create a drawing object
            draw = ImageDraw.Draw(background)

            # You can customize the font style and size
              # Increase the font size here
            font = ImageFont.truetype("arial.ttf", font_size)  # Specify the font and size

            # Set the text color (black in this case)
            

            # Set the position where you want to place the text
            text_position = (x,y)

            # Wrap the text to fit within the specified line length
            wrapped_text = textwrap.fill(text, width=max_line_length)

            # Add wrapped text to the image
            draw.text(text_position, wrapped_text, font=font, fill=text_color)

            # Save the new image with the added text
            background.save(output_path)

        
        #for title
        title=session.get('title')
        num_characters_title = len(title)
        
        #title 1
        if num_characters_title < 40:
            x=40
            y=200
            # Example usage
            background_image_path = "static/screenshots/mobile_ss_white_theme/title_1.jpg"
            text_to_add = title
            output_image_path = "static/screenshots/final_screenshots/title.jpg"
            add_text_to_image(background_image_path, text_to_add, output_image_path,x,y,38)
        
        
        #title 2    
        elif 40 <= num_characters_title and num_characters_title < 80:
            x=55
            y=155
            # Example usage
            background_image_path = "static/screenshots/mobile_ss_white_theme/title_2.jpg"
            text_to_add = title
            output_image_path = "static/screenshots/final_screenshots/title.jpg"
            add_text_to_image(background_image_path, text_to_add, output_image_path,x,y,38)
        
        #title 3    
        elif  80 <= num_characters_title < 120:
            x=55
            y=155
            # Example usage
            background_image_path = "static/screenshots/mobile_ss_white_theme/title_3.jpg"
            text_to_add = title
            output_image_path = "static/screenshots/final_screenshots/title.jpg"
            add_text_to_image(background_image_path, text_to_add, output_image_path,x,y,38)
         
        #title 4       
        elif 120 <= num_characters_title < 160:
            x=55
            y=190
            # Example usage
            background_image_path = "static/screenshots/mobile_ss_white_theme/title_4.jpg"
            text_to_add = title
            output_image_path = "static/screenshots/final_screenshots/title.jpg"
            add_text_to_image(background_image_path, text_to_add, output_image_path,x,y,38)
        
        
        #for comments
        comment_list=[]
        max_line_length=50
        for comment in os.listdir("static/Audio"):
            if comment=='title.mp3':
                continue
            comment_number =int((comment.replace("comment", "")).replace(".mp3", ""))
            comment_list.append(comment_number)
        comment_list.sort()   
        for c in comment_list:
            i=c-1
            text=all_comments[i].body
            num_characters = len(text)  # Get the number of characters in the text
            id=i+1
            
            
            if num_characters < 50:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_1.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")

            elif 50 <= num_characters < 100:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_2.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")

            elif 100 <= num_characters < 150:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_3.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
                
            elif 150 <= num_characters < 200:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_4.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
                
            elif 200 <= num_characters < 250:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_5.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
                
            elif 250 <= num_characters < 300:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_6.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")

            elif 300 <= num_characters < 350:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_7.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")

            elif 350 <= num_characters < 400:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_8.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
                
            elif 400 <= num_characters < 450:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_9.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")

            elif 450 <= num_characters < 500:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_10.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")

            elif 550 <= num_characters < 600:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_11.jpg"
                text_to_add = text
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
                
            elif 600 <= num_characters:
                x=45
                y=125
                background_image_path = "static/screenshots/mobile_ss_white_theme/comment_12.jpg"
                text_to_add = text[:620]
                output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
                add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
                
                
                
        flash('Content Generated Successfully', category='success')    
        return redirect(url_for('Audio'))
    
    
    
    @app.route("/Audio",methods=["POST","GET"])
    @login_required
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
        
        
        
    @app.route("/final_video",)
    @login_required
    def final_video():
        T = os.path.exists("static/Final_Videos/Final_Video_2.mp4")
        return render_template("final_video.html",T=T)



    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', category='info')
        return redirect(url_for('home'))
    

    if __name__ == "__main__":
        users = User.query.all()
        #for user in users:
            #print(user.name)
        app.run(debug=True)
