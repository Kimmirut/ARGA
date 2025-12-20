import json

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Frame, PageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config.config import font_name, year
from styles import *


def build_pdf(path: str) -> None:
    """Создаёт pdf-документ из json-файла по заданному пути.


    Args:
        path (str): _description_
    """

with open('student_report_pmi.json', encoding='utf-8') as input_file:
    survey: dict = json.load(input_file)

SPECIALITY_CODE = survey['speciality_code']
SPECIALITY_NAME = survey['speciality_name']
FIELD_OF_STUDY = survey['field_of_study']




# Создание документа
# Название документа определяется по образцу:
# otchet-student_{код специальности}-{название направления}.-{направление подготовки}.pdf
# Например:
# otchet-student_01.03.02-prikladnaja-matematika-i-informatika.-programmirovanie-analiz-dannyh-i-matematicheskoe-modelirovanie.pdf
document = SimpleDocTemplate(
    f"otchet-student_{SPECIALITY_CODE}-{SPECIALITY_NAME}.-{FIELD_OF_STUDY}.pdf",
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=60,
    bottomMargin=40
)

content = []


# Создание титульного листа
content.append(Paragraph("""
ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ

«СЕВЕРО-ОСЕТИНСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ ИМЕНИ
КОСТА ЛЕВАНОВИЧА ХЕТАГУРОВА»""", style=front_page_paragraph_1), )

content.append(
    Image('img/sogu_logo.jpg')
)

content.append(
    Paragraph('АНАЛИТИЧЕСКИЙ ОТЧЕТ', style=front_page_paragraph_2)
)

content.append(
    Paragraph(
            f"""
            о результатах комплексного мониторингового исследования
            «Оценка качества образования в Северо-Осетинском государственном университете имени Коста Левановича Хетагурова» образовательной программы
            {SPECIALITY_CODE} {SPECIALITY_NAME}
            {FIELD_OF_STUDY}
            """, style=front_page_paragraph_3
    )
)

content.append(Paragraph('ВЛАДИКАВКАЗ – 2025', style=front_page_paragraph_4))
content.append(PageBreak())

# Добавление отчёта по вопросам

content.append(Paragraph('ОСНОВНЫЕ ВЫВОДЫ ПО РЕЗУЛЬТАТАМ ИССЛЕДОВАНИЯ', style=main_title_style))

questions: list[dict] = survey['questions']

# 1 Вопрос
question = questions[0]
wording, answers = question['question'], question['answers']

improved = answers['Безусловно улучшилось'] + answers['Скорее, улучшилось']
worsened = answers['Скорее, ухудшилось'] + answers['Безусловно ухудшилось']
remained = answers['Осталось неизменным']

content.append(Paragraph(
    f'{improved} студентов данной образовательной программы считает, что качество обучения в СОГУ в {year} учебном году улучшилось по сравнению с предыдущим годом, в то время как {worsened}% - считают, что качество обучения ухудшилось, {remained}% - качество обучения осталось на прежнем уровне (рис. 1).', style=main_style
))

# 2 Вопрос
question = questions[1]
wording, answers = question['question'], question['answers']

satisfied = answers['Полностью удовлетворен'] + answers['Скорее, удовлетворен']
unsatisfied = answers['Скорее, не удовлетворен'] + answers['Полностью не удовлетворен']
fifty_fifty = answers['Отчасти удовлетворен, отчасти нет']

content.append(Paragraph(
    f'Удовлетворённость студентов данной образовательной программы качеством образования в СОГУ составила {satisfied}%, доля студентов, неудовлетворительно оценивающих предоставляемые услуги составила всего {unsatisfied}%, отчасти удовлетворены, отчасти нет – {fifty_fifty}% (рис. 2).   ', style=main_style
))

# 3 Вопрос
question = questions[2]
wording, answers = question['question'], question['answers']

satisfaction = ...

content.append(Paragraph(
    f'Индекс удовлетворенности студентов, обучающихся по данной образовательной программе, различными аспектами, поддерживающими процесс обучения в СОГУ составил i=0,77 баллов (рис. 3). В меньшей степени студенты удовлетворены «удобством использования «Личного кабинета студента»» (i=0,64),  «доступностью специализированных компьютерных программ» (i=0,66), «качеством питания в столовых и буфетах» (i=0,65), а в большей степени «готовностью сотрудников деканата оказать помощь» (i=0,9) и «доступностью библиотечных ресурсов» (i=0,87)1.  ', style=main_style
))


document.build(content)
