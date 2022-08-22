from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.http.response import *
from .models import *
from .forms import *
from .func import *
import json
import time

# Create your views here.


def index(request):
    if request.method != 'POST':
        form = FolderCreationForm()
    else:
        form = FolderCreationForm(data=request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.creator = request.user
            new_folder.save()
            return HttpResponseRedirect(reverse('note:index'))
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))
    else:
        changelog = Log.objects.order_by('-date_updated')
        folders = Folder.objects.filter(creator=request.user).order_by('-date_added')
        library = Book.objects.filter(public=True).order_by('-date_added')
        context = {'folders': folders, 'library': library, 'form': form, 'changelog': changelog}
        return render(request, 'index.html', context=context)


@login_required
def upload(request, folder_id):
    if request.method != 'POST':
        form = ExcelUploadForm()
    else:
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            folder = Folder.objects.get(id=folder_id)
            form_data = form.cleaned_data
            files = request.FILES.getlist('file')
            valid_main_extension_names = ['xlsx']
            for i, file in enumerate(files[:]):
                if file.name.split('.')[-1] in valid_main_extension_names:
                    main_name, path = format_filename_with_time(file.name)
                    with open(path, mode='wb') as written_file:
                        written_file.write(file.file.getvalue())
                    del files[i]
                    break
            ori_data = {
                "main": path,
                "additions": {}
            }
            for one in files:
                main, path = format_filename_with_time(one.name)
                ori_data["additions"][main] = path
                with open(file=path, mode='wb') as file:
                    file.write(one.file.getvalue())
            print(ori_data["additions"])
            data = load(ori_data['main'])
            book = Book.objects.create(
                uploader=request.user, name=form_data['name'], folder=folder,
                description=form_data['description'], public=form_data['public']
            )
            create_book(data, book, ori_data['additions'])
            return HttpResponseRedirect(reverse('note:index'))
    return render(request, 'upload.html', {'form': form, 'folder_id': folder_id})


def get_question_page(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'question.html', context={'book': book})


def get_question(request, book_id):
    book = Book.objects.get(id=book_id)
    questions = []
    for question in book.choicequestion_set.all():
        print(question.image_set.all()[0].image.path)
        data = {
            'id': question.id,
            'type': 'c',
            'stem': question.stem,
            'multiple': question.multiple,
            'choices': [{'id': choice.id, 'content': choice.content} for choice in question.choice_set.all()],
            'images': [img.image.name[7:] for img in question.image_set.all()]
        }
        print(data)
        questions.append(data)
    for question in book.completion_set.all():
        data = {
            'id': question.id,
            'type': 'f',
            'stem': question.stem,
        }
        questions.append(data)
    return JsonResponse(json.dumps(questions, ensure_ascii=False), safe=False)


@csrf_exempt
def post_answer_sheet(request):
    if request.method == 'POST':
        ans_data = json.loads(request.body.decode('utf-8'))
        book = Book.objects.get(id=ans_data['book'])
        timer = ans_data['time']
        sheet = AnswerSheet.objects.create(book=book, respondent=request.user, used_time=timer)
        c = book.choicequestion_set
        f = book.completion_set
        total_correct = 0
        for q in ans_data['answers']:
            if q['type'] == 'c':
                question = c.get(id=q['question'])
                correct_answers = question.choice_set.filter(correct=True)
                answers = [question.choice_set.get(id=int(num)) for num in q['answer'] if num]
                correct = len(correct_answers) == len(answers)
                if correct:
                    for answer in answers:
                        correct *= answer.correct
                q_ans = UserChoiceQuestionAnswer.objects.create(
                    sheet=sheet, question=question, correct=correct
                )
                for answer in answers:
                    UserChoiceAnswer.objects.create(question=q_ans, choice=answer)
                total_correct += correct
            else:
                question = f.get(id=q['question'])
                valid_answers = [ans.content for ans in question.answer_set.all()]
                ans = str(q['answer'])
                correct = ans in valid_answers
                UserCompletionQAnswer.objects.create(
                    sheet=sheet, question=question,
                    answer=ans, correct=correct
                )
                total_correct += correct
        adding = total_correct / timer * 100
        request.user.userprofile.exp += adding
        request.user.userprofile.save()
    return HttpResponseRedirect(reverse('note:index'))


