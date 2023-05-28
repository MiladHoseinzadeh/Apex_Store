from django.contrib.auth import login
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

# def login(request):
#     return render(request, 'accounts/login.html')