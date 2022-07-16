from django.shortcuts import render
from rest_framework.views import APIView,Response
from rest_framework import permissions,status,generics
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from .serializers import CreateUserSerializer ,LoginSerializer,EditProfileSerializer

from . models import User,OTP,Profile
import random
from django.contrib.auth.decorators import login_required
from knox.views import LoginView,LogoutView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

@method_decorator(csrf_exempt,name='dispatch')
class SendOTPphone(APIView):
    """
     provide phone  in json format to meet ur request as follow
    {
    "phone" : "8373733743"
   }

    """
    def post(self,request,*args,**kwargs):
        print(request.data)
        phone_number = request.data.get("phone")
        print(phone_number)
        if phone_number:

            user = User.objects.filter(phone__iexact = phone_number)
            if user.exists():
                return Response({
                    'status': False,
                    'detail':"Failed to enroll as phone number already taken "
                })
            else:

               key =  SendOTP(phone_number)
               if key:
                   old_otp = OTP.objects.filter(phone = phone_number)
                   if old_otp.exists():
                       old = old_otp.first()
                       count = old.count
                       print(count)
                       if count > 4:
                           return Response({
                               'status': False,
                               'detail': 'OTP sending limit is crossed contact to customer care on 8340312640 '

                           })
                       else:
                           old.count = count+1
                           old.otp = key
                           old.save()
                           return Response({
                               "status": True,
                               "OTP": key,
                               "Detail": "OTP sent Successfully "

                           })

                   OTP.objects.create(
                       phone = phone_number,
                       otp = key,
                       count =1
                   )
                   return Response({
                       "status": True,
                       "OTP" : key,
                       "Detail": "OTP sent Successfully "


                   })
               else:
                   return Response({
                       'status': False,
                       'detail': 'Something Went Wrong please contact customer support'

                   })


        else:
            return Response({
                'status': False,
                'detail': 'Phone Number Not Given plz input valid phone number'

            })


def SendOTP(phone):
    if phone :
        key = random.randint(999,9999)
        return key
    else:
        return False


class validateOTP(APIView):
    """
    if user has already recieved the otp then  redirect to set password for registration

    provide phone and OTP in jason format to meet ur request as follow
    {

    "phone" : "83737337434" ,
    "otp" : "4848"

    }
    """
    def post(self,request,*args,**kwargs):
        phone = request.data.get("phone")
        sent_otp = request.data.get("otp")
        if phone and sent_otp:
            old = OTP.objects.filter(phone__iexact = phone)
            old = old.first()
            if str(sent_otp) == old.otp :
                old.validated = True
                old.save()
                return Response({
                    "status" : True,
                    "Message " : "OTP Matched proceed for registration "

                })
            else:
                return Response({
                    "status": False,
                    "Message ": "OTP Not Matched Try Again with valid otp "

                })
        else:
            return Response({
                "status": False,
                "Message ": "Enter valid phone number in valid json format "

            })



class Register(APIView):

    """
     provide phone and password in json format to meet ur request as follow
    {

    "phone" : "8737337434",
    "pwd"   : "Sanjf38339@",
    "email" : "sajjff27636@gmail.com",
    "DOB"   :  "1998-12-30",
    "username" : "sachin"

    }

    """
    def post(self,request,*args,**kwargs):
        phone = request.data.get("phone")
        password = request.data.get("pwd")
        email = request.data.get("email")
        DOB = request.data.get("DOB")
        print(phone,password)
        if phone and password :
            old = OTP.objects.filter(phone__iexact = phone)
            if old.exists() :
                old = old.first()
                if old.validated:
                    temp_data = {
                        "phone":phone,
                        "password":password,
                        "email" : email,
                        "date_of_birth":DOB,
                        "username":request.data.get("username")

                    }
                    serializer =  CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        "status" : True,
                        "message" : "Account created",
                        "token": AuthToken.objects.create(user)[1]
                    })
                else:
                    return Response({
                        "status": False,
                        "message": "Account not created First verify ur phone"
                    })
            else:

                return Response({
                    "status": False,
                    "message": "Account not created First verify ur phone"
                })
        else:
            return Response({
                "status": False,
                "message": "Enter valid phone or password in json format"
            })



class LoginAPI(LoginView):
    """
     provide phone and password in json format to meet ur login request as follow
    {

    "phone" : "8737337434",
    "password"   : "Sanjf38339@"
    }
    """

    permission_classes = (permissions.AllowAny,)
    def post(self,request, format = None):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        logged_in = login(request,user)
        print(logged_in)
        if logged_in:
            print("user is logged in ")
        return super().post(request,format=None)



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfile(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request,*args, **kwargs):
        data = request.data
        queryset = Profile.objects.filter(id = data['id'])
        serializer = EditProfileSerializer(queryset,data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():

            return Response({
                "UpdatedData":serializer.validated_data,
                'status': True,
                "msg" : "Data successfully updated"

            })
        else:
            return Response({
                "msg": "something went wrong",
                "status": False
            })
