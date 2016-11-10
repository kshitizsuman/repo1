from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render , get_object_or_404,redirect
from django.utils import timezone
from comments.models import Comment
# Create your views here.
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from .forms import PostForm
from .models import Post

def post_create(request):
	domain="http://"+request.META['HTTP_HOST']
	register=domain+"/register/"
	loginlink =domain+'/login/'
	logoutlink =domain+'/logout/'
	if not request.user.is_authenticated():
		return render(request,"form.html",{"message":"You must login to continue","register":register,"dashboard":domain,"loginlink":loginlink})
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.user=request.user
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"form":form,
		"dashboard":domain,"logoutlink":logoutlink,
	}
	return render(request,"post_form.html",context )

def post_detail(request , slug=None):
	instance = get_object_or_404(Post, slug=slug)
	domain="http://"+request.META['HTTP_HOST']
	register=domain+"/register/"
	loginlink =domain+'/login/'
	logoutlink =domain+'/logout/'
	createlink = domain+'/create/'
	if instance.draft or instance.publish > timezone.now().date():
		pass
	share_string = quote_plus(instance.content)

	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
						)
		

	comments = instance.comments
	context ={
		"register":register,"dashboard":domain,"loginlink":loginlink,"logoutlink":logoutlink,"createlink":createlink,
		"title" : instance.title,
		"instance" : instance,
		"share_string": share_string,
		"comments":comments,
		"comment_form":form,
	}
	return render(request,"post_detail.html",context )

def post_list(request):
	domain="http://"+request.META['HTTP_HOST']
	register=domain+"/register/"
	loginlink =domain+'/login/'
	logoutlink =domain+'/logout/'
	createlink = domain+'/create/'
	userpostlist = domain+'/userposts/'
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		query_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			    Q(title__icontains=query)|
			    Q(content__icontains=query)|
			    Q(user__first_name__icontains=query)|
			    Q(user__last_name__icontains=query)
			    ).distinct()

	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context ={
		"register":register,"dashboard":domain,"loginlink":loginlink,"logoutlink":logoutlink,
		"userpostlist":userpostlist,
		"createlink":createlink,
		"object_list" : queryset,
		"title" : "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request,"post_list.html",context )



def listing(request):
    contact_list = Contacts.objects.all()
    

    return render(request, 'list.html', {'contacts': contacts})




def post_update(request,slug =None):
	instance = get_object_or_404(Post, slug=slug)
	domain="http://"+request.META['HTTP_HOST']
	register=domain+"/register/"
	loginlink =domain+'/login/'
	logoutlink =domain+'/logout/'
	if not request.user.is_authenticated():
		return render(request,"form.html",{"message":"You must login to continue","register":register,"dashboard":domain,"loginlink":loginlink})
	if request.user != instance.user:
		 return render(request,"message.html",{"message":"You cannot edit this post.","dashboard":domain,"logoutlink":logoutlink})
	form = PostForm(request.POST or None, request.FILES or None , instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Saved")

		return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"title" : instance.title,
		"instance" : instance,
		"form":form,

	}
	return render(request,"post_form.html",context )

def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	domain="http://"+request.META['HTTP_HOST']
	register=domain+"/register/"
	loginlink =domain+'/login/'
	logoutlink =domain+'/logout/'
	if not request.user.is_authenticated():
		return render(request,"form.html",{"message":"You must login to continue","register":register,"dashboard":domain,"loginlink":loginlink})
	if request.user != instance.user:
		 return render(request,"message.html",{"message":"You cannot delete this post.","dashboard":domain,"logoutlink":logoutlink})
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("posts:list")


def post_user_list(request):
	domain="http://"+request.META['HTTP_HOST']
	register=domain+"/register/"
	loginlink =domain+'/login/'
	logoutlink =domain+'/logout/'
	createlink = domain+'/create/'
	userpostlist=domain+"/userposts/"
	today = timezone.now().date()
	queryset_list = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		query_list = Post.objects.all()

	query = request.GET.get("q")
	queryset_list = queryset_list.filter(user=request.user)

	paginator = Paginator(queryset_list, 2) # Show 2 posts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context ={
		"register":register,"dashboard":domain,"loginlink":loginlink,"logoutlink":logoutlink,"userpostlist":userpostlist,
		"createlink":createlink,
		"object_list" : queryset,
		"title" : "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request,"post_list.html",context )
