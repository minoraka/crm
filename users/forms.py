from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'username',
            'last_name',
            'first_name',
            'middle_name',
            'email',
            'birth_date',
            'gender',
            'phone',
            'address',
            'photo',
            'student_id',
            'group',
            'course',
            'admission_year',
            'education_form',
            'funding',
            'status',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['gender'].required = True
        self.fields['student_id'].required = True
        self.fields['group'].required = True
        self.fields['admission_year'].required = True


class StudentCreateForm(StudentForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    field_order = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data['password'])
        if commit:
            student.save()
        return student


class StudentUpdateForm(StudentForm):
    pass
