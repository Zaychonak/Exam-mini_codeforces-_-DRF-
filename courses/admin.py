from django.contrib import admin
from .models import Course, Module, TestCase, Task

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(TestCase)