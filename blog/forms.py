from django.forms import ModelForm, TextInput, Textarea
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Your name here'}),
            'text': Textarea(attrs=
                {'placeholder': 'Your comment here'}
            ),
        }

