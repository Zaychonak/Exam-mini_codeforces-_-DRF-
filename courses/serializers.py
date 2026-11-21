from rest_framework import serializers
from .models import Course, Module, Task, TestCase, Submission


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    is_solved_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_is_solved_by_me(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return Submission.objects.filter(user=request.user,task=obj,status='accepted').exists()
        return False


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        source='task'
    )
    class Meta:
        model = Submission
        fields = ['id', 'task_id', 'user', 'code', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']