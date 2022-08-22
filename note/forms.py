from django import forms
from .models import *


class ExcelUploadForm(forms.Form):
    name = forms.CharField(max_length=40)
    file = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = forms.CharField(max_length=100)
    public = forms.BooleanField(required=False)


class BookNameEditorForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name']
        labels = {'name': ''}
        widgets = {
            'name': forms.TextInput(attrs={
                'style': 'height: 32px; width: 40%; font-size: 20px',
                'id': 'book_name_input'
            })
        }


class BookDescriptionEditingForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['description']
        labels = {'description': ''}
        widgets = {
            'description': forms.Textarea(attrs={
                'style': 'height: 30px; width: 80%; font-size: 16px',
                'id': 'description_input'
            })
        }


class SortingOutForm(forms.ModelForm):
    completion = forms.BooleanField(required=False)
    choosing = forms.BooleanField(required=False)
    right_questions = forms.BooleanField(required=False)
    wrong_questions = forms.BooleanField(required=False)

    class Meta:
        model = Book
        fields = ['folder', 'name', 'description', 'public']


class FolderCreationForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
        labels = {'name': ''}
        widgets = {'name': forms.TextInput(attrs={
            'id': 'new_folder_name',
            'style': 'height: 32px; width: 80%; font-size: 20px;',
        })}
