from django import forms
from django.db.models import DateTimeField

from .models import ToDoList


class ToDoListForm(forms.ModelForm):
    end_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'end_date']

    def __init__(self, *args, **kwargs):
        super(ToDoListForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




