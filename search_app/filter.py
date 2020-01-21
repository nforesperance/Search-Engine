from .keywords_parser import *


class AntologyProcessor():

    minimal_val_for_spaces = 2 # n = valeur minimale du l'espace a considere lors du calcul du moyenne de l'espace
    min_block_size = 10 # plus petite taille d'un block
    @staticmethod
    def getSections(str,num_space, size = min_block_size):
        arr = []
        length = len(str)
        i=0
        last = 0
        while i<length:
            j= i
            while j<length:
                if(str[j] == " "):
                    nxt = AntologyProcessor.getNext(j,str)
                    if nxt>num_space:
                        start = i
                        end = j
                        if (end-start)+1>size:
                            # adding to array
                            arr.append(str[start:end])
                        i = j + nxt
                        last = i
                        j = i
                    
                j = j+1
            i = i+1
        if (length-last)>size and last!=0:
            #adding to array
            arr.append(str[last:length])
        return arr

    @staticmethod
    def getNext(j,str):
        x = 0
        while  j<len(str) and (str[j] == " "):
            x = x + 1
            j = j + 1
        return x
    
    @staticmethod
    def getAverage(str,n= minimal_val_for_spaces):
        length = len(str)
        i=0
        x = 0
        nxts = 0
        j= 0
        while j<length:
            if(str[j] == " "):
                nxt = AntologyProcessor.getNext(j,str)
                if(nxt>n):
                    nxts = nxts + nxt
                    x = x + 1
                i = j + nxt
                j = i   
            j = j+1
        if x!=0:
            avg = (nxts/x)-1
        if x==0:
            avg = 0
        return avg


    @staticmethod
    def getElement(search,elts):
        arr = []
        for elt in elts:
            if search in elt:
                arr.append(elt)
        if len(arr)>0:
            max = len(arr[0])
            elt = arr[0]
            for s in arr:
                if len(s)>max:
                    max = len(s)
                    elt = s
            return elt
        else:
            return ""
        

class ScrapingProcessorUnit():

    def __init__(self , imediatly_fectch = True , item = None , url = ''):
        self.url = url
        if item:
            self.url = item['link']
        self.item = item
        self.imediatly_fectch = imediatly_fectch
        self.full_text = ""
        self.stripped_text = ""
        self.sections = []
        self.tokens = []
        self.has_fetched = False
        if imediatly_fectch :
            self.fetch()

    def fetch(self):
        if not self.has_fetched:
            try:
                self.full_text = extract_text_from_url(self.url , remove_blank=False)
                self.stripped_text = remove_spaces(self.full_text)
                self.getSections()
                self.has_fetched = True
            except :
                pass

    def getSections(self):
        spaces = AntologyProcessor.getAverage(self.full_text)
        self.sections = AntologyProcessor.getSections(self.full_text , spaces)

    def getPrincipalSection(self , extrait):
        try :
            if( AntologyProcessor.getElement(extrait , self.sections)==""):
                return AntologyProcessor.getElement(extrait , self.sections)
            else:
                return "..." + AntologyProcessor.getElement(extrait , self.sections)[:400] + "..."
        except :
            return AntologyProcessor.getElement(extrait , self.sections)
    




    