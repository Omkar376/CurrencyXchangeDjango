# -*- coding: utf-8 -*-


from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
import numpy as np
import uuid
from datetime import datetime
from reportlab.lib.styles import ParagraphStyle, TA_CENTER

class Report:
    def generate_report(user, message, dfdata):
        #Transaction Table generation
        GRID_STYLE = TableStyle(
                    [('GRID', (0, 0), (-1, -1), 0.15, colors.dodgerblue),
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT')])
        transaction_table = Table([list(dfdata.columns)] + np.array(dfdata).tolist())
        transaction_table.setStyle(GRID_STYLE)
        filename = str(uuid.uuid4())
        filepath = r"C:\Users\lncoretech\New folder\CurrencyXchange\reports" + f"\\{filename}.pdf"
        doc = SimpleDocTemplate(filepath, pagesize=letter)

        #Adding Headers and Text
        story = [] 
        parastyle = ParagraphStyle('parrafos',
                alignment = TA_CENTER,
                fontSize = 30,
                fontName="Times-Roman",
                textColor= colors.dodgerblue)
        story.append(Paragraph("CurrencyXchange" , parastyle))
        story.append(Spacer(1, 30))
        parastyle2 = ParagraphStyle('parrafos',
                            alignment = TA_CENTER,
                            fontSize = 15,
                            fontName="Times-Roman")
        story.append(Paragraph(message,parastyle2))
        story.append(Spacer(1, 30))
        parastyle3 = ParagraphStyle('parrafos',
                            alignment = TA_CENTER,
                            fontSize = 10)
        story.append(Paragraph("Account: " + user , parastyle3))
        story.append(Paragraph("( Transactions report generated on: " + str(datetime.now()) +" )" , parastyle3))
        story.append(Spacer(1, 12))
        element = story + [] 
        element.append(transaction_table)
        
        #Saving pdf file
        doc.build(element)
        return filepath
