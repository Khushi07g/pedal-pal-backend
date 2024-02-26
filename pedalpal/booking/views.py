from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import authentication
from django.http.response import JsonResponse
from booking.models import Cycle, Ride
from booking.serializers import BookRideSerializer, RideSerializer
import datetime

from django.http import JsonResponse
from django.db.models import Count,Q



from booking.models import Hub,Cycle
from booking.serializers import CycleSerializer
from .serializers import HubSerializer

class BookNowAPI(generics.GenericAPIView):
    serializer_class = BookRideSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cycle = serializer.validated_data.get("cycle")
        user = self.request.user

        if user.is_ride_active():
            return JsonResponse(
                {"message": "User already has an active ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cycle.is_booked():
            return JsonResponse(
                {"message": "Cycle already booked"}, status=status.HTTP_400_BAD_REQUEST
            )

        cycle.book(user)
        user.set_ride_active(True)

        start_time = datetime.datetime.now()
        ride = Ride.objects.create(
            user=user,
            cycle=cycle,
            start_time=start_time,
            end_time=None,
            start_hub=cycle.hub,
            end_hub=None,
            time=0,
            payment_id=None,
        )

        serializer = RideSerializer(ride)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    




class ViewsAPI(generics.GenericAPIView):


    


    def get(self, request, *args, **kwargs):
        queryset = Hub.objects.all()
        serializer_class = HubSerializer
        available_cycles = Hub.objects.annotate(num_available=Count('cycle', filter=Q(cycle__booked=False))).values_list('id', flat=True)
        hub_data = serializer_class(queryset, many=True).data
        for hub in hub_data:
            hub['available'] = available_cycles[hub_data.index(hub)]
        return JsonResponse(hub_data,safe=False)   


        