def operate(request, book_id):
    book = Book.objects.get(id=book_id)
    desc_editor = BookDescriptionEditingForm(instance=book)
    if request.method != 'POST':
        form = BookNameEditorForm(instance=book)
    else:
        form = BookNameEditorForm(data=request.POST, instance=book)
        if form.is_valid():
            form.save()
    answer_sheets = book.answersheet_set.filter(respondent=request.user).order_by('-date_added')
    context = {'book': book, 'sheets': answer_sheets, 'form': form, 'desc_editor': desc_editor}
    return render(request, 'operating.html', context=context)


def view_sheet(request, sheet_id):
    sheet = AnswerSheet.objects.get(id=sheet_id)
    book = sheet.book
    choice_questions = []
    completions = []
    for uca in sheet.userchoicequestionanswer_set.all():
        choice_questions.append(uca)
    for uca in sheet.usercompletionqanswer_set.all():
        completions.append(uca)
    context = {
        "sheet": sheet, "book": book, "choosing": choice_questions, "completions": completions
    }
    return render(request, 'view.html', context)


def sort_out(request, sheet_id):
    answer_sheet = AnswerSheet.objects.get(id=sheet_id)
    if request.method != 'POST':
        form = SortingOutForm(initial={'folder': '1'})
    else:
        form = SortingOutForm(data=request.POST)
        if form.is_valid():
            result = []
            data = form.cleaned_data
            if not data['name']:
                now_time = time.strftime('%y-%m-%d, %H: %M')
                data['name'] = 'Sorted book from %s at %s' % answer_sheet.book.name, now_time
            if data['choosing']:
                answer_set = answer_sheet.userchoosingquestionanswer_set.all()
                if answer_set:
                    for question in answer_set:
                        if (question.correct and data['right_questions']) or (
                                (not question.correct) and data['wrong_questions']):
                            cq = question.question
                            choices = []
                            correct_ans = None
                            for i, choice in enumerate(cq.choice_set.all()):
                                choices.append(choice.content.content)
                                if choice.content == cq.correct_answer:
                                    correct_ans = i + 2
                            datum = {
                                'type': 'c',
                                'stem': cq.stem,
                                'correct_answer': correct_ans,
                                'choices': choices
                            }
                            result.append(datum)
                    del cq, choices, correct_ans
            if data['completion']:
                answer_set = answer_sheet.usercompletionanswer_set.all()
                if answer_set:
                    for question in answer_set:
                        if (question.correct and data['right_questions']) or (
                                (not question.correct) and data['wrong_questions']):
                            fq = question.question
                            datum = {
                                'type': 'f',
                                'stem': fq.stem,
                                'correct_answer': fq.correct_answer
                            }
                            result.append(datum)
            book = Book.objects.create(name=data['name'], folder=data['folder'])
            create_book(result, book)
            return HttpResponseRedirect(reverse('note:op', args=(answer_sheet.book.id,)))
    return render(request, 'sorting.html', {'form': form, 'sheet': answer_sheet})


def edit_desc(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookDescriptionEditingForm(data=request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('note:op', args=(book_id, )))


@csrf_exempt
def refactor(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode().replace("'", "\""))
        target = Folder.objects.get(id=data['folder'])
        book = Book.objects.get(id=data['book'])
        book.folder = target
        book.save()
    return HttpResponseRedirect(reverse('note:index'))


def change_public_status(request, book_id):
    book = Book.objects.get(id=book_id)
    book.public = not book.public
    book.save()
    return HttpResponseRedirect(reverse('note:op', args=(book_id, )))
