from .models import *
from wrong_note.settings import *
import xlrd
import os
import time


def load(filepath):
    results = []
    table = xlrd.open_workbook(filepath).sheets()[0]
    lines = table.nrows
    for x in range(lines):
        row = table.row_values(x)
        meta = row[0].lower()
        q_type = meta[0]
        p2 = meta[1:].split(';')
        add_sum = int(p2[0])
        sum = int(p2[1])
        choices = [str(row[2+y+add_sum]) for y in range(sum)]
        correct_answer = list({int(s) - 1 for s in p2[2].split(",")}) if q_type in "mc" else choices
        data = {
            'type': q_type,
            'stem': row[1],
            'correct_answer': correct_answer,
            'additions': [str(row[2+x]) for x in range(add_sum)]
        }
        if q_type in "mc":
            data['choices'] = choices
        results.append(data)
    return results


def create_book(data, book, ad_dict):
    for datum in data:
        if datum['type'] in 'mc':
            multiple = (datum['type'] == 'm')
            question = ChoiceQuestion.objects.create(stem=datum['stem'], book=book, multiple=multiple)
            for addition in datum['additions']:
                Image.objects.create(question=question, filename=addition, image=ad_dict[addition])
            for index, content in enumerate(datum['choices']):
                correct = index in datum['correct_answer']
                Choice.objects.create(question=question, content=content, correct=correct)
        else:
            question = Completion.objects.create(stem=datum['stem'], book=book)
            for ans in datum['correct_answer']:
                Answer.objects.create(question=question, content=ans)


def format_filename_with_time(filename):
    formatted_time = time.strftime(' %m-%d,%H-%M-%S')
    filename_divided = filename.split('.')
    filename_without_extension = '.'.join(filename_divided[:-1])
    filename_divided[-2] += formatted_time
    return filename_without_extension, os.path.join(MEDIA_ROOT, '.'.join(filename_divided))
