import os

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .forms import ProfileForm, ContactForm, PostForm, SeekForm
from .models import Goods, Category, Profile, Tag, Seek
from .decorators import canonical

# Create your views here.
def index(request):
	goods = Goods.objects.filter(status=Goods.RECOMMENDED)
	query = request.GET.get("q")
	if query:
		goods = goods.filter(
				Q(name__icontains=query)|
				Q(price__icontains=query)
				).distinct()
	paginator = Paginator(goods, 9) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	return render(request, "trade/index.html", {'goods': goods})

def seek(request):
	lost_found = Seek.objects.filter(status=Seek.lost_found)
	demand = Seek.objects.filter(status=Seek.demand)
	context = {
		"lost_found": lost_found,
		"demand": demand,
	}
	return render(request, "trade/square.html", context) 	

def seek_post(request):
	if request.user.is_authenticated():
		form = SeekForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "添加成功")
			return HttpResponseRedirect('/')
		context = {
			"form": form,
		}
	else:
		messages.info(request, "请先登录")
		return HttpResponseRedirect('/../accounts/login')		
	return render(request, 'trade/seekpost.html', context)	

def help(request):
	return render(request, "trade/help.html", {})
 
"""
用户扩展views
"""
@canonical(Profile)
def profile(request, profile):
	"""
	用户主页
	"""
	return render(request, 'trade/profile.html', {
		"profile": profile,
	})

@login_required
@transaction.atomic
def setting(request, id):
	"""
	编辑用户资料
	"""
	profile = get_object_or_404(Profile, user=id)
	form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
	if form.is_valid():
		profile = form.save(commit=False)
		profile.save()
		messages.success(request, "更新成功")
		return HttpResponseRedirect('/')
	context = {
		"form": form,
		"profile": profile,
	}
	return render(request, 'trade/setting.html', context) 

def mygoods(request):
	user = request.user
	mygoods = Goods.objects.filter(user=user.id)
	return render(request, 'trade/mygoods.html', {"mygoods": mygoods}) 


def contact(request):
	"""
	联系我们
	"""
	form = ContactForm(request.POST or None)
	if form.is_valid():
		full_name = form.cleaned_data.get("full_name")
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		#print (email, message, full_name)
		subject = '大学生二手交易网站'
		message = "%s: %s %s"%(
					full_name, 
					email, 
					message
				)

		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email]

		if subject and message and from_email and to_email:
			try:
				send_mail(
					subject, 
					message, 
					from_email,
					to_email, 
					#html_message= some_html_message,
					fail_silently =False
				)
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			messages.success(request, "感谢您的建议")
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("Make sure all fields are entered and valid")	

	context = {
		"form":form,
	}
	return render(request, "trade/contact.html", context)	  

def list(request, category_id=None):
	"""
	物品列表
	"""
	categories = Category.objects.filter(goods__status=Goods.RECOMMENDED).annotate(num_goods=Count('goods'))

	goods = Goods.objects.filter(status=Goods.RECOMMENDED)

	sort = request.GET.get('sort')
	if sort == 'views':
		goods = goods.order_by('-view_count')
	else:
		goods = goods.order_by('-timestamp')

	current_category = None
	if category_id != None:
		current_category = get_object_or_404(Category, pk=category_id)
		goods = goods.filter(category=current_category)

	paginator = Paginator(goods, 16)
	page = request.GET.get('page')
	try:
		goods = paginator.page(page)
	except PageNotAnInteger:
		goods = paginator.page(1)
	except EmptyPage:
		goods = paginator.page(paginator.num_pages)

	sort_urls = {}
	url_get_params = request.GET.copy()
	url_get_params['sort'] = 'published'
	sort_urls['published'] = '?' + url_get_params.urlencode()
	url_get_params['sort'] = 'views'
	sort_urls['views'] = '?' + url_get_params.urlencode()
	
	context = {
		"current_category": current_category,
		"categories": categories,
		"goods": goods,
		"sort_urls": sort_urls
	}

	return render(request, 'trade/list.html', context)

def detail(request, id=None):
	goods_detail = get_object_or_404(Goods, id=id)
	context = {
		"goods_detail": goods_detail,
	}
	return render(request, 'trade/detail.html', context) 
	
def post(request):
	if request.user.is_authenticated():
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "添加成功")
			return HttpResponseRedirect('/')
		context = {
			"form": form,
		}
	else:
		messages.info(request, "请先登录")
		return HttpResponseRedirect('/../accounts/login')		
	return render(request, 'trade/post.html', context)	
	
def update(request, id=None):
	update = get_object_or_404(Goods, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=update)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "添加成功")
		return HttpResponseRedirect('/')

	context = {
		"update": update,
		"form": form,
	}
	return render(request, 'trade/update.html', context)

def delete(request, id=None):
	delete = get_object_or_404(Goods, id=id)
	delete.delete()
	return redirect("trade:mygoods")
