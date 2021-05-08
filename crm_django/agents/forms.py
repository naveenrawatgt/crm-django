from django.forms import ModelForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from leads.models import Agent

class AgentModelForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )

        widgets = {
            'email': forms.EmailInput(
                attrs = {
                    'placeholder': 'Email',
                    'class': "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                }
            ),
            'username': forms.TextInput(
                attrs = {
                    'placeholder': 'User Name',
                    'class': "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                }
            ),
            'first_name': forms.TextInput(
                attrs = {
                    'placeholder': 'First Name',
                    'class': "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'placeholder': 'Last Name',
                    'class': "w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                }
            )
        }
