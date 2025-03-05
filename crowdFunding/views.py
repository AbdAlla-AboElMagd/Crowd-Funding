
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from crowdFunding.forms import CustomUserCreationForm
from django.contrib import messages
from crowdFunding.models import User  
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.urls import reverse
def home(request):
    if request.session.get('email'):
        return render(request=request, template_name='crowdFunding/home.html')
    else:
        return redirect(custom_login)

def about(request):
    if request.session.get('email'):
        return render(request=request, template_name='crowdFunding/about.html')
    else:
        return redirect(custom_login)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # لسه مش مفعل
            user.save()

            # إعدادات الإيميل
            current_site = get_current_site(request)
            mail_subject = 'فعل حسابك الآن'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"http://{current_site.domain}{activation_link}"
            
            message = render_to_string('crowdFunding/activation_email.html', {
                'user': user,
                'activation_url': activation_url
            })
            send_mail(mail_subject, message, 'drnasser.khairy@gmail.com', [user.email])

            messages.success(request, 'تم التسجيل! تحقق من بريدك الإلكتروني لتفعيل حسابك.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'crowdFunding/signup.html', {'user_creation_form': form})

from django.contrib.auth import get_user_model

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'تم تفعيل حسابك بنجاح! سجل دخولك الآن.')
        return redirect('login')
    else:
        messages.error(request, 'رابط التفعيل غير صالح أو انتهت صلاحيته.')
        return redirect('home')


# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
    
#         if form.is_valid():
#             form.save()
           
#             messages.success(request, 'تم التسجيل بنجاح! سجل دخولك الآن.')  
#             return redirect(custom_login)  
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'crowdFunding/signup.html', {'user_creation_form': form})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            request.session['email'] = user.email  
            return redirect('home')
        else:
            messages.error(request, 'البريد الإلكتروني أو كلمة المرور غير صحيحة!')

    return render(request, 'crowdFunding/login.html')
def custom_logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect(custom_login)
    
    
    
    
# def new(request):
#     form = UserForm()
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('home/')
#     return render(request=request, template_name='crowdFunding/register.html', context={'user_form': form})
    
# def signup(request):
#     user_creation_form = UserCreationForm()
#     if request.method == 'POST':
#         user_creation_form = UserCreationForm(request.POST)
#         if user_creation_form.is_valid():
#             user_creation_form.save()
#             user_name=user_creation_form.cleaned_data.get('username')
#             password=user_creation_form.cleaned_data.get('password1')
#             user=authenticate(username=user_name, password=password)
#             login(request, user)
#             return HttpResponseRedirect('home/')
#     context={
#             'user_creation_form': user_creation_form,
#     }
#     return render(request=request, template_name='crowdFunding/signup.html', context=context)
        
# def signup(request):
#     user_creation_form = CustomUserCreationForm()  # استخدام الفورم الجديد
#     if request.method == 'POST':
#         user_creation_form = CustomUserCreationForm(request.POST)
#         if user_creation_form.is_valid():
#             user = user_creation_form.save(commit=False)  # احفظ من غير ما تعمله save نهائي
#             user.is_active = True  # خليه نشط تلقائي
#             user.save()  # احفظ اليوزر
#             email = user_creation_form.cleaned_data.get('email')
#             password = user_creation_form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=password)  # التحقق بالإيميل والباسورد
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect('home/')
#     context = {
#         'user_creation_form': user_creation_form,
#     }
#     return render(request=request, template_name='crowdFunding/signup.html', context=context)






