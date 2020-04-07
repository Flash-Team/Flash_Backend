from django.urls import path

from flash.organization.views import OrganizationsView, OrganizationView, FilialsView, FilialView

urlpatterns = [
    path('', OrganizationsView.as_view()),
    path('<int:pk>/', OrganizationView.as_view()),
    path('<int:pk>/filial/', FilialsView.as_view),
    path('<int:pk2>/filial/<int:pk>/', FilialView.as_view()),
]
