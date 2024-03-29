from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from users.models import User

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class EmployeeRegistrationForm(UserCreationForm):
    # gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENDER_CHOICES)

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['username'].label = "Username"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        # self.fields['gender'].widget = forms.CheckboxInput()

        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Username',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender']
        error_messages = {
            'username': {
                'required': 'Username is required',
                'max_length': 'Name is too long'
            },
            'email': {
                'required': 'Email is required',
                
            },
            'gender': {
                'required': 'Gender is required'
            }
        }

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "candidate"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Company Name"
        self.fields['last_name'].label = "Company Location"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"

        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Company Location',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Enter Email',
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Enter Password',
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirm Password',
            }
        )

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Company Name is required',
                'max_length': 'Company Name is too long'
            },
            'last_name': {
                'required': 'Company Location is required',
                'max_length': 'Company Location is too long'
            }
        }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = "recruiter"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user