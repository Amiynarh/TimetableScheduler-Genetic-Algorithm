from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'UserName',
            'id': 'id_username'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password',
            'id': 'id_password',
        }))

class UserSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Username',
            'id': 'id_username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'Email',
            'id': 'id_email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Password',
            'id': 'id_password1',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Confirm Password',
            'id': 'id_password2',
        })

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Username uniqueness check
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")

        # Email uniqueness check
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")

        # Password match check
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'seating_capacity']



# class InstructorForm(forms.ModelForm):
#     preferred_time_slots = forms.MultipleChoiceField(
#         choices=TIME_SLOTS,
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
#     )
#     preferred_days = forms.MultipleChoiceField(
#         choices=DAYS_OF_WEEK,
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
#     )

#     class Meta:
#         model = Instructor
#         fields = ['name', 'preferred_time_slots', 'preferred_days']
#         help_texts = {
#             'preferred_time_slots': 'Select one or more preferred time slots.',
#             'preferred_days': 'Select one or more preferred days.'
#         }
class InstructorForm(forms.ModelForm):
    preferred_time_slots = forms.MultipleChoiceField(choices=TIME_SLOTS, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    preferred_days = forms.MultipleChoiceField(choices=DAYS_OF_WEEK, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Instructor
        fields = ['name', 'preferred_time_slots', 'preferred_days']
        help_texts = {
            'preferred_time_slots': 'Hold down "Control", or "Command" on a Mac, to select more than one.',
            'preferred_days': 'Hold down "Control", or "Command" on a Mac, to select more than one.'
        }
class CourseForm(forms.ModelForm):

    instructors = forms.ModelMultipleChoiceField(
        queryset=Instructor.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False
    )
    
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'}),
        required=False
    )

    
    level = forms.ChoiceField(
        choices=Course.LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )


    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'max_numb_students', 'instructors', 'departments', 'level']  # Changed 'department' to 'departments'
        widgets = {
            'course_number': forms.TextInput(attrs={'placeholder': 'e.g. CSC2301'}),
            'course_name': forms.TextInput(attrs={'placeholder': 'e.g. DBMS'})
        }


    