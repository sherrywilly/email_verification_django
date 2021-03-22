from core.form import CustomuserCreationForm
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import  get_current_site
from django.utils.encoding import force_bytes,force_text
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.




from django.core.mail import send_mail
from django.conf import settings


def email(a,b):
    subject = 'Activation Email'
    message = a
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [b,]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('registration')

class RegView(View):
    def get(self,request):
        form = CustomuserCreationForm()
        context = {
            'form':form
        }
        return render(request,"form.html",context)

    def post(self,request):
        form = CustomuserCreationForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_Site = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            _x = reverse("active",kwargs={'uidb64':uid,'token':token})
            myrl = 'http://'+current_Site+_x
            email(myrl,to_email)
            return redirect(reverse('registration'))
        else:
            print(form.errors)
            return redirect(reverse('registration'))





class Activation(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')