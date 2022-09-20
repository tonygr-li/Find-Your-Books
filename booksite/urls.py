"""booksite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users import views as users_views
from utilisateurs import views as utilisateurs_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # English

    path('en/', include('selling.urls')),

    path('en/sign-up/', users_views.register, name='register'),
    path('en/profile/', users_views.profile, name="profile"),
    path('en/update-profile/', users_views.update_profile, name='update-profile'),
    path('en/login/', users_views.login_user, name='login'),
    path('en/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('en/activate-user/<uidb64>/<token>/', users_views.activate_user, name='activate'),
    path('en/resend-activation-email', users_views.resend_activate_email, name='resend-activation-email'),

    path('en/reset-password/', auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'), name='reset_password'),
    path('en/reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/reset_sent.html'), name='password_reset_done'),
    path('en/reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('en/reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'), name='password_reset_complete'),

    path('en/report-user/<int:pk>/', users_views.report_user, name='report'),

    path('en/staff/', users_views.admin_page, name='staff'),
    path('en/delete-outdated-posts/', users_views.delete_outdated_posts, name='outdated-posts'),
    path('en/report-leaders/', users_views.report_leaders, name='report-leaders'),
    path('en/report-info/<int:pk>/', users_views.report_info, name='report-info'),
    path('en/dismiss-report/<int:pk>/', users_views.dismiss_report, name='dismiss-report'),
    path('en/unauthorized/', users_views.unauthorized, name='staff-only'),

    path('en/guide/', users_views.guide, name='guide'),
    path('en/terms-of-use/', users_views.terms, name='terms-of-use'),
    path('en/about/', users_views.about, name='about'),

    # Français
    path('', include('vendre.urls')),

    path('inscription/', utilisateurs_views.register, name='register-fr'),
    path('profil/', utilisateurs_views.profile, name="profile-fr"),
    path('revision-profil/', utilisateurs_views.update_profile, name='update-profile-fr'),
    path('connexion/', utilisateurs_views.login_user, name='login-fr'),
    path('deconnexion/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout-fr'),
    path('activation-utilisateur/<uidb64>/<token>/', utilisateurs_views.activate_user, name='activate-fr'),
    path('reenvoyer-courriel-activation/', utilisateurs_views.resend_activate_email, name='resend-activation-email-fr'),

    path('reinitialisation-motdepasse/', auth_views.PasswordResetView.as_view(template_name='utilisateurs/reset_password.html'), name='reset_password-fr'),
    path('reinitialisation-motdepasse-envoye/', auth_views.PasswordResetDoneView.as_view(template_name='utilisateurs/reset_sent.html'), name='password_reset_done-fr'),
    path('reinitialisation-confirme/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='utilisateurs/password_reset_confirm.html'), name='password_reset_confirm-fr'),
    path('reinitialisation-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='utilisateurs/reset_password_complete.html'), name='password_reset_complete-fr'),

    path('denoncer-utilisateur/<int:pk>/', utilisateurs_views.report_user, name='report-fr'),

    path('staff/', utilisateurs_views.admin_page, name='staff-fr'),
    path('effacer-publications-dépassés/', utilisateurs_views.delete_outdated_posts, name='outdated-posts-fr'),
    path('denonces-leaders/', utilisateurs_views.report_leaders, name='report-leaders-fr'),
    path('info-denonces/<int:pk>/', utilisateurs_views.report_info, name='report-info-fr'),
    path('effacer-denonciation/<int:pk>/', utilisateurs_views.dismiss_report, name='dismiss-report-fr'),
    path('non-autorise/', utilisateurs_views.unauthorized, name='staff-only-fr'),

    path('guide/', utilisateurs_views.guide, name='guide-fr'),
    path('conditions-dutilisation/', utilisateurs_views.terms, name='terms-of-use-fr'),
    path('apprendre-plus/', utilisateurs_views.about, name='about-fr'),
]
urlpatterns += staticfiles_urlpatterns()

handler404 = 'users.views.handler404'
handler403 = 'users.views.handler403'
handler400 = 'users.views.handler400'
handler500 = 'users.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
