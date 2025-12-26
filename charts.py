from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Импортируем основной стиль из модуля styles
try:
    from style.styles import main_style
except ImportError:
    # Если модуль не найден, создаем минимальный стиль
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    # Попытка регистрации шрифта, если он доступен
    try:
        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
        font_name = 'DejaVu'
    except:
        font_name = 'Helvetica'

    main_style = ParagraphStyle(
        "main_style",
        fontName=font_name,
        fontSize=10
    )


def create_pie_chart(wording, answers, style=None):
    """Создание круговой диаграммы"""
    if style is None:
        style = main_style

    # Подготовка данных
    labels = list(answers.keys())
    data = list(answers.values())

    # Создание рисунка и диаграммы
    drawing = Drawing(400, 250)
    pie = Pie()
    pie.data = data
    pie.labels = labels
    pie.x, pie.y = 150, 50  # Положение диаграммы на рисунке

    # Применение стиля к меткам диаграммы
    pie.labels.fontName = style.fontName
    pie.labels.fontSize = style.fontSize
    if hasattr(style, 'textColor'):
        pie.labels.fillColor = style.textColor

    # Цвета для секторов
    pie.slices.fillColor = colors.HexColor('#2E86AB')
    pie.slices.strokeWidth = 0.5

    # Легенда с процентами
    legend = Legend()
    legend.x, legend.y = 50, 200
    legend.colorNamePairs = [(colors.HexColor('#2E86AB'), f'{l} ({v}%)') for l, v in zip(labels, data)]

    # Применение стиля к легенде
    legend.fontName = style.fontName
    legend.fontSize = style.fontSize
    if hasattr(style, 'textColor'):
        legend.textColor = style.textColor

    legend.boxAnchor = 'nw'

    drawing.add(pie)
    drawing.add(legend)
    return drawing


def create_bar_chart(wording, answers, style=None):
    """Создание вертикальной столбчатой диаграммы"""
    if style is None:
        style = main_style

    labels = list(answers.keys())
    data = [list(answers.values())]  # данные должны быть списком списков

    drawing = Drawing(400, 250)
    bc = VerticalBarChart()
    bc.x, bc.y = 50, 50
    bc.height, bc.width = 150, 300
    bc.data = data
    bc.categoryAxis.categoryNames = labels
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100  # т.к. данные в процентах

    # Применение стиля к подписям
    bc.categoryAxis.labels.fontName = style.fontName
    bc.categoryAxis.labels.fontSize = style.fontSize
    bc.valueAxis.labels.fontName = style.fontName
    bc.valueAxis.labels.fontSize = style.fontSize

    if hasattr(style, 'textColor'):
        bc.categoryAxis.labels.fillColor = style.textColor
        bc.valueAxis.labels.fillColor = style.textColor

    # Настройка внешнего вида
    bc.barWidth = 15
    bc.groupSpacing = 10
    bc.barLabelFormat = '%0.1f%%'  # подписи над столбцами
    bc.barLabels.nudge = 10
    bc.barLabels.fontName = style.fontName
    bc.barLabels.fontSize = max(style.fontSize - 2, 8)  # Немного меньше основного стиля

    if hasattr(style, 'textColor'):
        bc.barLabels.fillColor = style.textColor

    # Цвет заливки и обводки
    bc.bars[0].fillColor = colors.HexColor('#A23B72')
    bc.bars[0].strokeColor = colors.HexColor('#7A2A58')

    drawing.add(bc)
    return drawing


def create_horizontal_bar_chart(wording, answers, style=None):
    """Создание горизонтальной столбчатой диаграммы"""
    if style is None:
        style = main_style

    labels = list(answers.keys())
    data = [list(answers.values())]

    drawing = Drawing(400, 250)
    hbc = HorizontalBarChart()
    hbc.x, hbc.y = 120, 50  # увеличен отступ слева для длинных подписей
    hbc.height, hbc.width = 150, 250
    hbc.data = data
    hbc.categoryAxis.categoryNames = labels
    hbc.valueAxis.valueMin = 0
    hbc.valueAxis.valueMax = 100

    # Применение стиля к подписям
    hbc.categoryAxis.labels.fontName = style.fontName
    hbc.categoryAxis.labels.fontSize = style.fontSize
    hbc.valueAxis.labels.fontName = style.fontName
    hbc.valueAxis.labels.fontSize = style.fontSize

    if hasattr(style, 'textColor'):
        hbc.categoryAxis.labels.fillColor = style.textColor
        hbc.valueAxis.labels.fillColor = style.textColor

    # Настройки
    hbc.barWidth = 12
    hbc.groupSpacing = 8
    hbc.barLabelFormat = '%0.1f%%'
    hbc.barLabels.nudge = 5
    hbc.barLabels.fontName = style.fontName
    hbc.barLabels.fontSize = max(style.fontSize - 2, 8)

    if hasattr(style, 'textColor'):
        hbc.barLabels.fillColor = style.textColor

    # Цвет
    hbc.bars[0].fillColor = colors.HexColor('#F18F01')
    hbc.bars[0].strokeColor = colors.HexColor('#C67C00')

    drawing.add(hbc)
    return drawing


def add_question_with_chart(content, wording, answers, chart_type='pie', style=None):
    """Добавление вопроса с диаграммой в документ"""
    styles = getSampleStyleSheet()

    if style is None:
        style = main_style

    # 1. Добавляем формулировку вопроса
    content.append(Paragraph(wording, style))
    content.append(Spacer(1, 12))

    # 2. Создаём и добавляем саму диаграмму
    if chart_type == 'pie':
        chart = create_pie_chart(wording, answers, style)
    elif chart_type == 'bar':
        chart = create_bar_chart(wording, answers, style)
    elif chart_type == 'horizontal_bar':
        chart = create_horizontal_bar_chart(wording, answers, style)
    else:
        raise ValueError(f"Неизвестный тип диаграммы: {chart_type}")

    content.append(chart)
    content.append(Spacer(1, 24))  # отступ перед следующим вопросом
