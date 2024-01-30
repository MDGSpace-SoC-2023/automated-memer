# Automated Memer 🎥

All done WITHOUT video editing or asset compiling. Just pure ✨programming magic✨.

In the ever-evolving landscape of content creation, Reddit videos have emerged as a dominant force across platforms like Instagram, YouTube, and TikTok, amassing millions of views. These videos typically follow a specific formula: a Minecraft background paired with a robot reading out an AskReddit thread.However, the manual process of stitching these elements together is time-consuming and inefficient. To address this challenge, I developed Automated Memer, an automated Reddit Video Bot, capable of seamlessly generating these videos with a single command.

Check it out for yourself: http://rishabhjain123.pythonanywhere.com/


## Video Explainer (Youtube)
[![thubmnail](https://github.com/MDGSpace-SoC-2023/automated-memer/assets/40473326/4fd7e9ba-f8ec-4ad8-9c8b-5f176d300f46)
](https://www.youtube.com/watch?v=evKCuA0kOL0&t=50s&ab_channel=RishabhJain)


## Installation

Follow these steps to set up RetroCraft Hub on your local machine:

### Step 1: Clone the Repository

```bash
git clone https://github.com/rishabhJain1234/RetroCraft_Hub.git](https://github.com/MDGSpace-SoC-2023/automated-memer.git
cd automated-memer
```

### Step 2: Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create a .env file
```bash
touch .env
echo "SECRET_KEY=your_secret_key" >> .env
echo "CLIENT_ID=your_client_id" >> .env
echo "CLIENT_SECRET=your_client_secret" >> .env
echo "CLIENT_ID_REDDIT=your_reddit_client_id" >> .env
echo "CLIENT_SECRET_REDDIT=your_reddit_client_secret" >> .env
echo "USERNAME_REDDIT=your_reddit_username" >> .env
echo "PASSWORD_REDDIT=your_reddit_password" >> .env


```

### Environment Variables
Make sure to replace the placeholder values in the .env file with your actual credentials.

1. SECRET_KEY is the Flask server's secret key. You can set it up to be any value.

2. CLIENT_ID and CLIENT_SECRET are credentials for the Google's OAuth. For more information on how to get your own credentials, follow this link: [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2).

3. CLIENT_ID_REDDIT and CLIENT_SECRET_REDDIT are credentials for your reddit app.Follow this detailed tutorial to get them: [Reddit app documentation](https://docs.google.com/document/d/1wHvqQwCYdJrQg4BKlGIVDLksPN0KpOnJWniT6PbZSrI/edit).

4. USERNAME_REDDIT and PASSWORD_REDDIT are the username and password of your reddit account respectively which you used to make your reddit app in the above step.

### Step 5: Run the Application
```bash
python main.py
```

Visit http://localhost:5000 in your web browser to access Automated Memer.

Now you are all set to run Automated Memer!
If you get stuck at any step of Installation ,feel free to contact me at my email: rishabhjain.1632004@gmail.com

## Video

https://github.com/MDGSpace-SoC-2023/automated-memer/assets/40473326/18e1aefe-7a74-4c62-9a91-109fec075199


## Techstack 

### Flask
Flask is a web framework written in Python. It is lightweight and modular, making it an excellent choice for developing web applications. In Automated Memer, Flask is the backbone of the server-side logic, handling HTTP requests, routing, and interacting with the database.

### AJAX and fetch API
AJAX (Asynchronous JavaScript and XML) is a technique used on the client-side to create dynamic and asynchronous web applications. RetroCraft Hub uses AJAX and fetch API to update content on web pages without requiring a full page reload. This results in a smoother user experience.I have used this extensively in my client-server comuunication.

### Google OAuth
OAuth (Open Authorization) is a secure, open-standard protocol that allows users to authorize third-party applications without sharing their credentials. RetroCraft Hub uses Google OAuth for user authentication. This allows users to log in using their Google accounts, enhancing security and simplifying the registration process.

### PRAW (Python Reddit API Wrapper):
PRAW is a Python package that allows for simple access to Reddit's API. PRAW aims to be easy to use and internally follows all of Reddit's API rules. With PRAW there's no need to introduce sleep calls in your code. Give your client an appropriate user agent and you're set.I used PRAW to get the title and comments of the reddit post from the user's link.

### GTTS (Google Text to Speech):
GTTS is a Python library and CLI tool to interface with Google Translate's text-to-speech API.I used this as one of the ways to convert my comments and title from text to speech.

### microsoft/speecht5_tts huggingface ML model:
I used microsoft's sppecht5 tts model from huggingface as one of the ways to convert my comments and title from text to speech.It provides more natural and realistic results than gtts.

### Pillow (fork of PIL):
Pillow/PIL is an image processing library in python.I used this library to create screenshots from the comments by overlaying the text over pre-made templates.

### Pydub:
Pydub is an audio processing library.It helped me to combine all the speeches from the text to speech model into a single combined file and also add silent durations between them.

### FFmpeg:
FFmpeg is a very powerful ui-less video editor which runs on the terminal.It can process multimedia content such as audio, video, subtitles and related metadata.It is core component of Automated Memer and I utilised it to stich together and overlay the screenshots and the audio files over video of minecraft background.

## Conclusion

I am grateful to have had the opportunity to work on Automated Memer. It has been an exciting journey, and I have learned a lot during the development process. From implementing various technologies to designing a responsive user interface, every step has been a valuable learning experience.

Throughout this project, I have honed my skills in web development and gained a deeper understanding of how different technologies work together to create a seamless user experience. I am proud of the final result and the effort I have put into making Automated Memer.

I would like to express my gratitude to everyone who has supported me during this journey, including @MDGSpace my mentor, colleagues, and friends. Their guidance and feedback have been invaluable in shaping the project and pushing me to deliver my best work.

As I conclude this project, I am excited to see how Automated Memer will continue to evolve. I look forward to future opportunities to contribute to similar projects and further enhance my skills as a software developer.

Thank you for being a part of this journey with me.








