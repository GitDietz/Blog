from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        # possible to use
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count ==1:
        #     user = user_qs.first()
        if not user:
            raise ValidationError("This user does not exist")
        if not user.check_password(password):
            raise ValidationError("The password is incorrect")
        if not user.is_active:
            raise ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args,**kwargs)