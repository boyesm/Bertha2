

#Code by Jarvis Coghlin

def getVideoName(link):

    """
    :param link: This is the link to the youtube video including https://

    """

    if type(link) == "String":

        return ("Title" + link.strip(".,//\\\n"))

    else:

        return False


#Finds the number of views a video has froma link
def getNumViews(link):

    #FIXME Write function to find the number of views

    return "123,456"

