from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from programs.models import Program, ProgramEnrollment, Resource
from ..serializers.program_serializers import (
    MinimalProgramSerializer, FullProgramSerializer, 
    ProgramEnrollmentSerializer, ResourceSerializer
)

class ProgramListView(APIView):
    def get(self, request):
        programs = Program.objects.filter(is_active=True)
        
        # Filtering
        topic = request.query_params.get('topic')
        if topic:
            programs = programs.filter(topic=topic)
            
        counselor_id = request.query_params.get('counselor_id')
        if counselor_id:
            programs = programs.filter(counselor_id=counselor_id)
            
        serializer = MinimalProgramSerializer(programs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FullProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgramDetailView(APIView):
    def get(self, request, id):
        program = get_object_or_404(Program, id=id)
        serializer = FullProgramSerializer(program)
        return Response(serializer.data)
    
    def put(self, request, id):
        program = get_object_or_404(Program, id=id)
        serializer = FullProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        program = get_object_or_404(Program, id=id)
        program.is_active = False
        program.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProgramEnrollmentView(APIView):
    def post(self, request, program_id):
        program = get_object_or_404(Program, id=program_id)
        user = request.user
        
        # Check if already enrolled
        if ProgramEnrollment.objects.filter(user=user, program=program).exists():
            return Response(
                {"error": "User is already enrolled in this program"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        enrollment = ProgramEnrollment.objects.create(user=user, program=program)
        serializer = ProgramEnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, program_id):
        program = get_object_or_404(Program, id=program_id)
        user = request.user
        
        enrollment = get_object_or_404(ProgramEnrollment, user=user, program=program)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResourceListView(APIView):
    def get(self, request, program_id):
        program = get_object_or_404(Program, id=program_id)
        resources = Resource.objects.filter(program=program)
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
    
    def post(self, request, program_id):
        program = get_object_or_404(Program, id=program_id)
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(program=program)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)