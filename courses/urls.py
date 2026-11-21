from django.urls import path
from .views import (CourseListCreateView, CourseDetailView, ModuleDetailView, ModuleListCreateView, TaskListCreateView, TaskDetailView,
                    TestCaseListCreateView, TestCaseDetailView, SubmissionListCreateView, StaticCourseView, StaticAcceptedTestsView,
                    StaticTopUsersView, StaticPopularCoursesView, StaticHardTasksView, StaticPlatformView)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view()),
    path('courses_detail/<int:pk>/', CourseDetailView.as_view()),
    path('modules/', ModuleListCreateView.as_view()),
    path('models_detail/<int:pk>/', ModuleDetailView.as_view()),
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks_detail/<int:pk>/', TaskDetailView.as_view()),
    path('testcases/', TestCaseListCreateView.as_view()),
    path('testcases_detail/<int:pk>/', TestCaseDetailView.as_view()),
    path('submissions/', SubmissionListCreateView.as_view()),
    path('static_course/', StaticCourseView.as_view()),
    path('static_accepted/', StaticAcceptedTestsView.as_view()),
    path('static_top_users/', StaticTopUsersView.as_view()),
    path('static_popular_courses/', StaticPopularCoursesView.as_view()),
    path('static_hard_tasks/', StaticHardTasksView.as_view()),
    path('static_platform/', StaticPlatformView.as_view()),
]