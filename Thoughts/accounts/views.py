from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from articles.models import Article


# Create your views here.
def signup_view(request):
	if request.method == 'POST':
		form = forms.SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			#pointing to name of url in articles app
			return redirect('articles:list')
	else:
		form = forms.SignUpForm()
	return render(request, 'accounts/signup.html', {'form': form})

def signin_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('articles:list')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/signin.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('articles:list')

@login_required(login_url = 'accounts:signin')
def profile_view(request):
	user = request.user
	my_articles = Article.objects.filter(author=user)
	if user.is_authenticated:
		return render(request, 'accounts/profile.html', {'my_articles':my_articles})