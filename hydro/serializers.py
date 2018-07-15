from django.contrib.auth import get_user_model
from rest_framework import serializers
from hydro.models import *

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = tuple(User.REQUIRED_FIELDS) + (
			User._meta.pk.name,
			User.USERNAME_FIELD,
		)
		read_only_fields = (
			User.USERNAME_FIELD,
		)

class DataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Data
		fields = '__all__'

class DataTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DataType
		fields = '__all__'
