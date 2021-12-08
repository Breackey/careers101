from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('account/', views.account, name='account'),
    path('contact-us/', views.contactView, name='contact'),
    path('success/', views.successView, name='success'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('privacy-policy/', views.privacy, name='privacy-policy'),
    path('terms-of-service/', views.terms, name='terms-of-service'),
    path('hiring/pricing/', views.pricing, name='pricing'),
    path('accounts/', include('allauth.urls')),
    path('', include('candidates.urls')),
    path('hiring/', include('recruiters.urls')),
    path('', include('pwa.urls')),
    path('blog/', include('blog.urls'), name='blog'),
    path('newsletter/', include('newsletter.urls')),
    path('control-panel/', include('control_panel.urls')),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)