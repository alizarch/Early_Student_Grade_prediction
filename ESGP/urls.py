from django.contrib import admin
from django.urls import path
from esgpapp import views
from django.conf import settings
from django.conf.urls.static import static
from esgpapp import Helper

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingpage , name = 'landingpage'),
    path('signup', views.signup, name = 'signup'),
    path('signuppost', views.signuppost, name = 'signuppost'),
    path('login', views.user_login, name = 'login'),
    path('loginpost', views.loginpost, name = 'loginpost'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('logout', views.user_logout, name='logout'),
    path('calculate/grade/prediction', views.CalculatePrediction, name='cal_pre'),
    path('upload/csv/file', views.upload_csv_file_faculty, name='upload_csv_file'),
    path('upload/student/data', views.upload_data_student, name='upload_student_data'),
    path('upload/student/data/result', views.upload_data_student_result, name='upload_student_data_result'),
    path('export', Helper.exportCSV_Content, name='export'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
