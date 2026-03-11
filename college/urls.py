"""
URL configuration for COLLAGE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from STUDENT.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('stu_regi/',stu_regi,name='stu_regi'),
    path('stu_login/',stu_login,name='stu_login'),
    path('stu_dash/',stu_dash,name='stu_dash'),
    path('fac_regi/',fac_regi,name='fac_regi'),
    path('fac_login/',fac_login,name='fac_login'),
    path('fac_dash/',fac_dash,name='fac_dash'),
    path('admin_login/',admin_login,name='admin_login'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),
    path('admin_logout/',admin_logout,name='admin_logout'),
    path('logout/',logout,name='logout'),
    path('view_faculty/',view_faculty,name='view_faculty'),
    path('view_students/',view_students,name='view_students'),
    path('view_students_fac/',view_students_fac,name='view_students_fac'),
    path('post_attendance/',post_attendance,name='post_attendance'),
    path('post_result/',post_result,name='post_result'),
    path('view_attandence/',view_attendance,name='view_attandence'),
    path('view_result/',view_result,name='view_result'),
    path('download-result/<int:student_id>/',download_result_pdf, name='download_result'),
    path('view_results_fac/',view_results_fac,name='view_results_fac')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)