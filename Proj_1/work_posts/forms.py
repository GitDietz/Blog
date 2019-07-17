from django import forms
from .models import Post, Robot
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish',
        ]


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = [
            'name',
            'number',
            'job',
        ]
