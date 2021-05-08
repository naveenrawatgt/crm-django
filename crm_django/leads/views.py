from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from django.views.generic import (TemplateView, CreateView, DeleteView,
                         UpdateView, ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView

from .forms import CustomAgentCreationForm, LeadForm, LeadModelForm, UserClassForm
from agents.mixins import OrganisorAndLoginRequiredMixin
from leads.forms import CustomPasswordResetForm, CustomSetPasswordForm

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomAgentCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingTemplateView(TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/lead-list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation.
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Filter for agent logged in.
            queryset = Lead.objects.filter(agent__user = user)
        elif self.request.user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)

        return queryset

class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = "leads/lead-details.html"  
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation.
        if self.request.user.is_agent:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Filter for agent logged in.
            queryset = Lead.objects.filter(agent__user = user)
        elif self.request.user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        return queryset

class LeadCreateView(OrganisorAndLoginRequiredMixin,CreateView):
    template_name = "leads/lead-create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # TODO sent email
        send_mail(
            subject="A New Lead Has Been Created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin,UpdateView):
    template_name = "leads/lead-update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-list")

class LeadDeleteView(OrganisorAndLoginRequiredMixin,DeleteView):
    template_name = "leads/lead-delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.filter(organisation=user.userprofile)
        return queryset

class LoginCustomView(LoginView):
    
    form_class = UserClassForm

class PasswordResetCustomView(PasswordResetView):

    form_class = CustomPasswordResetForm

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm