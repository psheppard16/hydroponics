from django.contrib.auth import get_user_model

from rest_framework import serializers, mixins
from rest_framework.fields import CurrentUserDefault

from hydro.models import *
from tagging.fields import Tag

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

# class ModelSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Model
# 		fields = '__all__'
