from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from academics.models import Group

from .forms import StudentCreateForm, StudentUpdateForm
from .models import Student


def word_variants(word):
    return {word, word.lower(), word.upper(), word.capitalize(), word.title()}


class StudentListView(ListView):
    model = Student
    template_name = 'users/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = Student.objects.select_related('group').filter(is_superuser=False)
        query = self.request.GET.get('q', '').strip()
        group = self.request.GET.get('group', '').strip()
        for word in query.split():
            condition = Q()
            for variant in word_variants(word):
                condition |= Q(last_name__contains=variant)
                condition |= Q(first_name__contains=variant)
                condition |= Q(middle_name__contains=variant)
            queryset = queryset.filter(condition)
        if group.isdigit():
            queryset = queryset.filter(group_id=group)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        context['groups'] = Group.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_group'] = self.request.GET.get('group', '')
        context['querystring'] = params.urlencode()
        return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'users/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.select_related('group__direction__faculty')


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = 'users/student_form.html'

    def get_success_url(self):
        return reverse('students:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новый студент'
        return context


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'users/student_form.html'

    def get_success_url(self):
        return reverse('students:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование студента'
        return context


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'users/student_confirm_delete.html'
    context_object_name = 'student'
    success_url = reverse_lazy('students:list')
