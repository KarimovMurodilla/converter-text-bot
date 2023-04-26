import fitz, docx

from pathlib import Path

class ExtractText:
    def __init__(self):
        self.__dir = Path(__file__).resolve().parent / 'files'


    def pdfToText(self, filename):
        with fitz.open(self.__dir / filename) as doc:
            text = ''
            for page in doc:
                text += page.getText()

        return text


    def docxToText(self, filename):
        doc = docx.Document(self.__dir / filename)

        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)

        return '\n'.join(fullText)
    

    def get_dir(self):
        return self.__dir