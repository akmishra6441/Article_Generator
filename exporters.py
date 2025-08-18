from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
import pypandoc

def export_to_pdf(article, filename="article.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = [Paragraph(article, styles["Normal"])]
    doc.build(content)
    return filename

def export_to_word(article, filename="article.docx"):
    doc = Document()
    doc.add_paragraph(article)
    doc.save(filename)
    return filename

def export_to_md(article, filename="article.md"):
    pypandoc.convert_text(article, 'md', format='md', outputfile=filename, extra_args=['--standalone'])
    return filename
