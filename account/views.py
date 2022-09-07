from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .send_sms import send_code


def register(request):
    
    if request.method == 'POST':
        
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        
        if password != password_repeat or len(password) < 5:
            messages.warning(request, 'اشکال در رمز عبور')
            return redirect('main:index')
        
        accounts = Account.objects.filter(phone_number__iexact=phone_number)
        
        if accounts:
            messages.warning(request, 'اکانت با این شمارهه از قبل وجود دارد')
            return redirect('main:index')
        
        Account.objects.create_user(
            phone_number=phone_number,
            email=email,
            name=name,
            last_name=last_name,
            password=password,
            is_active=False,
        )
        
        otp = Otp.objects.filter(phone_number__iexact=phone_number)
        
        for obj in otp:
            obj.delete()
            
            
        code = send_code(phone_number=phone_number)
        Otp.objects.create(phone_number=phone_number, code=code)
        
        return redirect('account:confirm_code', pk="register", phone_number=phone_number)
    
    
    
    
def confirm_code(request, phone_number, pk):
    otp = Otp.objects.get(phone_number=phone_number)
    account = Account.objects.get(phone_number=phone_number)
    
    if pk == 'register':
        
        if request.method == 'POST':
            code = request.POST.get('code')
            
            if int(code) != int(otp.code):
                messages.warning(request, 'کد وارد شده اشتباه است')
                
                return redirect('account:confirm_code', pk='register', phone_number=phone_number)
            
            account.is_active = True
            account.save()
            otp.delete()
            
            login(request, account)
            return redirect('main:index')
        
    
    if pk == "login":
        
        if request.method == "POST":
            code = request.POST.get('code')
            
            if int(code) != int(otp.code):
                messages.warning(request, 'کد وارد شده اشتباه است')
                
                return redirect('account:confirm_code', pk='register', phone_number=phone_number)
            
            otp.delete()
            login(request, account)
            return redirect("main:index")
        
        
    if pk == 'reset-password':
        
        if request.method == 'POST':
            code = request.POST.get('code')
            
            if int(code) != int(otp.code):
                messages.warning(request, 'کد وارد شده اشتباه است')
                
                return redirect('account:confirm_code', pk='register', phone_number=phone_number)
            
            
            otp.delete()
            login(request, account)
            
            return redirect('account:set_password', pk=account.id)
        
        
    return render(request, 'confirm-code.html')



def logout_user(request):
    
    logout(request)
    
    return redirect ("main:index")



def login_user(request):
    
    if request.method == 'POST':
        
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        user = authenticate(phone_number=phone_number, password=password)
        
        if user is None:
            messages.warning(request, 'نام کاربری یا رمز عبور اشکال دارد')
            return redirect("main:index")
        
        
        otp = Otp.objects.filter(phone_number__iexact=phone_number)
        
        for obj in otp:
            obj.delete()
            
            
        code = send_code(phone_number=phone_number)
        Otp.objects.create(phone_number=phone_number, code=code)
        
        
    return redirect("account:confirm_code", pk='login', phone_number=phone_number)



def reset_password(request):
    
    if request.method == 'POST':
        
        phone_number = request.POST.get('phone_number')
        
        account = Account.objects.filter(phone_number__iexact=phone_number)
        
        if not account:
            messages.warning(request, "اکانتی با این شماره تلفن یافت نشد")
            return redirect("account:reset_password")
        
        
        otp = Otp.objects.filter(phone_number__iexact=phone_number)
        
        for obj in otp:
            obj.delete()
            
            
        code = send_code(phone_number=phone_number)
        Otp.objects.create(phone_number=phone_number, code=code)
        
        return redirect("account:confirm_code", pk="reset-password", phone_number=phone_number)
    
    return render(request, 'reset-password.html')




def set_password(request, pk):
    
    account = Account.objects.get(id=pk)
    
    if request.method == 'POST':
        
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        
        if password != password_repeat or len(password) < 5:
            messages.warning(request, 'اشکال در رمز عبور وارد شده')
            return redirect('account:set_password')
        
        account.set_password(password)
        account.save()
        messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
                         
        return redirect('main:index')
    
    return render(request, 'set-password.html')



def profile(request):
    
    account = request.user
    
    if request.method == 'POST':
        
        email = request.POST.get('email')
        name= request.POST.get('name')
        last_name= request.POST.get('last_name')
        profile_img = request.FILES.get('profile_img')
        
        account.email = email
        account.name = name 
        account.last_name = last_name
        
        if profile_img:
            account.profile_img = profile_img
            
        account.save()
        
        messages.success(request, 'اکانت شما با موفقیت به روز رسانی شد')
        return redirect('account:profile')
    
    return render(request, 'profile.html')
        
        