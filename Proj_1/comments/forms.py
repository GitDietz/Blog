from django import forms


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        print('content = ' + content)
        return content