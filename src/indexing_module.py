import os,math,json

# Modulo Filters
from filters import *

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
        tf = 1 + math.log(freq_values[term],2)

        if term in inv_index:
            inv_index[term][1][doc]=tf
        else:
            inv_index[term] = (0,{doc:tf})

    return inv_index

# Calculo del IDF  para cada termino de la coleccion y de la longitud de los documentos
def idf_docweight_process(inv_index,n_docs):
    doc_weights = {}
    for term in inv_index:
        inv_index[term] = (math.log(n_docs/len(inv_index[term][1]),2),inv_index[term][1])
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
    index = 1
    for doc in files:
        if os.path.isfile(dir+doc):
            if index%1000 == 0:
                print("Documentos: "+str(index))
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
            # Cerramos el fichero
            f.close()
            index += 1
    # Calculamos el IDF para cada termino
    inv_index,doc_weights = idf_docweight_process(inv_index,len(files))

    # Guardamos las variables en ficheros
    save_variable(inv_index,'IndiceInvertido.dat')
    save_variable(doc_weights,'PesoDocumentos.dat')

