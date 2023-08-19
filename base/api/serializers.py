#serializers are classes that take a certain model or object that we wamt to serialize
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'