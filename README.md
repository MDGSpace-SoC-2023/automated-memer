# Automated Memer 🎥

All done WITHOUT video editing or asset compiling. Just pure ✨programming magic✨.

In the ever-evolving landscape of content creation, Reddit videos have emerged as a dominant force across platforms like Instagram, YouTube, and TikTok, amassing millions of views. These videos typically follow a specific formula: a Minecraft background paired with a robot reading out an AskReddit thread.However, the manual process of stitching these elements together is time-consuming and inefficient. To address this challenge, I developed Automated Memer, an automated Reddit Video Bot, capable of seamlessly generating these videos with a single command.


## Video Explainer (Youtube)
[![thubmnail](https://github.com/MDGSpace-SoC-2023/automated-memer/assets/40473326/4fd7e9ba-f8ec-4ad8-9c8b-5f176d300f46)
](https://www.youtube.com/watch?v=yjbsk9O5998)


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
Flask is a web framework written in Python. It is lightweight and modular, making it an excellent choice for developing web applications. In RetroCraft Hub, Flask is the backbone of the server-side logic, handling HTTP requests, routing, and interacting with the database.

### AJAX and fetch API
AJAX (Asynchronous JavaScript and XML) is a technique used on the client-side to create dynamic and asynchronous web applications. RetroCraft Hub uses AJAX and fetch API to update content on web pages without requiring a full page reload. This results in a smoother user experience.I have used this extensively in my client-server comuunication.

### Google OAuth
OAuth (Open Authorization) is a secure, open-standard protocol that allows users to authorize third-party applications without sharing their credentials. RetroCraft Hub uses Google OAuth for user authentication. This allows users to log in using their Google accounts, enhancing security and simplifying the registration process.

### WebSockets
WebSockets provide full-duplex communication channels over a single, long-lived connection. In RetroCraft Hub, WebSockets enable real-time communication between users, supporting features like instant messaging and live notifications. This technology enhances the interactive and dynamic nature of the platform.

### Socket.IO
Socket.IO is a library that enables real-time, bidirectional, and event-based communication. It is built on top of WebSockets but provides additional features, such as fallback mechanisms for environments where WebSocket is not available. RetroCraft Hub utilizes Socket.IO to establish and manage WebSocket connections between clients and the server.

### SQLAlchemy
SQLAlchemy is an SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of high-level API for interacting with relational databases. In RetroCraft Hub, SQLAlchemy facilitates the interaction with the database, allowing for seamless integration of database operations within the Flask application.

### Bootstrap
Bootstrap is a front-end framework that simplifies the design and development of responsive and mobile-first web pages. RetroCraft Hub utilizes Bootstrap for its responsive design, ensuring a consistent and visually appealing user interface across different devices.Its 12 grid system made it easier to arrange divs into rows and columns based upon my liking.

## Conclusion

I am grateful to have had the opportunity to work on the RetroCraft Hub project for the past month. It has been an exciting journey, and I have learned a lot during the development process. From implementing various technologies to designing a responsive user interface, every step has been a valuable learning experience.

Throughout this project, I have honed my skills in web development and gained a deeper understanding of how different technologies work together to create a seamless user experience. I am proud of the final result and the effort I have put into making RetroCraft Hub.

I would like to express my gratitude to everyone who has supported me during this journey, including my mentors, colleagues, and friends. Their guidance and feedback have been invaluable in shaping the project and pushing me to deliver my best work.

As I conclude this project, I am excited to see how RetroCraft Hub will continue to evolve. I look forward to future opportunities to contribute to similar projects and further enhance my skills as a software developer.

Thank you for being a part of this journey with me.












