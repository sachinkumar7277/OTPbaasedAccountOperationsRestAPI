from rest_framework import serializers

from rest_framework.authentication import authenticate
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone','password','email','date_of_birth','username']
        extra_kwargs = {'password':{'write_only':True },}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['phone'], validated_data['email'],validated_data['date_of_birth'],validated_data['username'], validated_data['password'])

        return user





class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},trim_whitespace=False
    )
    def validate(self,data):
        print(data)
        phone = data.get('phone')
        password = data.get('password')

        if phone and password :
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                user = authenticate(request=self.context.get('request'),phone=phone,password=password)
                print(user)
            else:
                msg={"message":"Invalid credentials"}
                raise serializers.ValidationError(msg)
            if not user:
                msg = {"message": "user does not exist with this phone number"}
                raise serializers.ValidationError(msg,code='authorizarion')
        else:
            msg = {"message": "phone and password not given"}
            raise serializers.ValidationError(msg,code='authorizarion')
        data['user'] = user
        return data



class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['Profile_pic','pin_no','address','Fullname','phone_no','Email','date_of_birth']
        extra_kwargs = {'phone_no': {'read_only': True},'Email':{'read_only': True},}
    def update(self, instance, validated_data):
        instance.phone_no = validated_data.get('phone',instance.phone_no)
        instance.Email = validated_data.get('Email', instance.Email)
        instance.address = validated_data.get('address', instance.address)
        instance.Fullname = validated_data.get('Fullname', instance.Fullname)
        instance.Profile_pic = validated_data.get('Profile_pic', instance.Profile_pic)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance