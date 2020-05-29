global maindict
import json
import re


def Loader():
    #Loads in the masterfile (containing all the songs and lyrics)
    try:
        global maindict
        maindict = json.load(open("masterfile.txt"))
    except:
        pass

def Parser():
    #Goes through each song lyric and "cleans" it by passing it to Cleaner function
    #Currently each song lyric is not indexed. They will get indexed and split in cleaner
    for i in maindict.keys():
        for j in maindict[i].keys():
            cleaned = Cleaner(maindict[i][j])
            maindict[i][j] = {}
            maindict[i][j] = cleaned
        break

def Cleaner(uncleaneddict):
    #Gets rid of unwanted punctuation in each song lyric and splits each lyric. 
    #set number as key, and lyric as value
    cleaneddict = {}
    num = 0
    splitted = uncleaneddict.split("\n")
    for i in (splitted):
        if (("[") in i) or (i == ""):
            pass
        else:
            i = i.replace("'","")
            i = i.strip()
            i = re.sub('[^A-Za-z0-9]+', ' ',i)
            cleaneddict[num] = i
            num += 1
    return(cleaneddict)


def Saver():
    #Saves all progress into masterfile
    json.dump(maindict, open("masterfile.txt", 'w'))


def Cleaner1():
    #function that isnt used anymore
    #Used only to get rid of lyrics too long or too short
    for artistname in maindict.keys():
        for songname in maindict[artistname].keys():
            returneddict = {}
            for index in maindict[artistname][songname].keys():
                if ((len(maindict[artistname][songname][index].split())> 3) and (len(maindict[artistname][songname][index].split()) < 20)):
                    returneddict[index] = maindict[artistname][songname][index]
            maindict[artistname][songname]=returneddict

def Deleter():
    #function that is used to delete all lyrics from certain artist or song. Only used for debugging
    for i in maindict["Drake"].keys():
        print(i)

if __name__ == "__main__":
    Loader()
    #Deleter()
    Saver()
