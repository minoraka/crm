from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

try:
    from django.contrib.auth.forms import AdminUserCreationForm as BaseCreationForm
except ImportError:
    from django.contrib.auth.forms import UserCreationForm as BaseCreationForm

from .models import Student


class StudentCreationForm(BaseCreationForm):
    class Meta(BaseCreationForm.Meta):
        model = Student


class StudentChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    form = StudentChangeForm
    add_form = StudentCreationForm

    fieldsets = UserAdmin.fieldsets + (
        (
            'Личные данные',
            {'fields': ('middle_name', 'birth_date', 'gender', 'phone', 'address', 'photo')},
        ),
        (
            'Обучение',
            {
                'fields': (
                    'student_id',
                    'group',
                    'course',
                    'admission_year',
                    'education_form',
                    'funding',
                    'status',
                )
            },
        ),
        ('Служебное', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Данные студента',
            {
                'fields': (
                    'last_name',
                    'first_name',
                    'middle_name',
                    'student_id',
                    'group',
                    'course',
                    'admission_year',
                )
            },
        ),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('username', 'full_name', 'student_id', 'group', 'course', 'status')
    search_fields = ('username', 'last_name', 'first_name', 'middle_name', 'student_id')
    list_filter = ('group', 'course', 'status')
