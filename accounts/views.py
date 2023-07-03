from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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

@login_required
def my_account(request):
    return render(request, 'accounts/my_account.html')

@login_required
def edit_my_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('accounts:my_account')
    
    return render(request, 'accounts/edit_my_account.html')