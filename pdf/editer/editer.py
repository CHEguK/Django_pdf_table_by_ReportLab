stat = {'Всего диалогов': 
                    {'Вконтакте': 0, 
                     'Телеграм': 2, 
                     'Сайт': 796, 
                     'Приложение эл.почта': 32, 
                     'Приложение чат': 493, 
                     'Все': 1323}, 

         'Диалоги оператора': {'Вконтакте': 0, 
                               'Телеграм': 0, 
                               'Сайт': 41, 
                               'Приложение эл.почта': 28, 
                               'Приложение чат': 337, 
                               'Все': 406}, 

         'Диалоги бота': {'Вконтакте': 0, 
                          'Телеграм': 1, 
                          'Сайт': 45, 
                          'Приложение эл.почта': 0, 
                          'Приложение чат': 201, 'Все': 247}, 
         
         '% Исходящих бота': {'Вконтакте': 0, 
                              'Телеграм': 50.0, 
                              'Сайт': 5.65, 
                              'Приложение эл.почта': 0.0, 
                              'Приложение чат': 40.77, 
                              'Все': 18.67}, 

         'Кол-во входящих сообщений': {'Вконтакте': 0, 
                                       'Телеграм': 2, 
                                       'Сайт': 812, 
                                       'Приложение эл.почта': 20, 
                                       'Приложение чат': 1366, 
                                       'Все': 2200},

         'Кол-во исходящих оператора': {'Вконтакте': 0, 
                                        'Телеграм': 0, 
                                        'Сайт': 44, 
                                        'Приложение эл.почта': 30, 
                                        'Приложение чат': 646, 
                                        'Все': 720}, 

         'Кол-во сообщений на к-е бот ответил': {'Вконтакте': 0, 
                                                 'Телеграм': 1, 
                                                 'Сайт': 45, 
                                                 'Приложение эл.почта': 0, 
                                                 'Приложение чат': 230, 
                                                 'Все': 276}, 

         'Кол-во сообщений на к-е бот ответил неверно': {'Вконтакте': 0, 
                                                         'Телеграм': 0, 
                                                         'Сайт': 1, 
                                                         'Приложение эл.почта': 0, 
                                                         'Приложение чат': 7, 
                                                         'Все': 8}, 
         '% Ошибок': {'Вконтакте': 0, 
                      'Телеграм': 0.0, 
                      'Сайт': 2.22, 
                      'Приложение эл.почта': 0, 
                      'Приложение чат': 3.04, 
                      'Все': 2.9}}


def json2lists(data_json):
    columns_name = list(data_json.keys())
    rows = list(data_json[columns_name[0]].keys())

    columns_name.insert(0, '')
    columns_name.insert(1, 'Канал')
    columns_name = list(map(lambda x: x.replace(" ", "\n"), columns_name))

    table_data = list()
    columns_name = ['', 
                    '', 
                    'Всего\nдиалогов', 
                    'Диалоги\nоператора', 
                    'Диалоги\nбота', 
                    '%\nИсходящих\nбота', 
                    'Кол-во\nвходящих\nсообщений', 
                    'Кол-во\nисходящих\nоператора', 
                    'Кол-во\nсообщений\nна к-е\nбот\nответил', 
                    'Кол-во\nсообщений\nна к-е\nбот\nответил\nневерно', 
                    '%\nОшибок']

    table_data.append(columns_name)
    for row in rows:
        line = list()
        line.append(row.replace(" ", "\n"))
        for column in data_json.values():
            line.append(column[row])
        if row=='Сайт':
            line.insert(0, Image('resources/img2.jpg', width=30, height=15.9))
        elif row=='Вконтакте':
            line.insert(0, Image('resources/img3.jpg', width=30, height=26.1))
        elif row=='Телеграм':
            line.insert(0, Image('resources/img4.jpg', width=30, height=26.1))
        else:
            line.insert(0, '')
        table_data.append(line)
    return table_data

from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib import colors

def drawMyRuler(pdf):
    pdf.drawString(100,520, 'x100')
    pdf.drawString(200,520, 'x200')
    pdf.drawString(300,520, 'x300')
    pdf.drawString(400,520, 'x400')
    pdf.drawString(500,520, 'x500')
    pdf.drawString(600,520, 'x600')
    pdf.drawString(700,520, 'x700')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')


fileName = 'MyDoc.pdf'
documentTitle = 'Document Title!'
title = 'Statistics'
SubTitle = 'Statistcs for a week'

data = json2lists(stat)

textLines = ['% исходящих бота = диалоги бота / всего диалогов', 
             '% ошибок бота = кол-во сообщений, на которые бот ответил неверно / кол-во сообщений, на которые бот ответил',
            ]

image = 'resources/img1.jpg'


def pdf():
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph,Table,TableStyle,Frame
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics


    story = []
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={fileName}'

    pdfmetrics.registerFont(TTFont('ubuntu', 'ubuntu.ttf'))
    pdfmetrics.registerFont(TTFont('ubuntu-bold', 'ubuntu-bold.ttf'))

    pdf=canvas.Canvas(response)
    pdf.setPageSize((842, 540)) # Длина и высота листа в point'ах

    header = pdf.beginText(250,480)
    header.setFont('ubuntu-bold', size=28)
    header.textLine('Статистика по всем каналам')
    pdf.drawText(header)
    
    for i in range(1,20):
        header = pdf.beginText(250,480)
        header.setFont('ubuntu-bold', size=28)
        header.textLine('Статистика по всем каналам')
        pdf.drawText(header)
        
        # drawMyRuler(pdf)
        interval = pdf.beginText(290,440)
        interval.setFont('ubuntu-bold', size=28)
        interval.textLine('(23.04.2020 - 22.04.2020)')
        pdf.drawText(interval)
        
        flow_obj=[]
        table = Table(data)
        ts=TableStyle([('FONTNAME', (1,0), (-1,0), 'ubuntu-bold'),
                        ('LEFTPADDING', (1,0), (-1,0), 3),
                        ('RIGHTPADDING', (1,0), (-1,0), 3),
                        ('BOTTOMPADDING', (1,0), (-1,0), 30),
                        ('FONTNAME', (1,1), (-1,-1), 'ubuntu'),
                        ('FONTNAME', (1,-1), (-1,-1), 'ubuntu-bold'),
                        ('FONTSIZE', (0,0), (-1,-1), 13),
                        ('ALIGN', (1,0), (-1,0), 'CENTER'),
                        ('ALIGN', (0,1), (0,-1), 'CENTER'),
                        ('VALIGN', (1,0), (-1,0), 'TOP'),
                        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
                        ('LEFTPADDING', (2,1), (-1,-1), 6),
                        ('BOTTOMPADDING', (1,1), (-1,-1), 6),
                        ('VALIGN', (2,1), (-1,-1), 'MIDDLE'),
                        ('GRID', (1,0), (-1,-1), 0.5, colors.Color(0.84, 0.84, 0.84, 1)),])
        table.setStyle(ts)

        flow_obj.append(table)

        frame=Frame(0,100,842,300)
        frame.addFromList(flow_obj, pdf)

        text = pdf.beginText(80,80)
        text.setFont('ubuntu', size=11)
        for line in textLines:
            text.textLine(line)
        pdf.drawText(text)

        pdf.drawInlineImage(image, -1, 478, width=35, height=23)

        pdf.showPage()

    pdf.save()

    return response