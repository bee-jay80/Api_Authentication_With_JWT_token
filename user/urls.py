# from django.urls import path
# from . import views
# urlpatterns = [
#     path('register',views.RegisterView)
# ]
from django.urls import path
from.views import RegisterView, LoginView, UserView, OrganisationView, OrganisationDetailView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('api/users/:<userId>/', UserView.as_view()),
    path('api/organisations/', OrganisationView.as_view()),
    path('api/organisations/:<orgId>/', OrganisationDetailView.as_view()),
    path('api/organisations/:<orgId>/users/', AddUserToOrganisationView.as_view()),
]