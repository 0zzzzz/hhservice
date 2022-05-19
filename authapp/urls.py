from django.urls import path
from authapp import views as authapp

app_name = 'authapp'


urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('skills_add/', authapp.skills_add, name='skills_add'),
    # path('skills_add/', authapp.SkillsAddView.as_view(), name='skills_add'),
    # path('user_skills_add/', authapp.UserSkillsAdd.as_view(), name='user_skills_add'),
    # path('skills_skills_add/', authapp.SkillsAdd.as_view(), name='skills_skills_add'),
    path('skills/create/', authapp.SkillCreateView.as_view(), name='skill_create'),
    path('skills/', authapp.SkillsListView.as_view(), name='skills_list'),
    path('skills/update/<int:pk>/', authapp.SkillUpdateView.as_view(),
         name='skill_update'),
    path('skills/delete/<int:pk>/', authapp.SkillDeleteView.as_view(),
         name='skill_delete'),
    path('account/', authapp.personal_account, name='account'),
    path('api/reg/', authapp.RegistrationAPIView.as_view(), name='APIreg'),
    path('api/log/', authapp.LoginAPIView.as_view(), name='APIlog'),
]

