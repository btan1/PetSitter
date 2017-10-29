from django import forms
from models import UserProfile
from django.contrib.auth import authenticate


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={
        "required": "You have to enter your Email",
        "invalid": "You have to enter valid Email"

    })
    first_name = forms.CharField(required=True, error_messages={
        "required": "You have to enter your first name",
    })
    last_name = forms.CharField(required=True, error_messages={
        "required": "You have to enter your last name",
    })
    password = forms.CharField(required=True,min_length=6,max_length=20,error_messages={
        "required": "You have to enter your password",
        "min_length": "The minimum length is 6",
        "max_length": "The maximum length is 10",
    })
    password_confirmation = forms.CharField(required=True,min_length=6,max_length=20,error_messages={
        "required": "You have to enter your password",
        "min_length": "The minimum length is 6",
        "max_length": "The maximum length is 10",
    })

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("two passwords doesn't match")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email = email):
            raise forms.ValidationError("email has been used")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={
        "required": "You have to enter your Email",
        "invalid": "You have to enter valid Email",
    })
    password = forms.CharField(required=True, min_length=6, max_length=16, error_messages={
        "required": "You have to enter your password",
        "min_length": "The minimum length is 6",
        "max_length": "The maximum length is 16",
    })

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("username or password is wrong!")


class profileForm(forms.Form):
    petname = forms.CharField(required=True,max_length=10,error_messages={
        "required": "You have to enter your petname",
        "max_length": "The maximum length is 10",
    })
    petage = forms.IntegerField(required=True, min_value=0, max_value=100,error_messages={
        "required": "You have to enter your petage",
        "min_value": "The minimum age is 0",
        "max_value": "The maximum age is 100",
    })
    petbio = forms.CharField(required=True, max_length=200, error_messages={
        "required": "You have to enter your pet bio",
        "max_length": "The maximum length is 200",
    })


class AvatorUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=['avator']


class FoodSetForm(forms.Form):
    amount = forms.DecimalField(required=True, max_digits=5, decimal_places=2, error_messages={
        "required": "You have to enter food amount",
        "max_digits": "max digits is 5",
        "decimal_places":"decimal places is 2"
    })
    time = forms.CharField(required=True,  error_messages={
        "required": "You have to enter time",

    })