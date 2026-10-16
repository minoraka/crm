from rest_framework.routers import DefaultRouter

from academics.views import DirectionViewSet, FacultyViewSet, GroupViewSet
from users.api import StudentViewSet

router = DefaultRouter()
router.register('faculties', FacultyViewSet, basename='faculty')
router.register('directions', DirectionViewSet, basename='direction')
router.register('groups', GroupViewSet, basename='group')
router.register('students', StudentViewSet, basename='student')

urlpatterns = router.urls
