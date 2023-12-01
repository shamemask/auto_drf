import os

def generate_drf_project(project_name, apps):
    # Создание Django проекта
    os.makedirs(project_name)
    os.chdir(project_name)
    os.system(f'django-admin startproject {project_name} .')

    # Добавление DRF в INSTALLED_APPS
    with open(os.path.join(project_name, project_name, "settings.py"), "r+") as settings_file:
        settings_content = settings_file.read()
        settings_content = settings_content.replace(
            "'django.contrib.staticfiles',",
            "'django.contrib.staticfiles',\n    'rest_framework',"
        )
        settings_file.seek(0)
        settings_file.write(settings_content)
        settings_file.truncate()

    # Создание и добавление API приложений и моделей
    for app in apps:
        app_name = app["name"]
        models = app["models"]

        # Создание API приложения
        os.system(f'python manage.py startapp {app_name}')
        
        # Генерация кода для models.py
        models_code = f"""
from django.db import models

class {app_name.capitalize()}Model(models.Model):
    name = models.CharField(max_length=100)
"""
        with open(os.path.join(app_name, "models.py"), "w") as file:
            file.write(models_code)
        
        # Добавление API приложения в INSTALLED_APPS
        with open(os.path.join(project_name, project_name, "settings.py"), "r+") as settings_file:
            settings_content = settings_file.read()
            settings_content = settings_content.replace(
                "'django.contrib.staticfiles',\n    'rest_framework',",
                f"'django.contrib.staticfiles',\n    'rest_framework',\n    '{app_name}',"
            )
            settings_file.seek(0)
            settings_file.write(settings_content)
            settings_file.truncate()

        # Генерация кода для views.py
        views_code = f"""
from rest_framework import viewsets
from .models import {app_name.capitalize()}Model
from .serializers import {app_name.capitalize()}Serializer

class {app_name.capitalize()}ViewSet(viewsets.ModelViewSet):
    queryset = {app_name.capitalize()}Model.objects.all()
    serializer_class = {app_name.capitalize()}Serializer
"""
        with open(os.path.join(app_name, "views.py"), "w") as file:
            file.write(views_code)

        # Генерация кода для serializers.py
        serializers_code = f"""
from rest_framework import serializers
from .models import {app_name.capitalize()}Model

class {app_name.capitalize()}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {app_name.capitalize()}Model
        fields = '__all__'
"""
        with open(os.path.join(app_name, "serializers.py"), "w") as file:
            file.write(serializers_code)

project_name = "myproject"
apps = [
    {
        "name": "app1",
        "models": [
            {
                "name": "Model1",
                "fields": [
                    {"name": "name", "type": "CharField", "max_length": 100},
                    {"name": "age", "type": "IntegerField"}
                ]
            }
        ]
    },
    {
        "name": "app2",
        "models": [
            {
                "name": "Model2",
                "fields": [
                    {"name": "title", "type": "CharField", "max_length": 100},
                    {"name": "content", "type": "TextField"}
                ]
            }
        ]
    }
]
generate_drf_project(project_name, apps)
