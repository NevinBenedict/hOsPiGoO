from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.core.mail import send_mail
import random
from datetime import datetime, timedelta
from hospitalapp.models import *



# Create your views here.

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form,'current_page':'register'})

    def post(self, request):
        print(request.POST)
        otp=str(random.randint(1000,9999))
        print(otp)
        request.session['otp_created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            print('form is valid')
            request.session['otp']=otp
            request.session['email']=request.POST.get('email')
            request.session['username']=request.POST.get('username')
            request.session['first_name']=request.POST.get('first_name')
            request.session['last_name']=request.POST.get('last_name')
            request.session['phone']=request.POST.get('phone')
            request.session['password']=request.POST.get('password')
            subject = 'OTP for Registration'
            message = f'Your OTP for registration is {otp}'
            email_from = 'nevinbenedict07@gmail.com'
            recipient_list = [request.POST.get('email'), ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'otp.html',)
        return redirect('register')
    
class RegisterVerificationView(View):

    def post(self, request):
        otp_created_at = request.session.get('otp_created_at')
        
        if otp_created_at:
            otp_created_at = datetime.strptime(otp_created_at, '%Y-%m-%d %H:%M:%S')
            remaining_time = timedelta(seconds=150) - (datetime.now() - otp_created_at)
            
            
            if remaining_time.total_seconds() <= 0:
                request.session['otp'] = None  
                
                # Invalidate the OTP

                return redirect('login')
        otp=request.POST.get('otp1')+request.POST.get('otp2')+request.POST.get('otp3')+request.POST.get('otp4')
        if otp== request.session['otp']:
            user = CustomUser.objects.create_user(username=request.session['username'], first_name=request.session['first_name'], last_name=request.session['last_name'], email=request.session['email'], phone=request.session['phone'], password=request.session['password'])
            user.save()
            return redirect('login')
        else:
            return render(request, 'otp.html', {'message': 'Invalid OTP. Please try again.'})

class DocRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form,'current_page':'docregister'})

    def post(self, request):
        otp = str(random.randint(1000, 9999))
        print(otp)
        request.session['otp_created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form = UserRegistrationForm(request.POST)
        # print(form)
        if form.is_valid():
            print('form is valid')
            request.session['otp'] = otp
            print(otp)
            request.session['email'] = form.cleaned_data['email']
            request.session['username'] = form.cleaned_data['username']
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['phone'] = form.cleaned_data['phone']
            request.session['password'] = form.cleaned_data['password']
            subject = 'OTP for Registration'
            message = f'Your OTP for registration is {otp}'
            email_from = 'nevinbenedict07@gmail.com'
            recipient_list = [form.cleaned_data['email']]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'docotp.html')
        return redirect('register')
    
class DocRegisterVerificationView(View):
    def post(self, request):
        otp_created_at = request.session.get('otp_created_at')
        if otp_created_at:
            otp_created_at = datetime.strptime(otp_created_at, '%Y-%m-%d %H:%M:%S')
            remaining_time = timedelta(seconds=150) - (datetime.now() - otp_created_at)
            if remaining_time.total_seconds() <= 0:
                request.session['otp'] = None
                return redirect('register')
        otp = (
            request.POST.get('otp1', '') +
            request.POST.get('otp2', '') +
            request.POST.get('otp3', '') +
            request.POST.get('otp4', '')
        )
        print(otp)
        print(request.session.get('otp'))
        if otp == request.session.get('otp'):

            user = CustomUser.objects.create_user(
                username=request.session.get('username'),
                first_name=request.session.get('first_name'),
                last_name=request.session.get('last_name'),
                email=request.session.get('email'),
                phone=request.session.get('phone'),
                password=request.session.get('password'),
                is_doctor=True
            )
            user.save()
            request.session['user'] = user.id
            return redirect('docreg')
        else:
            return render(request, 'otp.html', )

class UserLoginView(View):

    def get(self, request):
        
        return render(request, 'login.html', {'current_page': 'login'})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            AppointmentSlot.objects.filter(date=datetime.today().date()).delete()
            
            print('login successful')
            if user.is_doctor:
                return redirect('doctorhome')
           

            return redirect('patienthome')
        else:
            print('login failed')
            return render(request, 'login.html')
        

class UserLogoutView(View):
    def get(self, request):
        print(request.user)
        logout(request)
        return redirect('login')
        
    
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgotpassword.html')
    
    def post(self, request):
        request.session['email']=request.POST.get('email')
        email = request.POST.get('email')
        
        user = CustomUser.objects.get(email=email)
        if user:
            otp=str(random.randint(1000,9999))
            request.session['otp']=otp
            request.session['otp_created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            request.session['email']=email
            subject = 'OTP for Password Reset'
            message = f'Your OTP for password reset is {otp}'
            email_from = 'nevinbendict07@gmail.com'
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'forgotpasswordotp.html',)

class ForgotPasswordVerificationView(View):
    def post(self, request):
        otp=request.POST.get('otp1')+request.POST.get('otp2')+request.POST.get('otp3')+request.POST.get('otp4')
        print(otp)
        if otp_created_at:
            otp_created_at = datetime.strptime(otp_created_at, '%Y-%m-%d %H:%M:%S')
            remaining_time = timedelta(seconds=150) - (datetime.now() - otp_created_at)
            
            
            if remaining_time.total_seconds() <= 0:
                request.session['otp'] = None  
                
                # Invalidate the OTP

                return redirect('login')
        if otp == request.session['otp']:
            return render(request, 'newpassword.html', {'message': 'Password reset successful. Please login.'})
        else:
            return render(request, 'forgotpasswordotp.html', {'message': 'Invalid OTP. Please try again.'})
        
class ResetPasswordView(View):
    def post(self, request):
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'newpassword.html', {'message': 'Passwords do not match. Please try again.'})
        print(request.session.get('email'))
        user = CustomUser.objects.get(email=request.session.get('email'))
        user.set_password(password)
        user.save()
        return redirect('login')

class ResendOtpView(View):
    def post(self, request):
        otp=str(random.randint(1000,9999))
        request.session['otp']=otp
        request.session['otp_created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        
        subject = 'OTP for Registration'
        message = f'Your OTP for registration is {otp}'
        email_from = 'nevinbenedict07@gmail.com'
        recipient_list = [request.session['email'], ]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, 'forgotpasswordotp.html',)

class ResendRegOtpView(View):
    def post(self, request):
        otp=str(random.randint(1000,9999))
        request.session['otp_created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        request.session['otp']=otp
        subject = 'OTP for Registration'
        message = f'Your OTP for registration is {otp}'
        email_from = 'nevinbenedict07@gmail.com'
        recipient_list = [request.session['email'], ]
        send_mail(subject, message, email_from, recipient_list)