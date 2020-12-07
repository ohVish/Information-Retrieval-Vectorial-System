import abc,re

# NLTK(Natural Language Toolkit) Package for Python
from nltk import PorterStemmer

# Clase Abstracta para los filtros
class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self,text):
        pass

# Filtros para el preprocesado de caracteres
class LowerFilter(Filter):
    def execute(self,text):
        return text.lower()

class RegexFilter(Filter):
    def __init__(self,regex,rplc):
        self.regex = regex
        self.rplc = rplc
    
    def execute(self,text):
        return re.sub(self.regex,self.rplc,text)

# Filtros para el preprocesamiento de terminos
class StopWordsFilter(Filter):
    def __init__(self,dir):
        f = open(dir,'r')
        self.stop_words = f.readlines()
        f.close()

    def execute(self,text):
        return [word for word in text if word not in self.stop_words]

class StemmerFilter(Filter):
    def __init__(self):
        self.ps = PorterStemmer()

    def execute(self, text):
        return [self.ps.stem(word) for word in text] 
    
class LengthFilter(Filter):
    def execute(self,text):
        return [word for word in text if len(word)>2]

# Gestor de Filtros
class FilterManager():
    def __init__(self):
        self.filters = set()

    def add_filter(self,filter):
        self.filters.add(filter)
    
    def apply_filters(self,text):
        for filter in self.filters:
            text = filter.execute(text)
        return text



def init_filters():

    filter_handlerC = FilterManager()
    filter_handlerC.add_filter(LowerFilter())
    filter_handlerC.add_filter(RegexFilter(r'[^-\w\']',' '))
    filter_handlerC.add_filter(RegexFilter(r'\b[0-9]+\b',' '))
    filter_handlerC.add_filter(RegexFilter(r'(-+ | -+)',' '))
    filter_handlerC.add_filter(RegexFilter(r' +',' '))

    filter_handlerT = FilterManager()
    filter_handlerT.add_filter(StopWordsFilter('./resources/stopwords'))
    filter_handlerT.add_filter(StemmerFilter())
    filter_handlerT.add_filter(LengthFilter())


    return (filter_handlerC,filter_handlerT)