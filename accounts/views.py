from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.conf import settings
from g_recaptcha.validate_recaptcha import validate_captcha
GOOGLE_RECAPTCHA_SITE_KEY: settings.GOOGLE_RECAPTCHA_SITE_KEY

@validate_captcha
def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('logout')

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


