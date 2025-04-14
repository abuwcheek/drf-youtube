from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Chanel
from .serializers import ChanelSerializer, GetChanelDataSerializers




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

          name = request.data.get('name')
          if not name:
               data = {
                    'status': False,
                    'message': "Kanal nomi kiritilmadi"
               }
               return Response(data=data)
          
          if Chanel.objects.filter(name=name).exists():
               data = {
                    'status': False,
                    'message': "Bu kanal nomi band"
               }
               return Response(data=data)
          

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



class GetChanelDataAPIView(ListAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = GetChanelDataSerializers

     def get_queryset(self):
          return self.request.user.chanel_subscribed.all()

     def get_serializer_context(self):
          return {
               'request': self.request  # bu MUHIM!
          }

     def list(self, request, *args, **kwargs):
          queryset = self.get_queryset()
          serializer = self.get_serializer(queryset, many=True)
          return Response({
               'status': True,
               'data': serializer.data
          })




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



