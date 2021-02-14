from rest_framework import generics, serializers
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSeriailizer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseErollView(APIView):
    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated, )
    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSeriailizer

    @detail_route(methods=['post'], 
    authentication_classes=[BasicAuthentication], 
    permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})
    
    @detail_route(methods=['get'], 
    serializer_class=CourseWithContentsSerializer, 
    authentication_classes=[BasicAuthentication], 
    permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)