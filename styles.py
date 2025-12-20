from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Frame, PageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
font_name = 'DejaVu'

# Основной стиль документа
main_style = ParagraphStyle(
    "main_style",
    fontName = font_name,
    fontSize=10
)

main_title_style = ParagraphStyle(
    "main_title_style",
    parent=main_style,
    alignment=TA_CENTER
)


# Стили титульного листа

pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
font_name = 'DejaVu'
# Выравнивание по центру, один шрифт
front_page_base = ParagraphStyle(
    "front_page_base",
    fontName = font_name,
    alignment=TA_CENTER,
)

front_page_paragraph_1 = ParagraphStyle(
    "front_page_paragraph_1",
    parent=front_page_base,
    fontSize=10
)

front_page_paragraph_2 = ParagraphStyle(
    "front_page_paragraph_2",
    parent=front_page_base,
    fontSize=14
)

front_page_paragraph_3 = ParagraphStyle(
    "front_page_paragraph_3",
    parent=front_page_base,
    fontSize=12
)

front_page_paragraph_4 = ParagraphStyle(
    "front_page_paragraph_4",
    parent=front_page_base,
    fontSize=12
)
