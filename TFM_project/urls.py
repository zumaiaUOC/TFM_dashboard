"""TFM_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from TFM_app import views, dash_app_code
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    re_path('exploratory_data_analysis/', TemplateView.as_view(
        template_name='exploratory_data_analysis.html'), name="dash_exploratory_data_analysis"),
    re_path('visualizacion/', TemplateView.as_view(
        template_name='visualizacion.html'), name="dash_visualizacion"),
    re_path('datos/', TemplateView.as_view(
        template_name='datos.html'), name="dash_datos"),
    re_path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('import_data_file/', views.import_data_file,
         name="import_data_file"),
    path('predict/', views.predict_chances, name='submit_prediction'),
    path('results/', views.view_results, name='results'),
 
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
