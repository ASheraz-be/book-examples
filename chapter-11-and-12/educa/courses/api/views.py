from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentsSerializer
from .permissions import IsEnrolled
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


class SubjectListView(ListAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer


class SubjectDetailView(RetrieveAPIView):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer


# a post() method for POST actions. No other HTTP method will be allowed for this view.
# class CourseEnrollView(APIView):
# 	authentication_classes = (BasicAuthentication,)
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, pk, format=None):
# 		course = get_object_or_404(Course, pk=pk)
# 		course.student.add(request.user)
# 		return Response({'enrolled': True})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

	@action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated])
	def enroll(self, request, *args, **kwargs):
		course = self.get_object()
		course.student.add(request.user)
		return Response({'enrolled': True})

	@action(detail=True, methods=['get'], serializer_class=CourseWithContentsSerializer, authentication_classes=[BasicAuthentication], permission_classes=[IsAuthenticated, IsEnrolled])
	def contents(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)