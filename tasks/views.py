from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.utils import timezone

# წიგნების ჩამონათვალი და ახალი წიგნის შექმნა
@api_view(['GET', 'POST'])
def Task_list_and_create(request):
    """
    მეთოდების მიხედვით:
    1. GET - ყველა წიგნის ჩამონათვალი.
    2. POST - ახალი წიგნის შექმნა.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            Task = serializer.save()  # წიგნის შექმნა
            return Response(
                {"message": "წიგნი წარმატებით შექმნილია!", "Task": TaskSerializer(Task).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# წიგნის განახლება, დეტალების ჩვენება და წაშლა
@api_view(['GET', 'PUT', 'DELETE'])
def task_update_and_detail(request, pk):
    """
    მეთოდების მიხედვით :
    1. GET - კონკრეტული წიგნის დეტალების ჩვენება.
    2. PUT - წიგნის განახლება.
    3. DELETE - წიგნის წაშლა.
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"message": "წიგნი ვერ მოიძებნა."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(Task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(Task, data=request.data, partial=False)
        if serializer.is_valid():
            updated_Task = serializer.save()
            return Response(
                {"message": "წიგნი წარმატებით განახლდა!", "Task": TaskSerializer(updated_Task).data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Task.delete()
        return Response({"message": "წიგნი წარმატებით წაიშალა."}, status=status.HTTP_204_NO_CONTENT)