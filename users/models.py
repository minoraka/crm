from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    GENDER_CHOICES = [
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    ]
    COURSE_CHOICES = [(number, f'{number} курс') for number in range(1, 5)]
    EDUCATION_FORM_CHOICES = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('вечерняя', 'Вечерняя'),
    ]
    FUNDING_CHOICES = [
        ('бюджет', 'Бюджет'),
        ('контракт', 'Контракт'),
    ]
    STATUS_CHOICES = [
        ('обучается', 'Обучается'),
        ('академический отпуск', 'Академический отпуск'),
        ('отчислен', 'Отчислен'),
        ('выпускник', 'Выпускник'),
    ]

    middle_name = models.CharField('отчество', max_length=100, blank=True)
    birth_date = models.DateField('дата рождения', null=True, blank=True)
    gender = models.CharField('пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField('телефон', max_length=20, blank=True)
    address = models.TextField('адрес', blank=True)
    photo = models.ImageField('фото', upload_to='students/', blank=True, null=True)
    student_id = models.CharField(
        'номер студенческого билета',
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        'academics.Group',
        on_delete=models.PROTECT,
        related_name='students',
        verbose_name='учебная группа',
        null=True,
        blank=True,
    )
    course = models.PositiveSmallIntegerField('курс', choices=COURSE_CHOICES, default=1)
    admission_year = models.PositiveSmallIntegerField('год поступления', null=True, blank=True)
    education_form = models.CharField(
        'форма обучения',
        max_length=20,
        choices=EDUCATION_FORM_CHOICES,
        default='очная',
    )
    funding = models.CharField(
        'основа обучения',
        max_length=20,
        choices=FUNDING_CHOICES,
        default='бюджет',
    )
    status = models.CharField(
        'статус',
        max_length=30,
        choices=STATUS_CHOICES,
        default='обучается',
    )
    created_at = models.DateTimeField('создан', auto_now_add=True)
    updated_at = models.DateTimeField('обновлён', auto_now=True)

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        name = ' '.join(part for part in (self.last_name, self.first_name, self.middle_name) if part)
        return name or self.username

    def __str__(self):
        if self.group:
            return f'{self.full_name} ({self.group})'
        return self.full_name
