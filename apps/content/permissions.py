from rest_framework.permissions import BasePermission


class IsHasChanel(BasePermission):
     def has_permission(self, request, view):
          if request.user.is_authenticated:
               if getattr(request.user, 'chanel', None):
                    return True
          return False
     


class IsOwner(BasePermission):
     def has_object_permission(self, request, view, obj):
          if request.user.is_authenticated:
               if obj.author == request.user.chanel:
                    return True
          return False



class IsAuthor(BasePermission):
     def has_object_permission(self, request, view, obj):
          solo = super().has_object_permission(request, view, obj)
          return solo and obj.user == request.user