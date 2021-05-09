from collections import namedtuple
from .views import CategoryDetailView, LeadCreateView, LeadDeleteView, LeadDetailView, LeadUpdateView, LeadListView, UnassignedLeadListView, AssignAgentView, CategoryListView
from django.urls import path

app_name = "leads"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('unassigned-leads', UnassignedLeadListView.as_view(), name='unassigned-leads'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('<int:pk>/assigned-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/category-details', CategoryDetailView.as_view(), name='category-details')
]