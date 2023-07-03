from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'# or provide a list of the attributes like 'user' 'description' 'email' etc
        exclude=['host','participants']