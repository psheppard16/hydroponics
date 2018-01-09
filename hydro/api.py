from rest_framework import viewsets, filters, generics, permissions
from hydro.serializers import *


###########################################################################
#                            HYDRO API VIEWSETS                           #
#                                                                         #
###########################################################################

# class ModelViewSet(viewsets.ModelViewSet):
#     # Router registration: 'model'
#
#     def perform_create(self, serializer):
#         serializer.save(submitter=self.request.user)
#         notify_notification(self.request.data)
#
#
#     queryset = Model.objects.all()
#     filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, filters.OrderingFilter,)
#     search_fields = ()
#     ordering = ()
