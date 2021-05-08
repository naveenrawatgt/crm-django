import random
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth import get_user, get_user_model

from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "agents/agent-list.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "agents/agent-create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0, 9999999)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
            )
        send_mail(
            subject=f"You are invited to be an agent as {user.username}",
            message=f'''You were added as an agent on CRM DJ: \n
            Username : {user.username} \n
            Email: {user.email} \n
            Initial Password: {user.password}\n
            Regards,
            SysAdmin
            ''',
            from_email=f"{self.request.user.email}",
            recipient_list= [f'{user.email}']
        )
        # agent.organisation = self.request.user.userprofile
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = "agents/agent-detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

class AgentUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "agents/agent-update.html"
    User = get_user_model()
    queryset = User.objects.filter()
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

    def get_success_url(self):
        return reverse("agents:agent-list")

class AgentDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "agents/agent-delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation = organisation)

    def get_success_url(self):
        return reverse("agents:agent-list")

