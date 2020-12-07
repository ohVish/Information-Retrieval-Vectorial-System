from indexing_module import indexate_corpus
from retrieval_module import retrieve_documents

if __name__ == '__main__':
    print('Select your action:')
    print('\t1. Index corpus')
    print('\t2. Make a query')
    print('\t3. Exit')
    selec = ''
    while selec not in ['1','2','3']:
        selec = input('>')
        if selec == '1':
            indexate_corpus()
        elif selec == '2':
            retrieve_documents()