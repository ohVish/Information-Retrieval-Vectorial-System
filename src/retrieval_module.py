import os,math,json

# Modulo Filters
from filters import *

# Funcion para cargar variable de un fichero
def load_variable(filename):
    with open('./src/'+filename,'r') as f:
        return json.load(f)

# Calculamos los documentos relacionados con la consulta
def query_process(terms,inv_index,doc_weights):
    query_docs = {}
    # Calculamos el numerador
    for term in terms:
        if term in inv_index:
            idf = inv_index[term][0]
            doclist = inv_index[term][1]
            for doc in doclist:
                if doc in query_docs:
                    query_docs[doc] += doclist[doc]*idf*idf
                else:
                    query_docs[doc] = doclist[doc]*idf*idf
    
    # Resultado final de la similitud
    for doc in query_docs:
        query_docs[doc] /= doc_weights[doc]

    return query_docs

# Obtiene el resumen para un documento concreto
def get_summary(doc):
    with open('./resources/corpus/'+doc,'r') as f:
        return f.readline()

def retrieve_documents():
    # Cargamos indice invertido y peso de los documentos
    inv_index = load_variable('IndiceInvertido.dat')
    doc_weights = load_variable('PesoDocumentos.dat')

    # Inicializamos los gestores de filtros
    filter_handlerC,filter_handlerT = init_filters()

    query = ''
    while query != 'E':
        # Leemos la consulta del usuario
        query = input("Enter your query (Press 'E' to quit search engine)> ")

        if query != 'E':
            # Preprocesamiento de la consulta
            text = filter_handlerC.apply_filters(query)
            terms = text.split(' ')
            terms = filter_handlerT.apply_filters(terms)

            query_docs = query_process(terms,inv_index,doc_weights)

            # Ordenar documentos segun ranking
            sorted_docs = sorted(query_docs.items(),key=lambda x: x[1],reverse=True)

            # Mostrar n primeros resultados
            n = 10
            i = 0
            for val in sorted_docs:
                if i==10:
                    break
                else:
                    print('Document ID:'+str(val[0])+' (weight: '+str(val[1])+')')
                    print('Summary:')
                    print(get_summary(val[0]))
                    i+=1