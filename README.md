# OTPbaasedAccountOperationsRestAPI
This app can be integrated with any project where we need two step verification and Authentication using OTP 
All the Operations are written using Django Rest Framework and can be used just by making an API call after integration with the frontend
Following operations are available in this account app :
1. Verify Phone or Generate OTP.
2. Verify OTP for further process for registration.
3. Register (all fields are mandatory to be filled)
4. Login (using Phone and Password )
5. Auto Profile creation whenever a new User will register it will automaticaly create profile for that user. using signals
6. Change Password 
7. Reset or Forget Password
8. Edit Profile ("id","phone","address",date_of_birth" etc need to pass )

Here we have used Custom User Model (by using AbstractBaseUser ,BaseUserManager etc )
phone number is USERNAME_FIELD
email,date_of_birth,username are REQUIRED_FIELD 
