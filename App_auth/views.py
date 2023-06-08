from rest_framework import viewsets, permissions, generics
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from App_auth.serializers import *


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"group_name": request.data['group_name']})
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer that includes user group in the response.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.first_name
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView that uses the CustomTokenObtainPairSerializer.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)

        groups = Group.objects.filter(user=user)
        group_names = [group.name for group in groups]

        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'group': group_names[0],
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom TokenRefreshView that uses the CustomTokenObtainPairSerializer.
    """
    serializer_class = CustomTokenObtainPairSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        patient_profile = serializer.save()
        return Response({"status": "Successfully Created"}, status=201)

    def retrieve(self, request, pk, **kwargs):
        patient_profile = ProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(patient_profile)
        return Response(serializer.data)

    def update(self, request, pk, **kwargs):
        patient_profile = ProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(patient_profile, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        patient_profile = serializer.save()
        return Response({"status": "Successfully Updated!"})

    def destroy(self, request, pk, **kwargs):
        patient_profile = ProfileModel.objects.get(pk=pk)
        patient_profile.delete()
        return Response(status=204)

    def patch(self, request, pk, **kwargs):
        patient_profile = ProfileModel.objects.get(pk=pk)
        serializer = self.serializer_class(patient_profile, data=request.data, partial=True,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        patient_profile = serializer.save()
        return Response({"status": "Successfully Updated!"})



