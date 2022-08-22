from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Folder)
admin.site.register(Book)
admin.site.register(Answer)
admin.site.register(ChoiceQuestion)
admin.site.register(Choice)
admin.site.register(Completion)
admin.site.register(AnswerSheet)
admin.site.register(UserChoiceQuestionAnswer)
admin.site.register(UserCompletionQAnswer)
admin.site.register(UserChoiceAnswer)
admin.site.register(Log)
admin.site.register(Image)
