from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import Ticket
from django.contrib.auth.models import Group, User
from django import template




def home(request):
    context = {
        'tickets': Ticket.objects.all()
    }
    return render(request, 'tickets/home.html', context)

class TicketListView(ListView):
    model = Ticket
    template_name = 'tickets/home.html'
    context_object_name = 'tickets'
    ordering = ['date_created']
    paginate_by = 5

    def get_queryset(self):
        status = 'Open'
        return Ticket.objects.filter(status=status).order_by('date_created')

class UserTicketListView(ListView):
    model = Ticket
    template_name = 'tickets/user_tickets.html'
    context_object_name = 'tickets'
    ordering = ['date_created']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ticket.objects.filter(author=user).order_by('-date_created')

class TicketDetailView(DetailView):
    model = Ticket

   

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['title', 'content', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.author or self.request.user.groups.filter(name='Managers').exists() or self.request.user.groups.filter(name='Help Desk').exists():
            return True
        return False

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.author or self.request.user.groups.filter(name='Managers').exists() or self.request.user.groups.filter(name='Help Desk').exists():
            return True
        return False
    

def create_ticket(request):
    return render(request, 'tickets/create.html')