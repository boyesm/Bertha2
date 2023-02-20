from pytube import YouTube


def is_valid_youtube_video(user_input):
    # print(user_input)

    try:
        # TEST CASE: https://www.youtube.com/watch?v=KRbsco8M7Fc
        yt = YouTube(user_input)

    except Exception as e:
        print(f"CHAT: link is invalid {e}")
        return False

    try:
        # this will return None if it's available, and an error if it's not
        yt.check_availability()

    except Exception as e:
        print(f"CHAT: {e}")
        return False

    if yt.age_restricted:
        print(f"CHAT: {user_input} is age restricted")
        return False

    # TODO: decide on an appropriate maximum video length
    if yt.length >= 390:
        print(f"CHAT: {user_input} is too long")
        return False

    return True
