from django.shortcuts import render, redirect
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
import random

# Create your views here.
def article_list(request):
	articles = Article.objects.all().order_by('date')
	if articles:
		feat = random.choice(articles)
		return render(request, "articles/article_list.html", {'articles_list':articles, 'feat':feat})
	return render(request, "articles/article_list.html", {'articles_list':articles, 'feat':None})

@login_required(login_url = '/accounts/signin/')
def article_page(request, slug):
	article = Article.objects.get(slug=slug)
	user = request.user.username
	vote = ["Upvote", "Remove Upvote"][article.check_for_user(user)]
	return render(request, "articles/article_page.html", {'article':article, 'vote': vote})

@login_required(login_url = '/accounts/signin/')
def article_create(request):
	if request.method == 'POST':
		form = forms.CreateArticle(request.POST, request.FILES)
		if form.is_valid():
			form_inst = form.save(commit=False)
			form_inst.author = request.user
			form_inst.save()
			return redirect('articles:list')
	else:
		form = forms.CreateArticle()
	return render(request, 'articles/article_create.html', {'form': form })


def article_upvote(request, slug):
	article = Article.objects.get(slug=slug)
	if request.user != None:
		user = request.user.username
		if article.check_for_user(user):
			print('exists')
			article.remove_from_upvotes(user)
			article.save()
			return redirect('/articles/'+ slug)
		else:
			print('nahi exists')
			article.add_to_upvotes(user)
			article.save()
			return redirect('/articles/'+ slug)
	else:
		return redirect('accounts:signin')