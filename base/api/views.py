from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
@api_view(['GET']) #we specify the http meto=hods which are allowed to access this API
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id'
    ]
    #return JsonResponse(routes,safe=False)
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    serializer=RoomSerializer(rooms,many=True)
    #gives error as the python django objects cannot be easily jsonified
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    rooms=Room.objects.get(id=pk)
    serializer=RoomSerializer(rooms,many=False)
    #gives error as the python django objects cannot be easily jsonified
    return Response(serializer.data)