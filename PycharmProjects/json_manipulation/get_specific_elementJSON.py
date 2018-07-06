import json
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


input_file = "/home/francois/Documents/resultat_sans_index.json"





with open(input_file, 'r', encoding ='utf-8') as file:
    doc = Document()    # création du document latex
    doc.preamble.append(Command('title', 'Datacatalogue'))
    doc.preamble.append(Command('author', "françois d'anselme"))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))


    raw_text = file.read()
    raw_text= raw_text.replace('μ', 'micro')
    #raw_text = raw_text.repalce('')
    liste_all_enregistrements = raw_text.split('\n')    #chaque entrée est séparée par un '\n' dans le fichier resultat
    del liste_all_enregistrements[-1]                   #on supprime la derniére entrée qui est vide a cause du '\n'
    for i in range(len(liste_all_enregistrements)):
        '''liste_all_enregistrements[i] = liste_all_enregistrements[i].replace('_', '').replace('%', '').replace('~', '')
        liste_all_enregistrements[i] = liste_all_enregistrements[i].replace('#', '').replace('\'', '').replace('\'','')'''
        json_load = json.loads(liste_all_enregistrements[i])

        #enlevement d'une partie d'un titre qui produisait une erreur lors de la génération du PDF
        try:
            defaulttitle = str(json_load['defaultTitle'].replace('Информационна система на защитени зони от екологична мрежа Натура 2000 Регистър на защитените територии и защитените зони в България', ''))
        except AttributeError:
            defaulttitle = str(json_load['defaultTitle'][0].replace('Информационна система на защитени зони от екологична мрежа Натура 2000 Регистър на защитените територии и защитените зони в България', ''))

        try:
            with doc.create(Section(defaulttitle)):

                try:
                    if type(json_load['defaultAbstract']) is list:
                        defaultabstract = json_load['defaultAbstract'][0]
                    else:
                        defaultabstract = json_load['defaultAbstract']
                    with doc.create(Subsection('Résumé:')):
                        doc.append(defaultabstract)
                except KeyError:
                    with doc.create(Subsection('Résumé:')):
                        doc.append("Pas de résumé disponible")
                try:
                    with doc.create(Subsection('Date de création:')):
                        doc.append(json_load['creationDate'])
                except KeyError:
                    result = 'pas de création date'
                try:
                    with doc.create(Subsection('Date de publication:')):
                        doc.append(json_load['publicationDate'])
                except KeyError:
                    result = 'pas de publication date'
                try:
                    with doc.create(Subsection('keywords:')):
                        doc.append(json_load['keyword'])
                except KeyError:
                    result = 'pas de keywords'

        except AttributeError:
            with doc.create(Section(json_load['defaultTitle'][0])):

                try:
                    with doc.create(Subsection('Résumé:')):
                        doc.append(json_load['abstract'])
                except KeyError:
                    with doc.create(Subsection('Résumé:')):
                        doc.append("pas d'abstract disponible")
                try:
                    with doc.create(Subsection('Date de création:')):
                        doc.append(json_load['creationDate'])
                except KeyError:
                    result = 'pas de création date'
                try:
                    with doc.create(Subsection('Date de publication:')):
                        doc.append(json_load['publicationDate'])
                except KeyError:
                    result = 'pas de publication date'
                try:
                    with doc.create(Subsection('keywords:')):
                        doc.append(json_load['keyword'])
                except KeyError:
                    result = 'pas de keywords'

    doc.generate_pdf('/home/francois/basic_maketitle2', clean_tex=False)
tex = doc.dumps() # The document as string in LaTeX syntax
'''
  print(json_load['defaultTitle'])
    print(json_load['keyword'])

    print(json_load['creationDate'])

    print(json_load['abstract'])

    print(json_load['publicationDate'])
defaultTitle
keyword
creationDate
abstract
publicationDate
'''