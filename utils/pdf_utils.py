from PyPDF2 import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


def clean_text_for_pdf(text):
    text = text.replace("$$", "")
    text = text.replace("\\(", "").replace("\\)", "")
    text = text.replace("**", "")
    text = text.replace("\n", "<br/>")
    return text


def create_pdf(text):
    cleaned = clean_text_for_pdf(text)

    doc = SimpleDocTemplate("output.pdf")
    styles = getSampleStyleSheet()

    story = []

    for para in cleaned.split("<br/><br/>"):
        story.append(Paragraph(para, styles["Normal"]))
        story.append(Paragraph("<br/>", styles["Normal"]))

    doc.build(story)
