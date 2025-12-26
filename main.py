import json

from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Frame, PageTemplate, NextPageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config.config import font_name, year
from style.frames import normal_frame, title_frame, NORMAL_MARGINS
from style.styles import *
from charts import add_question_with_chart


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

document = BaseDocTemplate(
    f"otchet-student_{SPECIALITY_CODE}-{SPECIALITY_NAME}.-{FIELD_OF_STUDY}.pdf",
    pagesize=A4,
    **NORMAL_MARGINS  # Распаковываем словарь с отступами
)

# Создаем шаблоны
title_template = PageTemplate(id='TitlePage', frames=title_frame)
normal_template = PageTemplate(id='NormalPage', frames=normal_frame)

# Добавляем шаблоны в документ
document.addPageTemplates([title_template, normal_template])

content = []

content.append(NextPageTemplate('TitlePage'))

# Создание титульного листа
content.append(Paragraph("""
ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ

«СЕВЕРО-ОСЕТИНСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ ИМЕНИ
КОСТА ЛЕВАНОВИЧА ХЕТАГУРОВА»""", style=front_page_paragraph_1), )
content.append(Spacer(width=10, height=35))
content.append(
    Image('img/sogu_logo.jpg', width=117, height=90)
)
content.append(Spacer(width=10, height=75))

content.append(
    Paragraph('АНАЛИТИЧЕСКИЙ ОТЧЕТ', style=front_page_paragraph_2)
)
content.append(Spacer(width=10, height=20))
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
content.append(Spacer(width=10, height=350))
content.append(Paragraph('ВЛАДИКАВКАЗ – 2025', style=front_page_paragraph_4))
content.append(PageBreak())

content.append(NextPageTemplate('NormalPage'))

# Добавление отчёта по вопросам

content.append(Paragraph('ОСНОВНЫЕ ВЫВОДЫ ПО РЕЗУЛЬТАТАМ ИССЛЕДОВАНИЯ', style=main_title_style))

questions: list[dict] = survey['questions']

# 1 Вопрос
question = questions[0]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

improved = answers['Безусловно улучшилось'] + answers['Скорее, улучшилось']
worsened = answers['Скорее, ухудшилось'] + answers['Безусловно ухудшилось']
remained = answers['Осталось неизменным']

content.append(Paragraph(
    f'{improved} студентов данной образовательной программы считает, что качество обучения в СОГУ в {year} учебном году улучшилось по сравнению с предыдущим годом, в то время как {worsened}% - считают, что качество обучения ухудшилось, {remained}% - качество обучения осталось на прежнем уровне (рис. 1).', style=main_style
))

# 2 Вопрос
question = questions[1]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

satisfied = answers['Полностью удовлетворен'] + answers['Скорее, удовлетворен']
unsatisfied = answers['Скорее, не удовлетворен'] + answers['Полностью не удовлетворен']
fifty_fifty = answers['Отчасти удовлетворен, отчасти нет']

content.append(Paragraph(
    f'Удовлетворённость студентов данной образовательной программы качеством образования в СОГУ составила {satisfied}%, доля студентов, неудовлетворительно оценивающих предоставляемые услуги составила всего {unsatisfied}%, отчасти удовлетворены, отчасти нет – {fifty_fifty}% (рис. 2).   ', style=main_style
))

# 3 Вопрос
question = questions[2]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

sorted_answers: list[tuple] = sorted(answers.items(), key=lambda x: x[1])

average_satisfaction_index = sum([float(index) for answer, index in answers.items()])/len(answers)
average_satisfaction_index = round(average_satisfaction_index, 2) # усечения до двух знаков

least_satisfied_1, least_satisfied_2 = sorted_answers[0], sorted_answers[1]
least_satisfied_3 = sorted_answers[2]
most_satisfied_1, most_satisfied_2 = sorted_answers[-1], sorted_answers[-2]

content.append(Paragraph(
    f'Индекс удовлетворенности студентов, обучающихся по данной образовательной программе, различными аспектами, поддерживающими процесс обучения в СОГУ составил i={average_satisfaction_index} баллов (рис. 3). В меньшей степени студенты удовлетворены пунктами: «{least_satisfied_1[0]}» (i={least_satisfied_1[1]}),  «{least_satisfied_2[0]}» ({least_satisfied_2[1]}), «{least_satisfied_3[0]}» ({least_satisfied_3[1]}), а в большей степени пунктами: «{most_satisfied_1[0]}» ({most_satisfied_1[1]}) и «{most_satisfied_2[0]}» ({most_satisfied_2[1]})', style=main_style
))

