from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class TestCase(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return f"TestCase for {self.task.title}"


class Submission(models.Model):

    class Status(models.TextChoices):
        ACCEPTED = 'accepted', 'Accepted'
        WRONG_ANSWER = 'wrong_answer', 'Wrong Answer'
        ERROR = 'error', 'Error'
        TIME_LIMIT = 'time_limit', 'Time Limit'
        

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='submissions')
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='submissions')
    code = models.TextField()
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ERROR)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.task}"



    #for commit

