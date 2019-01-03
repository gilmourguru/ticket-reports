from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import ReportRecipient
from django.contrib.auth.models import Group, User
from tickets.models import Ticket
# Create your views here.

def home(request):
    return render(request, 'reports/home.html')

class ReportRecipientListView(ListView):
    model = ReportRecipient
    template_name = 'reports/home.html'
    context_object_name = 'report_recips'
    ordering = ['date_created']
    paginate_by = 5

    def get_queryset(self):
        active = True
        return ReportRecipient.objects.filter(active=active).order_by('date_created')

class ReportRecipientCreateView(LoginRequiredMixin, CreateView):
    model = ReportRecipient
    fields = ['email']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ReportDetailView(DetailView):
    model = ReportRecipient

class UserReportListView(ListView):
    model = ReportRecipient
    template_name = 'reports/user_reports.html'
    context_object_name = 'reports'
    ordering = ['date_created']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        report = ReportRecipient.objects.filter(creator=user).order_by('-date_created')
        open_tickets = Ticket.objects.filter(status='Open').order_by('date_created')
        closed_tickets = Ticket.objects.filter(status='Closed').order_by('-date_created')
        return ReportRecipient.objects.filter(creator=user).order_by('-date_created')
        # return {'report':report, 'open_tickets': open_tickets, 'closed_tickets':closed_tickets}

class ReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReportRecipient
    fields = ['email', 'active']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


    def test_func(self):
        report = self.get_object()
        if self.request.user == report.creator or self.request.user.groups.filter(name='Managers').exists():
            return True
        return False

class ReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReportRecipient
    success_url = '/reports'

    def test_func(self):
        report = self.get_object()
        if self.request.user == report.creator or self.request.user.groups.filter(name='Managers').exists():
            return True
        return False