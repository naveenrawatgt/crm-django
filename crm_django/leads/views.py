from typing import ContextManager
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .models import Category, Lead
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.core.paginator import Paginator
from django.views.generic import (
    TemplateView, 
    CreateView, 
    DeleteView,
    UpdateView, 
    ListView, 
    DetailView
)

from agents.mixins import OrganisorAndLoginRequiredMixin
from .forms import (
    CustomAgentCreationForm, 
    LeadForm, 
    LeadModelForm, 
    UserClassForm, 
    CustomPasswordResetForm, 
    CustomSetPasswordForm, 
    AssignAgentForm
)

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
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False
                )
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Filter for agent logged in.
            queryset = Lead.objects.filter(agent__user = user)
        elif self.request.user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
                )
            
        return queryset


class UnassignedLeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/unassigned-leads-list.html"
    context_object_name = "leads"

    def get_queryset(self):
        if self.request.user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=self.request.user.userprofile, 
                agent__isnull=True
                )

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
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
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

class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "leads/assign-agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update(
            {
            "request": self.request
            }
        )
        return kwargs

    def form_valid(self, form):
        agent=form.cleaned_data["agent"]
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead-list")

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category-list.html"
    context_object_name = "categories"

    def get_queryset(self):
        user = self.request.user
        # Initial queryset of leads for the entire organisation.
        if user.is_agent:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        elif user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        # Initial queryset of leads for the entire organisation.
        if user.is_agent:
            counts = Lead.objects.filter(organisation=user.agent.organisation, category__isnull=True).count()
        elif user.is_organisor:
            counts = Lead.objects.filter(organisation=user.userprofile,  category__isnull=True).count()
        context.update(
            {
                "unassigned_leads_count": counts
            }
        )

        return context

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category-details.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        qs = self.get_object().leads.all()
        qs = qs.filter(organisation=self.request.user.userprofile)
        context.update(
            {
                "leads": qs
            }
        )

        return context

    def get_queryset(self, **kwargs):
        user = self.request.user
        # Initial queryset of leads for the entire organisation.
        queryset = Category.objects.filter(pk = self.kwargs['pk'])
        return queryset
