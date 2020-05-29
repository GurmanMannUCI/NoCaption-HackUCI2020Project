import json
import os
import random

listofrandom = ['car','money','ballin','hoes','kobe','lambo','computer','iphone','life','crazy','complete',
                'eggnog','cook','liar','scratch','female','men','swim','shark','oatmeal','house',
                'half','cheap','big','skinny','sleet','new','trump'
                ]

testcaptions = [{'song': 'DoIHaveTheSause?', 'artist': 'Ski Mask the Slump God', 'lyric': 'Air Force 1 with the flow no crease'},
 {'song': 'Whats Really Good', 'artist': 'The Diplomats', 'lyric': 'Air Force Ones looking like Lucky Charms'},
 {'song': 'Nikes', 'artist': 'Frank Ocean', 'lyric': 'These bitches want Nikes'},
 {'song': 'Earned It', 'artist': 'Chief Keef', 'lyric': 'I dont need a jet I want Air Force One'},
 {'song': 'Air Force Ones', 'artist': 'Nelly', 'lyric': 'Big boys stompin in my Air Force Ones'}]

class LyricMatcher():
    def __init__(self,query):
        self.query = query

    def findMatches(self):
        self.Loader()
        sorted_dict = self.Search(["difference", "money", "like", "kim", "kardashian"])
        captions = self.CaptionGetter(sorted_dict)
        return testcaptions

    def Loader(self):
        self.maindict = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/masterfile.txt"))
        self.wordindex = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/WordIndex.txt"))

    def Search(self,query):
        returneddict = {}
        for value in query:
            try:
                value = value.lower()
                valuemerge = self.wordindex[value]
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
            return self.Search(listofwords)
        sorteddict = sorted(returneddict.items(), key=lambda x: x[1], reverse=True)
        sorteddict = sorteddict[:20]
        return sorteddict

    def CaptionGetter(self,sorteddict):
        mainjson = []
        songvalue = 1
        setofsongs = set()
        for value in sorteddict:
            try:
                value = value[0]
                splitvalue = value.split("/")
                artistname = splitvalue[0]
                songname = splitvalue[1]
                songstring = str(songname) + " - " + str(artistname)
                caption = self.maindict[artistname][songname][splitvalue[2]]
                if songstring not in setofsongs:
                    mainjson.append({
                        "song": songname,
                        "artist": artistname,
                        "lyric": caption
                    })
                    songvalue += 1
                    setofsongs.add(songstring)
                if len(setofsongs) >= 5:
                    break
            except:
                pass
        return mainjson


#if __name__ == '__main__':
    #lm=LyricMatcher(["difference", "money", "like", "kim", "kardashian"])
    #print(lm.findMatches())