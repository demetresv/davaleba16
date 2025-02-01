from rest_framework import serializers
from .models import Task
from django.utils import timezone



class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

    def validate (self, value):
        if any(char in "!@#$^%&" for char in value):
            raise serializers.ValidationError("ტექსტი არ შეიძლება შეიცავდეს სიმბოლოებს")
        return value

    # შექმნის მეთოდი პითონის დონეზე, ბაზაში შენახვის გარეშე
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.create_date = timezone.now()
        return instance

    # განახლების მეთოდი პითონის დონეზე, ბაზაში შენახვის გარეშე
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.write_date = timezone.now()
        return instance

    # to_representation მეთოდით სერიალიზაციის გადაკეთება შეგვიძლია
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['custom_message'] = f"წიგნის ID არის {instance.id}"
        return representation

    # to_internal_value მეთოდით დესერიალიზაციის გადაკეთება შეგვიძლია
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'title' in data: internal_value['title'] = data['title'].strip().capitalize()
        return internal_value