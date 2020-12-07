import os,abc,re

class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self,text):
        pass

class MinusFilter(Filter):
    def execute(self,text):
        return text.lower()

class RegexFilter(Filter):
    def __init__(self,regex,rplc):
        self.regex = regex
        self.rplc = rplc
    
    def execute(self,text):
        return re.sub(self.regex,self.rplc,text)

class FilterManager():
    def __init__(self):
        self.filters = set()

    def addFilter(self,filter):
        self.filters.add(filter)
    
    def apply_filters(self,text):
        for filter in self.filters:
            filter.execute(text)


def init_filters():
    

def preprocess_corpus():
    filter_handler = init_filters()
    files = os.listdir('./resources/corpus/')
    for doc in files:
        if os.path.isfile(doc):
            f = open(doc,'r')
            doc_text = str(f.read())
            doc_text = filter_handler.apply_filters(doc_text)
