from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Chanel
from .serializers import ChanelSerializer




class ChanelCreateAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          try:
               chanel = request.user.chanel
               if chanel:
                    data = {
                         'status': False,
                         'message': "Bu user da kanal mavjud"
                    }
                    return Response(data=data)
          except Exception as ex:
               pass

          serializer = ChanelSerializer(data=request.data, context={'request': request})
          serializer.is_valid(raise_exception=True)
          chanel = serializer.save()
          chanel.user = request.user
          chanel.save()

          data = {
               'status': True,
               'message': "Kanal yaratildi",
               'data': serializer.data
          }
          return Response(data=data)



class GetChanelDataAPIView(APIView): 
     permission_classes = [IsAuthenticated]

     def get(self, request):
          chanel = get_object_or_404(Chanel, user=request.user)
          serializer = ChanelSerializer(instance=chanel, context={'request': request})
          data = {
               'status': True,
               'data': serializer.data
          }
          return Response(data=data)



class DeleteChanelAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def delete(self, request, pk):
          chanel = get_object_or_404(Chanel, pk=pk)
          if chanel.user == request.user:
               chanel.delete()
               data = {
                    'status': True,
                    'message': "Kanal o'chirildi"
               }
               return Response(data=data)
          else:  
               data = {
                    'status': False,
                    'message': "Bu kanal sizga tegishli emas"
               }
               return Response(data=data)