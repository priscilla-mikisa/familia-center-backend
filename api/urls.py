from django.urls import path
from .views.user_views import UserListView, UserDetailView, CounselorListView
from .views.program_views import (
    ProgramListView, ProgramDetailView, 
    ProgramEnrollmentView, ResourceListView
)
from .views.session_views import (
    SessionListView, SessionDetailView, 
    BookingView, FeedbackView
)

urlpatterns = [
    # User endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('counselors/', CounselorListView.as_view(), name='counselor-list'),
    
    # Program endpoints
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<int:id>/', ProgramDetailView.as_view(), name='program-detail'),
    path('programs/<int:program_id>/enroll/', ProgramEnrollmentView.as_view(), name='program-enroll'),
    path('programs/<int:program_id>/resources/', ResourceListView.as_view(), name='program-resources'),
    
    # Session endpoints
    path('sessions/', SessionListView.as_view(), name='session-list'),
    path('sessions/<int:id>/', SessionDetailView.as_view(), name='session-detail'),
    path('sessions/<int:session_id>/book/', BookingView.as_view(), name='session-book'),
    path('sessions/<int:session_id>/feedback/', FeedbackView.as_view(), name='session-feedback'),
]