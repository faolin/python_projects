'''CREATION DUN DOCUMENT LATEX A PARTIR DE TEXTE / DONNEES PYTHON'''
# begin-doc-include
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


def fill_document(doc):
    """Add a section, a subsection and some text to the document.
    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    test = "je suis un titre plutot long mais court a lafois ciic"
    with doc.create(Section(test)):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')


if __name__ == '__main__':


    # Document with `\maketitle` command activated
    doc = Document()

    doc.preamble.append(Command('title', 'Datacatalogue'))
    doc.preamble.append(Command('author', "françois d'anselme"))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    fill_document(doc)

    # Add stuff to the document
    with doc.create(Section('A second section')):
        doc.append('Some text.')

    doc.generate_pdf('/home/francois/basic_maketitle2', clean_tex=False)
tex = doc.dumps() # The document as string in LaTeX syntax