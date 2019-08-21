from django import forms
from django.contrib.auth.models import User
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

        # possible to use
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count ==1:
        #     user = user_qs.first()
        if username and password:
            known_user = User.objects.filter(username=username).exists
            user = authenticate(username=username, password=password)
            if not known_user:
                print('unknown user')
                raise ValidationError("This user does not exist")
            else:
                print('passw fault')
                raise ValidationError("The password is incorrect")
                # if not user.check_password(password):
            if user:
                print('knwon user')
                if not user.is_active:
                    raise ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args,**kwargs)