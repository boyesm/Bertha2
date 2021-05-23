from pytube import YouTube

from dbEngine import dbEngine

if (__name__ == "__main__"):

    user_input = input("Link: ")

    yt = YouTube(user_input)  # YouTube("https://www.youtube.com/watch?v=KRbsco8M7Fc")
    print(yt.check_availability())
