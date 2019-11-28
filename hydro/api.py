from rest_framework import viewsets, filters
from hydro.serializers import *
from django_filters.rest_framework import DjangoFilterBackend


###########################################################################
#                            HYDRO API VIEWSETS                           #
#                                                                         #
###########################################################################

# Data Viewsets
class DataViewSet(viewsets.ModelViewSet):
    # Router registration: 'data'
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)

# Data Viewsets
class DataTypeViewSet(viewsets.ModelViewSet):
    # Router registration: 'data'
    queryset = DataType.objects.all()
    serializer_class = DataTypeSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)