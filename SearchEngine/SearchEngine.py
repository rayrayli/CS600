from bs4 import BeautifulSoup  
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from InvertedIndex import InvertedIndex
from Tries import Tries

MINIMUM_CHR = 2
MAP_PATH = "MySpider/file_link_map.json"
class SearchEngine(object):
    inverted_index = InvertedIndex()

    def buildTries(self):
        f = open(MAP_PATH, "rb")
        file_link_map = json.loads(f.readlines()[0]) 

        # filter stopword and punctuation
        stop_words = set(stopwords.words('english'))
        stop_words.update(string.punctuation)

        for filename in file_link_map:
            filefullname = './MySpider/%s' % filename
            f = open(filefullname,"rb")
            soup = BeautifulSoup(f.read(), 'html.parser')
            [script.extract() for script in soup.findAll('script')]
            [style.extract() for style in soup.findAll('style')]
            print (file_link_map[filename])
            words = word_tokenize(soup.get_text())
            # remove the words containing punctuation
            words = [i for i in words if all(j not in string.punctuation for j in i)]
            
            for word in words:
                if word.lower() not in stop_words and len(word) > MINIMUM_CHR and word.isdigit()==False:
                        # build compressed trie tree
                        try:
                            # remove the words whcih can't encode to ascII
                            word = word.lower().strip().encode('ascII')
                        except:
                            a = 1
                        else:
                            self.inverted_index.put(word.decode('utf-8'), file_link_map[filename])
        f.close()
        
    def search(self, key):
        if self.inverted_index.get(key) == None:
            return {}
        else:
            return self.inverted_index.get(key)
    
    def getRecomendKey(self, string):
        return self.inverted_index.getRecommendKey(string) 
