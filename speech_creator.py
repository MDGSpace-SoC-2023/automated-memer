from flask import Flask, request, session
import praw
from gtts import gTTS
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env')

      
reddit=praw.Reddit(client_id=os.getenv('CLIENT_ID_REDDIT'),
                   client_secret=os.getenv('CLIENT_SECRET_REDDIT'),
                   username=os.getenv('USERNAME_REDDIT'),
                   password=os.getenv('PASSWORD_REDDIT'),
                   user_agent='prawtutorialv1'
)


def execute_speech():
    link = session.get('link')  # retrieve link from session
    voice= session.get('voice')
    submission = reddit.submission(url=link)
    title = submission.title
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
        background = Image.open(background_path)
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("arial.ttf", font_size)  
        text_position = (x,y)
        wrapped_text = textwrap.fill(text, width=max_line_length)
        draw.text(text_position, wrapped_text, font=font, fill=text_color)
        background.save(output_path)

            
    #for title
    num_characters_title = len(title)

    no_of_lines_title = min(4,(num_characters_title//40)+1)
    
    if no_of_lines_title==1:
        x=40
        y=200
    elif no_of_lines_title==2:
        x=55
        y=155
    elif no_of_lines_title==3:
        x=55
        y=155
    else:
        x=55
        y=190

    if not os.path.exists('static/screenshots/final_screenshots'):
        os.makedirs('static/screenshots/final_screenshots')
    background_image_path = f'static/screenshots/mobile_ss_white_theme/title_{no_of_lines_title}.jpg'
    text_to_add = title
    output_image_path = "static/screenshots/final_screenshots/title.jpg"
    add_text_to_image(background_image_path, text_to_add, output_image_path,x,y,38)



    #for comments
    max_line_length=50 
    for i in range(10):
        text=all_comments[i].body
        num_characters = len(text)  # Get the number of characters in the text
        id=i+1

        no_of_lines = min(12,(num_characters//50)+1)

        x=45
        y=125
        background_image_path = f'static/screenshots/mobile_ss_white_theme/comment_{no_of_lines}.jpg'
        text_to_add = text
        output_image_path = f'static/screenshots/final_screenshots/comment{id}.jpg'
        add_text_to_image(background_image_path, text_to_add, output_image_path, x, y, max_line_length, font_size=40, text_color="#454545")
