from pypdf import PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy_cv(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Dennis Gustavsson")
    c.drawString(100, 730, "Senior Python Developer")
    c.drawString(100, 700, "Experience:")
    c.drawString(100, 680, "- Senior Developer at Tech Corp (2020-Present)")
    c.drawString(120, 665, "  * Built AI applications using Python and LangChain")
    c.drawString(120, 650, "  * Optimized backend performance by 50%")
    c.drawString(100, 620, "- Junior Developer at StartUp Inc (2018-2020)")
    c.drawString(120, 605, "  * Full stack development with React and Node.js")
    c.drawString(100, 570, "Skills:")
    c.drawString(100, 550, "Python, TypeScript, React, FastAPI, LangChain, SQL, Docker")
    c.drawString(100, 520, "Education:")
    c.drawString(100, 500, "B.Sc. Computer Science, KTH Royal Institute of Technology")
    c.save()

if __name__ == "__main__":
    create_dummy_cv("dummy_cv.pdf")
