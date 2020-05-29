import io
import os
import base64
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
import time
import enchant
import re

stopwords = {"a","about","above","after","again","against","all","am","an","and",
            "any","are","arent","as","at","be","because","been","before","being",
             "below","between","both","but","by","cant","cannot","could","couldnt",
             "did","didnt","do","does","doesnt","doing","dont","down","during",
            "each","few","for","from","further","had","hadnt","has","hasnt","have",
            "havent","having","he","hed","hell","hes","her","here","heres","hers",
            "herself","him","himself","his","how","hows","i","id","ill","im","ive",
            "if","in","into","is","isnt","it","its","its","itself", "know", "like", "lets","me","more",
            "most","mustnt","my","myself","no","nor","not","of","on","once","only",
            "or","other","ought","our","ours", "ourselves","out","over","own","same",
            "shant","she","shed","shell","shes","should","shouldnt","so","some","such",
            "than","that","thats","the","their","theirs","them","themselves","then","there",
            "theres","these","they","theyd","theyll","theyre","theyve","this","those","through",
            "to","too","under","until","very","was","wasnt","we","wed","well","were",
            "weve","were","werent","what","whats","when","whens","where","wheres","which",
            "while","who","whos","whom","why","whys","with","wont","would","wouldnt","you",
            "youd","youll","youre","youve","your","yours","yourself","yourselves"}

class Vision():
    # image must be a Base64 string that converts to an image
    def __init__(self,image):
        self.d = enchant.Dict("en_US") #Valid Word
        self.image = image
        self.GOOGLE_VISION_API_CREDS = service_account.Credentials.from_service_account_file(os.path.dirname(os.path.abspath(__file__)) + '/NoCapTion-6bae2ab0bd5c.json')

    def classifyImage(self):
        #decoded_image = self.decodeBase64Image()
        #if( decoded_image == None ):
        #    return 'Unable to Decode Provided Image!'

        #annotations = self.getAnnotations(decoded_image)
        #if( annotations == None ):
        #    return 'Unable to Get Annotations From Provided Image!'

        #top_keywords = self.findTopAnnotations(annotations)
        #print(top_keywords)
        top_keywords = ['Nike',"Air","Force","Shoe","Cartoon","One","Black","White"]
        return top_keywords


    def decodeBase64Image(self):
        image = None
        try:
            decoded_image = base64.b64decode(self.image)
            image = types.Image(content=decoded_image)
        except:
            print('Unable to Decode Provided Image!')
        finally:
            return image

    def getAnnotations(self, image_file):
        img_annotes = None
        try:
            client = vision.ImageAnnotatorClient(credentials=self.GOOGLE_VISION_API_CREDS)
            response = client.annotate_image({
                        'image': image_file
                    })
            img_annotes = response
        except:
            print('Unable to get image annotations!')
        finally:
            return img_annotes

    def getValidWord(self, word):
        if(len(word) > 0):
            #print(word, self.d.check(word))
            if( self.d.check(word) ):
                return word
            #else:
                #suggested_words = self.d.suggest(word)
                #if( len(suggested_words) > 0 and (len(suggested_words[0])-len(word)) < 3):
                    #return suggested_words[0]
                #else:
                    #return word
        return ''


    def findTopAnnotations(self, annotations):
        # Do an OCR check at this point
        ocr_text_results = []
        if(annotations.full_text_annotation):
           ocr_text_results= annotations.full_text_annotation.text.strip().split('\n')
           refined_ocr = []
           for word in ocr_text_results:
              #print(word)
              if len(word.split()) > 1:
                 for i in word.split():
                    valid_word = self.getValidWord(re.sub(r'[^\w]', '', i)).lower()
                    if(valid_word != '' and valid_word not in refined_ocr and len(valid_word) > 2 and valid_word not in stopwords):
                        refined_ocr.append(valid_word)
              else:
                 valid_word = self.getValidWord(re.sub(r'[^\w]', '', word)).lower()
                 if(valid_word != '' and valid_word not in refined_ocr  and len(valid_word) > 2 and valid_word not in stopwords):
                    refined_ocr.append(valid_word)
           #print(refined_ocr)
           ocr_text_results=refined_ocr

        #print(annotations)
        web_results = annotations.web_detection
        top_web_words = {}
        for entity in web_results.web_entities:
            for descr in entity.description.split():
                refined=re.sub(r'[^\w]', ' ', descr).strip().lower().split()
                for r in refined:
                    if(len(r) > 2 and r not in stopwords):
                        if(r in top_web_words.keys()):
                            top_web_words[r]+=1
                        else:
                            top_web_words[r] = 1
        top_web_words = {k: v for k, v in sorted(top_web_words.items(), key=lambda item: item[1], reverse=True)}
        top_web_words = list(top_web_words.keys())
        #print(top_web_words)
        if(len(ocr_text_results) < 5 and len(top_web_words) >= 10): #Too many OCR results can mess things up
            return (ocr_text_results[:3]+(top_web_words[:7])) # return top
        elif(len(top_web_words) >= 15):
            return top_web_words[:7]

        # Web result algo was shitty for this image so try something else...
        # If we got to this point then the image is probably a non-famous person
        if(len(annotations.face_annotations) > 0): # So is it a human?
            # How is that person feeling?
            possible_moods = []
            if(annotations.face_annotations[0].joy_likelihood > 1):
                possible_moods.append('happy')
            if(annotations.face_annotations[0].sorrow_likelihood > 1):
                possible_moods.append('sad')
            if(annotations.face_annotations[0].anger_likelihood > 1):
                possible_moods.append('mad')
            if(annotations.face_annotations[0].surprise_likelihood > 1):
                possible_moods.append('surprised')

            top_label_annotations = {}
            for entity in annotations.label_annotations:
                for descr in entity.description.split():
                    if (descr.lower() in top_label_annotations.keys()):
                        top_label_annotations[descr.lower()] += 1
                    else:
                        top_label_annotations[descr.lower()] = 1
            top_label_annotations = {k: v for k, v in sorted(top_label_annotations.items(), key=lambda item: item[1], reverse=True)}
            top_label_annotations = list(top_label_annotations.keys())
            if(len(list(set(possible_moods + top_label_annotations))) >= 5):
                return list(dict.fromkeys((possible_moods + ocr_text_results[:3] + top_label_annotations)))[:10]
            elif(len(list(set(possible_moods + top_label_annotations + top_web_words))) >= 5):
                return list(dict.fromkeys((possible_moods + ocr_text_results[:3] + top_label_annotations + top_web_words)))[:10]
            elif(len(list(set(possible_moods + top_label_annotations + top_web_words))) >= 1):
                return list(dict.fromkeys((possible_moods + ocr_text_results[:3] + top_label_annotations + top_web_words)))
        else:
            #print('this is an object')
            top_label_annotations = {}
            for entity in annotations.label_annotations:
                for descr in entity.description.split():
                    if (descr.lower() in top_label_annotations.keys()):
                        top_label_annotations[descr.lower()] += 1
                    else:
                        top_label_annotations[descr.lower()] = 1
            top_label_annotations = {k: v for k, v in sorted(top_label_annotations.items(), key=lambda item: item[1], reverse=True)}
            top_label_annotations = list(top_label_annotations.keys())
            return self.removeDuplicates((top_web_words[:5]+ocr_text_results[:3]+top_label_annotations))[:10]
        return ['photo', 'picture', 'photograph', 'camera', 'art']

    def removeDuplicates(self,seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

# For testing remove before deployed
#if __name__ == '__main__':
    #test = ''
    #v = Vision(test)
    #v.classifyImage()
