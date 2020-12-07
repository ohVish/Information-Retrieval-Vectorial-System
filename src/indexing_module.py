import os,abc,re,math,json

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

# Calculo del TF para la lista de terminos del documento (1era Parte)
def tf_process(terms):
    freq_values = {}
    for word in terms:
        if word in freq_values:
            freq_values[word]+=1
        else:
            freq_values[word]=1
    return freq_values

# Calculo del TF para la lista de terminos del documento (2da Parte)
def inv_index_process(inv_index,freq_values,doc):
    for term in freq_values:
        tf = 1 + math.log(freq_values[term],10)

        if term in inv_index:
            inv_index[term][1][doc]=tf
        else:
            inv_index[term] = (0,{doc:tf})

    return inv_index

# Calculo del IDF  para cada termino de la coleccion y de la longitud de los documentos
def idf_docweight_process(inv_index,n_docs):
    doc_weights = {}
    for term in inv_index:
        inv_index[term] = (math.log(n_docs/len(inv_index[term][1]),10),inv_index[term][1])
        idf = inv_index[term][0]
        docs_term = inv_index[term][1]
        for doc in docs_term:
            tf_idf = idf * docs_term[doc]
            if doc in doc_weights:
                doc_weights[doc] += math.pow(tf_idf,2)
            else:
                doc_weights[doc] = math.pow(tf_idf,2)

    for doc in doc_weights:
        doc_weights[doc] = math.sqrt(doc_weights[doc])

    return (inv_index,doc_weights)

# Funcion para guardar variable en un fichero
def save_variable(var,filename):
    with open('./src/'+filename,'w') as f:
        json.dump(var,f)

def indexate_corpus():
    filter_handlerC,filter_handlerT = init_filters()
    dir = './resources/corpus/' 
    files = os.listdir(dir)
    inv_index = {}
    for doc in files:
        if os.path.isfile(dir+doc):
            # Leer el texto del documento
            f = open(dir+doc,'r')
            doc_text = str(f.read())
            # Preprocesamiento de caracteres
            doc_text = filter_handlerC.apply_filters(doc_text)
            # Division de documento en lista de terminos
            terms = doc_text.split(' ')
            # Preprocesamiento de terminos
            terms = filter_handlerT.apply_filters(terms)
            # Calculo del TF (Term Frequency)
            # 1era parte, frecuencia de los terminos
            freq_values =  tf_process(terms)
            # 2da parte, TF e indice invertido
            inv_index = inv_index_process(inv_index,freq_values,doc)
    # Calculamos el IDF para cada termino
    inv_index,doc_weights = idf_docweight_process(inv_index,len(files))

    # Guardamos las variables en ficheros
    save_variable(inv_index,'IndiceInvertido.dat')
    save_variable(doc_weights,'PesoDocumentos.dat')



indexate_corpus()
