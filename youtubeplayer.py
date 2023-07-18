import vlc
from pytube import YouTube, Search
import threading

# Global variable to control the loop in play_audio
dostop = False

def get_video_url(song_name):
    search_results = Search(song_name).results
    if search_results:
        video_url = search_results[0].watch_url
        return video_url

    return None

# Function to get the audio stream URL of a YouTube video
def get_audio_stream_url(video_url):
    youtube = YouTube(video_url)
    audio_stream = youtube.streams.filter(only_audio=True).first()
    return audio_stream.url

# Function to play the audio stream
def play_audio(stream_url):
    media_player = vlc.MediaPlayer(stream_url)
    media_player.play()
    while not dostop:
        pass  # Keep the player running until you want to stop

# Function to listen for user input
def input_listener():
    global dostop
    while True:
        user_input = input()
        if user_input.lower() == "stop":
            dostop = True
            break

# Create a thread for playing audio
def play_audio_thread(stream_url):
    play_thread = threading.Thread(target=play_audio, args=(stream_url,))
    play_thread.start()
    return play_thread

# Create a thread for listening to user input
def input_listener_thread():
    input_thread = threading.Thread(target=input_listener)
    input_thread.start()

# Example usage
if __name__ == "__main__":
    song_name = input("Enter the song name: ")
    video_url = get_video_url(song_name)
    if video_url:
        audio_stream_url = get_audio_stream_url(video_url)
        thread = play_audio_thread(audio_stream_url)
        input_listener_thread()
    else:
        print("No video found for the given song name.")

    if "l" in input("enter l to stop"):
        dostop = True
        thread.
        print("Stopped the song")