from rest_framework import viewsets

from .models import Direction, Faculty, Group
from .serializers import DirectionSerializer, FacultySerializer, GroupSerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DirectionViewSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer

    def get_queryset(self):
        queryset = Direction.objects.select_related('faculty')
        faculty = self.request.query_params.get('faculty')
        if faculty:
            queryset = queryset.filter(faculty_id=faculty)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = Group.objects.select_related('direction__faculty')
        direction = self.request.query_params.get('direction')
        if direction:
            queryset = queryset.filter(direction_id=direction)
        return queryset