# 4 Вопрос
question = questions[3]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

recommend = round(answers['Безусловно порекомендую'] + answers['Скорее, порекомендую'], 2)
not_recomend = round(answers['Безусловно не порекомендую'] + answers['Скорее, не порекомендую'], 2)

content.append(Paragraph('Некоторые мониторинговые исследования отмечают одним из лучших инструментов для определения успешности вуза оценку уровня лояльности ее студентов, которая выражается через готовность к рекомендациям и возвращению за образовательными услугами.',
                         style=main_style))

content.append(Paragraph(
    f'В случае необходимости получения образовательных услуг, порекомендуют обратиться в СОГУ {recommend}% опрошенных студентов данной образовательной программы и лишь {not_recomend}% - не порекомендуют (рис. 4).',
    style=main_style
))

# 5 Вопрос
question = questions[4]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

positive = round(answers['Безусловно да'] + answers['Скорее, да'], 2)
negative = round(answers['Скорее, нет'] + answers['Безусловно нет'], 2)

content.append(Paragraph(
    f'За дополнительным образованием или повышением квалификации в СОГУ снова готовы обратиться {positive}% опрошенных, {negative}% - предпочтут другое образовательное учреждение (рис. 5).  ',
    style=main_style
))

# 6 Вопрос
question = questions[5]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

no_difficulties = round(answers['У меня не будет никаких проблем с трудоустройством'], 2)
minor_difficulties = round(answers['Возникнут незначительные сложности, итоге в найду работу'], 2)
major_difficulties = round(answers['Скорее всего я не смогу найти работу'], 2)

content.append(Paragraph(
    f'Большинство студентов данной образовательной программы положительно оценивают свои шансы на трудоустройство – {no_difficulties}% опрошенных считают, что у них не будет никаких сложностей с этим, у {minor_difficulties}% - возможны незначительные сложности, которые все же позволят найти работу по специальности (рис. 6). Лишь {major_difficulties}% студентов отмечают, что скорее всего не смогут найти работу.   ',
    style=main_style
))

# 7 Вопрос
question = questions[6]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

will_work_in_related_field = round(answers['Попробую трудоустроиться в смежных сферах'], 2)
continue_education = round(answers['Продолжу обучение повышение квалификации по своей специальности'], 2)

will_follow_current_speciality = will_work_in_related_field + continue_education

if will_follow_current_speciality > 0.49:
    confidence_in_speciality = 'твердости намерения'
else:
    confidence_in_speciality = 'неуверенности в намерении'

content.append(Paragraph(
    f'Ответы, представленные на рисунке 7, говорят о {confidence_in_speciality} студентов следовать выбранной специальности, так как в случае НЕ успешности в вопросе трудоустройства по специальности {will_work_in_related_field}% - попробуют трудоустроиться в смежных сферах, а {continue_education}% - продолжат обучение по своей специальности.   ',
    style=main_style
))

# 8 Вопрос
question = questions[7]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

salary_min = round(answers['11-20 тыс. руб. в месяц'], 2)
salary_second_min = round(answers['21-30 тыс. руб. в месяц'], 2)

content.append(Paragraph(
    f'На минимальную заработную плату в размере 11-20 тыс. рублей готовы выйти – {salary_min}%, а на 21-30 тыс. рублей  - {salary_second_min}% (рис. 8).',
    style=main_style
))

# 9 Вопрос
question = questions[8]
wording, answers = question['question'], question['answers']

add_question_with_chart(content, wording, answers, chart_type='horizontal_bar')

self_hired = round(answers['Предпочитаю работать на себя'], 2)
private_company = round(answers['В частной коммерческой компании'], 2)
state_budgetary_institution = round(answers['В государственном бюджетном учреждении (федеральное, республиканское, муниципальное)'], 2)

content.append(Paragraph(
    f'Большинство студентов данной образовательной программы предпочитают работать на себя ({self_hired}%) или в частной коммерческой компании ({private_company}%). В государственном бюджетном учреждении свое трудоустройство видят {state_budgetary_institution}% опрошенных (рис. 9). ',
    style=main_style
))



document.build(content)
