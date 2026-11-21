from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Course, Module, Task, TestCase, Submission
from .serializers import CourseSerializer, ModuleSerializer, TaskSerializer, TestCaseSerializer, SubmissionSerializer
from accounts.permissions import IsAdmin, IsStudent
from rest_framework.permissions import IsAuthenticated
from django.db import models
from accounts.models import User
import subprocess
import sys
import json
import uuid
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Avg, Max, Min


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [AllowAny()]


class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.select_related('course').all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]


class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.select_related('course').all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [AllowAny()]


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.select_related('module').all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.select_related('module').all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [AllowAny()]



class TestCaseListCreateView(generics.ListCreateAPIView):
    serializer_class = TestCaseSerializer
    def get_queryset(self):
        queryset = TestCase.objects.select_related('task').all().order_by('id')

        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return queryset
        return queryset[:1]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]


class TestCaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [IsAdmin]



class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Submission.objects.select_related('user', 'task').all()
        return Submission.objects.filter(
            user=self.request.user
        ).select_related('user', 'task')

    def perform_create(self, serializer):
        submission = serializer.save(user=self.request.user)
        status = self.check_code(submission.code,submission.task)
        submission.status = status
        submission.save(update_fields=['status'])

    def check_code(self, code, task):
        test_cases = task.test_cases.all()
        if not test_cases.exists():
            return 'error'

        for test_case in test_cases:
            command = [
            'podman', 'run', '--rm',
            '-i',
            '--network=none',
            '--memory=128m',
            '--cpus=0.5',
            '--pids-limit=64',
            '--read-only',
            '--user=65534:65534',
            '--cap-drop=all',
            '--security-opt=no-new-privileges',
            'python:3.12-slim',
            'python', '-c', code
        ]

            try:
                result = subprocess.run(
                    command,
                    input=test_case.input_data,
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                print('RETURN CODE:', result.returncode)
                print('STDOUT:', result.stdout)
                print('STDERR:', result.stderr)
                output = result.stdout.strip()
                expected = test_case.expected_output.strip()

                if result.returncode != 0:
                    print('ERROR:', result.stderr)
                    print('RETURN CODE:', result.returncode)
                    return 'error'
                if output != expected:
                    return 'wrong_answer'

            except subprocess.TimeoutExpired:
                return 'time_limit'

        return 'accepted'



class StaticCourseView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        courses = Course.objects.annotate(tasks_count=Count('modules__tasks')).values('id', 'title', 'tasks_count')
        return Response(courses)


class StaticUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.annotate(submissions_count=Count('submissions')).values('id','username','submissions_count')
        return Response(users)


class StaticAcceptedTestsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = User.objects.annotate(accepted_count=Count('submissions',filter=models.Q(submissions__status='accepted'))).values('id','username','accepted_count')
        return Response(users)


class StaticTopUsersView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        users = User.objects.annotate(accepted_count=Count('submissions',filter=models.Q(submissions__status='accepted'))).order_by('-accepted_count')[:10]
        result = users.values('id','username','accepted_count')
        return Response(result)


class StaticPopularCoursesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        courses = Course.objects.annotate(submissions_count=Count('modules__tasks__submissions')).order_by('-submissions_count')[:5]
        result = courses.values('id','title','submissions_count')
        return Response(result)


class StaticHardTasksView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        tasks = Task.objects.annotate(wrong_count=Count('submissions',filter=models.Q(submissions__status='wrong_answer'))).order_by('-wrong_count')[:5]
        result = tasks.values('id','title','wrong_count')
        return Response(result)


class StaticPlatformView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        stats = {
            'users_count': User.objects.count(),
            'courses_count': Course.objects.count(),
            'tasks_count': Task.objects.count(),
            'submissions_count': Submission.objects.count(),
            'accepted_count': Submission.objects.filter(status='accepted').count(),
            'average_submissions_per_task': Task.objects.annotate(submissions_count=Count('submissions')).aggregate(Avg('submissions_count'))['submissions_count__avg'],
            'total_submissions': Submission.objects.aggregate(total=Count('id'))['total']
        }
        return Response(stats)