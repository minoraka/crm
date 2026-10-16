from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers, viewsets

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'username',
            'password',
            'last_name',
            'first_name',
            'middle_name',
            'full_name',
            'email',
            'birth_date',
            'gender',
            'phone',
            'address',
            'photo',
            'student_id',
            'group',
            'group_name',
            'course',
            'admission_year',
            'education_form',
            'funding',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'student_id': {'required': True, 'allow_null': False, 'allow_blank': False},
            'group': {'required': True, 'allow_null': False},
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(list(error.messages))
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Обязательное поле.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(password)
        student.save()
        return student

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        student = super().update(instance, validated_data)
        if password:
            student.set_password(password)
            student.save()
        return student


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.select_related('group').filter(is_superuser=False)
        group = self.request.query_params.get('group')
        if group:
            queryset = queryset.filter(group_id=group)
        return queryset
