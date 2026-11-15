from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_text_from_cv(file):
    extension = Path(file.name).suffix.lower()

    file.seek(0)

    if extension == '.pdf':
        reader = PdfReader(file)

        text = '\n'.join(
            page.extract_text() or ''
            for page in reader.pages
        )

    elif extension == '.docx':
        document = Document(file)

        text = '\n'.join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError('Formati i CV-se nuk mbeshtetet.')

    file.seek(0)

    return text.strip()

def extract_skills_from_cv(text):
    skills_database = [
        'Python',
        'Java',
        'JavaScript',
        'Django',
        'React',
        'Next.js',
        'HTML',
        'CSS',
        'SQL',
        'PostgreSQL',
        'MySQL',
        'C++',
        'C#',
        'PHP',
        'Laravel',
        'Node.js',
        'Git',
        'GitHub',
        'Docker',
        'Excel',
        'Machine Learning',
        'Data Analysis',
        'REST API',
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in skills_database:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills