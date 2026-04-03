import os
import pandas as pd
import PyPDF2
from docx import Document

def read_file(file_path):
    # File ka extension nikalo
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(file_path)
        return df, 'dataframe'

    elif ext == '.xlsx':
        df = pd.read_excel(file_path)
        return df, 'dataframe'

    elif ext == '.pdf':
        txt = ''
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                txt += page.extract_text()
        return txt, 'text'

    elif ext == '.docx':
        doc = Document(file_path)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text, 'text'

    else:
        return None, 'unsupported'