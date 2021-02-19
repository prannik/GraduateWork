from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.conf import settings
from .decorators import check_recaptcha

@check_recaptcha
def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            if request.recaptcha_is_valid:
                new_user.save()
                return redirect('logout')

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


