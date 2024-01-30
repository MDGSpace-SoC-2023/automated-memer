import os
import random  
import gdown
import soundfile as sf
from pydub import AudioSegment
import subprocess
import ffmpeg
from flask import Flask, request, session

def execute_ffmpeg():
    comment_no=[]
    comments_to_stich=[]
    total_length=0
    Start=[]
    End=[]
    user_email = session.get('user_email')
    Audio_dir=f"static/UserData/{user_email}/Audio"
    for comment in os.listdir(Audio_dir):
        print(comment)
        if comment=='title.mp3':
            data, samplerate = sf.read(Audio_dir + '/' + comment)
            title_length = round(len(data) / samplerate, 2)+1
            total_length+=title_length
        if comment=='combined_audio.mp3' or comment=='combined.mp3':
            os.remove(Audio_dir +'/' + comment)  
    t=0
    i=1
    gts=len(os.listdir(Audio_dir))-1   #total no of comments excluding title.mp3


    for comment in os.listdir(Audio_dir):
        if comment!='title.mp3'and comment!='combined.mp3'and comment!='combined_audio.mp3':
            data, samplerate = sf.read(Audio_dir + '/' + comment)
            comment_length = round(len(data) / samplerate, 2)+1
            total_length+=comment_length
            t+=1
            print(total_length)
                
                
            if total_length <= 60 or t==gts:
                comments_to_stich.append(comment)
                comment_number =int((comment.replace("comment", "")).replace(".mp3", ""))
                comment_no.append(comment_number)
                
        
            if total_length >= 60 or t==gts:
                
                if t!=gts:
                    total_length-=comment_length
                    
                Start.append(0)
                End.append(title_length)
                
                #write code for video generation using moviepy
                url1 ='https://drive.google.com/u/0/uc?id=1I5Sl-SukvYozqRtdDjteyiFpgvarVKHh&export=download&confirm=t'
                url2 ='https://drive.google.com/u/0/uc?id=1VvbxYTk9OZ8FztebojDfXC6f5_O5FGZ9&export=download&confirm=t'
                url3 ='https://drive.google.com/u/0/uc?id=16aTUJHUdd1ryJAROwk-D-J0yUsvfuhKJ&export=download&confirm=t'
                url4 ='https://drive.google.com/u/0/uc?id=12UbsZE7I4cdlkKup52KKTgRsWOIB37rv&export=download&confirm=t'
                url5 ='https://drive.google.com/u/0/uc?id=1BT_tYSRoHVdphK36l44DJ2pnUGzW4f_S&export=download&confirm=t'
                url6 ='https://drive.google.com/u/0/uc?id=1hnvcx9v4O1STKu9wjxu8Og8VgwseYgw-&export=download&confirm=t'
                url7 ='https://drive.google.com/u/0/uc?id=1lc0NYLewPs-3vmKc5zOKJtcwYCf-byxv&export=download&confirm=t'
                url8 ='https://drive.google.com/u/0/uc?id=1kS0uXqZkHGz6MMwcMn_dmYmY_BKZUBht&export=download&confirm=t'
                url9 ='https://drive.google.com/u/0/uc?id=1XdcpXjqQW0DU3-6Ocl_GXod2pPfsD_Ql&export=download&confirm=t'
                url10='https://drive.google.com/u/0/uc?id=1neSbDRswriDYiE5dieJMvIXOeraQ5RKI&export=download&confirm=t'

                url_list = [url1, url2, url3, url5, url6, url7, url8, url10,url1, url2, url3, url5, url6, url7, url8, url10,url4]
                first=random.choice(url_list)
                second=random.choice(url_list)
                third=random.choice(url_list)
                url = random.choice([first,second,third])
                no=url.replace("https://drive.google.com/u/0/uc?id=","")
                no=no.replace("&export=download&confirm=t","")
                output_file = f'static/Background_videos/video{no}.mp4'
                
                if not os.path.exists("static/Background_videos"):
                    os.makedirs("static/Background_videos")
                    
                if not os.path.exists(f"static/Background_videos/video{no}.mp4"):
                    print("Downloading video.mp4")
                    gdown.download(url, output_file, fuzzy=True, use_cookies=True)
                
                # Load the title audio file
                title = AudioSegment.from_file(Audio_dir +"/title.mp3")

                # Initialize the combined audio with the title
                combined_audio = title + AudioSegment.silent(duration=1000)

                # Iterate over the comments in comments_to_stich
                for comment in comments_to_stich:
                    comment_audio = AudioSegment.from_file(Audio_dir + "/" + comment)
                    combined_audio += comment_audio + AudioSegment.silent(duration=1000)

                # Export the combined audio as an mp3 file
                combined_audio.export(Audio_dir + "/combined.mp3", format="mp3", bitrate="320k")
                
                
                original_audio=AudioSegment.from_file("static/Bgm/Lofi_1.mp3")
                original_audio = original_audio[:total_length * 1000]

                # Load the new audio file
                new_audio = AudioSegment.from_file(Audio_dir + "/combined.mp3")

                # Combine the original audio with the new audio
                combined_audio = new_audio.overlay(original_audio)
                combined_audio.export(Audio_dir + "/combined_audio.mp3", format="mp3", bitrate="320k")
                
                
                iter=0
                start=0
                for comm in comments_to_stich:
                    
                    iter+=1
                    if iter==1:
                        start=title_length
                    else: 
                        start+=comm_length
                    
                    Start.append(start)
                    data, samplerate = sf.read(Audio_dir+ "/"+  comm)
                    comm_length = round(len(data) / samplerate, 2)+1
                    End.append(start+comm_length)
                    
    
                background_video = f'static/Background_videos/video{no}.mp4'
                screenshots = []
                screenshots.append(f'static/UserData/{user_email}/screenshots/title.jpg')
                no_of_ss=len(comments_to_stich)
                for ss in comments_to_stich:
                    s=ss.replace(".mp3",".jpg")
                    screenshots.append(f'static/UserData/{user_email}/screenshots/{s}') 
                    
                # Input audio path
                audio_file = Audio_dir + "/combined_audio.mp3"
                os.makedirs(f"static/UserData/{user_email}/Final_Video", exist_ok=True)
                output_video = f"static/UserData/{user_email}/Final_Video/output_video_without_audio.mp4"
                
                if no_of_ss==1:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==2:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==3: 
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'',
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==4:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==5:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', screenshots[5],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'[bg5];'
                    f'[bg5][6:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[5]},{End[5]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==6:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', screenshots[5],
                    '-i', screenshots[6],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'[bg5];'
                    f'[bg5][6:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[5]},{End[5]})\'[bg6];'
                    f'[bg6][7:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[6]},{End[6]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==7:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', screenshots[5],
                    '-i', screenshots[6],
                    '-i', screenshots[7],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'[bg5];'
                    f'[bg5][6:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[5]},{End[5]})\'[bg6];'
                    f'[bg6][7:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[6]},{End[6]})\'[bg7];'
                    f'[bg7][8:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[7]},{End[7]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==8:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', screenshots[5],
                    '-i', screenshots[6],
                    '-i', screenshots[7],
                    '-i', screenshots[8],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'[bg5];'
                    f'[bg5][6:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[5]},{End[5]})\'[bg6];'
                    f'[bg6][7:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[6]},{End[6]})\'[bg7];'
                    f'[bg7][8:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[7]},{End[7]})\'[bg8];'
                    f'[bg8][9:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[8]},{End[8]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss==9:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', screenshots[5],
                    '-i', screenshots[6],
                    '-i', screenshots[7],
                    '-i', screenshots[8],
                    '-i', screenshots[9],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'[bg5];'
                    f'[bg5][6:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[5]},{End[5]})\'[bg6];'
                    f'[bg6][7:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[6]},{End[6]})\'[bg7];'
                    f'[bg7][8:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[7]},{End[7]})\'[bg8];'
                    f'[bg8][9:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[8]},{End[8]})\'[bg9];'
                    f'[bg9][10:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[9]},{End[9]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                elif no_of_ss>=10:
                    ffmpeg_command = [
                    'ffmpeg',
                    '-y',
                    '-i', background_video,
                    '-i', screenshots[0],
                    '-i', screenshots[1],
                    '-i', screenshots[2],
                    '-i', screenshots[3],
                    '-i', screenshots[4],
                    '-i', screenshots[5],
                    '-i', screenshots[6],
                    '-i', screenshots[7],
                    '-i', screenshots[8],
                    '-i', screenshots[9],
                    '-i', screenshots[10],
                    '-i', audio_file,  # Add the audio file
                    '-filter_complex',
                    f'[0:v][1:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,0,{End[0]})\'[bg];'
                    f'[bg][2:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[1]},{End[1]})\'[bg2];'
                    f'[bg2][3:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[2]},{End[2]})\'[bg3];'
                    f'[bg3][4:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[3]},{End[3]})\'[bg4];'
                    f'[bg4][5:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[4]},{End[4]})\'[bg5];'
                    f'[bg5][6:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[5]},{End[5]})\'[bg6];'
                    f'[bg6][7:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[6]},{End[6]})\'[bg7];'
                    f'[bg7][8:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[7]},{End[7]})\'[bg8];'
                    f'[bg8][9:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[8]},{End[8]})\'[bg9];'
                    f'[bg9][10:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[9]},{End[9]})\'[bg10];'
                    f'[bg10][11:v] overlay=(W-w)/2:(H-h)/2:enable=\'between(t,{Start[10]},{End[10]})\'',  # Add the audio stream
                    '-c:a', 'aac',
                    output_video
                    ]
                        
                    
                        

                # Run the ffmpeg command
                subprocess.run(ffmpeg_command)


                input_video = ffmpeg.input(output_video)
                trimmed_video = input_video.trim(start=0, end=End[no_of_ss])
                
                added_audio = ffmpeg.input(Audio_dir + "/combined_audio.mp3").audio
                ffmpeg.concat(trimmed_video, added_audio, v=1, a=1).output(f'static/UserData/{user_email}/Final_Video/Final_Video.mp4').run(overwrite_output=True)                    
                
                    
                    
                total_length=title_length+1
                comment_no=[]
                comments_to_stich=[]
                comments_to_stich.append(comment)
                comment_number =int((comment.replace("comment", "")).replace(".mp3", ""))
                comment_no.append(comment_number)
                Start=[]
                End=[]
                    
                break;
    
            
