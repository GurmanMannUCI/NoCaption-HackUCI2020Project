import json
import random

#List of random works incase all the words chosen by user arent in the index
listofrandom = ['car','money','ballin','hoes','kobe','lambo','computer','iphone','life','crazy','complete',
                'eggnog','cook','liar','scratch','female','men','swim','shark','oatmeal','house',
                'half','cheap','big','skinny','sleet','new','trump'
                ]

#Searches main index using words specified by user. Reoccuring lyrics are given extra points as theyre more likely wanted by user.
#Top 20 lyrics, sorted from highest ranking to lowest, are output
#Picks random words incase all words by user arent in maindict
def Search(query):
    returneddict = {}
    for value in query:
        try:
            value = value.lower()
            valuemerge = wordindex[value]
            if valuemerge != "{}":
                for valuekey in valuemerge.keys():
                    if valuekey in returneddict.keys():
                        returneddict[valuekey] += valuemerge[valuekey]
                    else:
                        returneddict[valuekey] = valuemerge[valuekey]
        except:
            pass
    if returneddict == {}:
        listofwords = []
        for i in range(5):
            listofwords.append(random.choice(listofrandom))
        return Search(listofwords)
    sorteddict = sorted(returneddict.items(), key=lambda x: x[1],reverse = True)
    sorteddict = sorteddict[:20]
    return sorteddict

def CaptionGetter(sorteddict):
  #uses sorted captions to output a json file containing lyrics, songs, and artists
  #ensures that each caption from a song only appears once
    mainjson = {}
    songvalue = 1
    setofsongs = set()
    for value in sorteddict:
        try:
            value = value[0]
            splitvalue = value.split("/")
            artistname = splitvalue[0]
            songname = splitvalue[1]
            songstring = str(songname)+" - "+str(artistname)
            caption = maindict[artistname][songname][splitvalue[2]]
            if songstring not in setofsongs:
                mainjson["Song{}".format(songvalue)] = {
                    "Name"    :  songname,
                    "Artist"  :  artistname,
                    "Caption" :  caption
                }
                songvalue += 1
                setofsongs.add(songstring)
            if len(setofsongs) >=5:
                break
        except:
            pass
    return mainjson


def tester():
  #prints artist names. used in debugging
    for i in maindict.keys():
        print(i)


def Loader():
  #loads in masterfile containing all lyrics, and a wordindex which shows their location
    global maindict
    maindict = json.load(open("masterfile.txt"))
    global wordindex
    wordindex = json.load(open("WordIndex.txt"))


def Saver():
  #saves masterfile
    json.dump(maindict,open("masterfile.txt",'w'))

if __name__ == "__main__":
    Loader()
    prompt = ""
    while (True):
        prompt = input("Enter Search Query: ")
        if prompt == "quit":
            break
        query = prompt.split(" ")
        sorteddict = Search(query)
        jsonfile = CaptionGetter(sorteddict)
        print(jsonfile)


