from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, PageBreak
from reportlab.lib.pagesizes import A4

# Отступы для титульного листа
TITLE_MARGINS = {
    'leftMargin': 72,    # 1 дюйм = 72 пункта
    'rightMargin': 72,
    'topMargin': 50,    # 2 дюйма
    'bottomMargin': 65
}

# Отступы в остальном документе
NORMAL_MARGINS = {
    'leftMargin': 40,
    'rightMargin': 40,
    'topMargin': 60,
    'bottomMargin': 40
}

# Создаем фрейм для титульной страницы
page_width, page_height = A4
title_frame = Frame(
    TITLE_MARGINS['leftMargin'],
    TITLE_MARGINS['bottomMargin'],
    page_width - TITLE_MARGINS['leftMargin'] - TITLE_MARGINS['rightMargin'],
    page_height - TITLE_MARGINS['topMargin'] - TITLE_MARGINS['bottomMargin'],
    id='title_frame'
)

# Фрейм для обычных страниц
normal_frame = Frame(
    NORMAL_MARGINS['leftMargin'],
    NORMAL_MARGINS['bottomMargin'],
    page_width - NORMAL_MARGINS['leftMargin'] - NORMAL_MARGINS['rightMargin'],
    page_height - NORMAL_MARGINS['topMargin'] - NORMAL_MARGINS['bottomMargin'],
    id='normal_frame'
)
