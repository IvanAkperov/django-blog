from django import forms
from .models import Comment


class EmailSender(forms.Form):
    name = forms.CharField(max_length=50)
    email_field = forms.EmailField()
    email_field_to = forms.EmailField()
    body = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']