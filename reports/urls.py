from django.urls import path
from .views import ReportRecipientListView, ReportRecipientCreateView, ReportDetailView, UserReportListView, ReportDeleteView, ReportUpdateView


urlpatterns = [
    path('', ReportRecipientListView.as_view(), name='reports-home'),
    path('new/', ReportRecipientCreateView.as_view(), name='report-create'),
    path('report<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('user/<str:username>', UserReportListView.as_view(), name='user-reports'),
    path('report<int:pk>/update/', ReportUpdateView.as_view(), name='report-update'),
    path('report<int:pk>/delete/', ReportDeleteView.as_view(), name='report-delete'),

]