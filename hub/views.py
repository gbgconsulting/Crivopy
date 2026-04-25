from django.views.generic import ListView, CreateView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Job
from .forms import JobForm

# TAREFA 2.2.1: Adicione esta classe que estava faltando!
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'hub/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Métrica simples para o dashboard
        context['active_jobs_count'] = Job.objects.filter(user=user, status='ACTIVE').count()
        return context

class JobListView(LoginRequiredMixin, ListView):
    '''
    List all jobs created by the authenticated user.
    '''
    model = Job
    template_name = 'hub/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        # Task 3.3.2: Filter queryset to return only jobs owned by the user
        return Job.objects.filter(user=self.request.user)

class JobCreateView(LoginRequiredMixin, CreateView):
    '''
    Create a new job position for the authenticated user.
    '''
    model = Job
    form_class = JobForm
    template_name = 'hub/job_form.html'
    success_url = reverse_lazy('hub:job-list')

    def form_valid(self, form):
        # Task 3.3.4: Set the user instance before saving
        form.instance.user = self.request.user
        messages.success(self.request, 'Vaga criada com sucesso!')
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Update an existing job position owned by the authenticated user.
    '''
    model = Job
    form_class = JobForm
    template_name = 'hub/job_form.html'
    success_url = reverse_lazy('hub:job-list')

    def get_queryset(self):
        # Task 3.3.6: Ensure the user only edits their own jobs
        return Job.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Vaga atualizada com sucesso!')
        return super().form_valid(form)

class JobArchiveView(LoginRequiredMixin, View):
    '''
    Custom view to archive a job via POST request.
    '''
    def post(self, request, pk):
        # Task 3.3.7: Securely retrieve the job and change status
        job = get_object_or_404(Job, pk=pk, user=request.user)
        job.status = Job.ARCHIVED
        job.save()
        
        messages.success(request, f'A vaga "{job.title}" foi arquivada.')
        return redirect('hub:job-list')