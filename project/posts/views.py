from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render , get_object_or_404,redirect

# Create your views here.
from .forms import PostForm
from .models import Post

def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"form":form,
	}
	return render(request,"post_form.html",context )

def post_detail(request , slug=None):
	instance = get_object_or_404(Post, slug=slug)
	share_string = quote_plus(instance.content)
	context ={
		"title" : instance.title,
		"instance" : instance,
		"share_string": share_string,
	}
	return render(request,"post_detail.html",context )

def post_list(request):
	queryset_list = Post.objects.all()
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
		"object_list" : queryset,
		"title" : "List",
		"page_request_var": page_request_var
	}
	return render(request,"post_list.html",context )



def listing(request):
    contact_list = Contacts.objects.all()
    

    return render(request, 'list.html', {'contacts': contacts})




def post_update(request,slug =None):
	instance = get_object_or_404(Post, slug=slug)
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
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("posts:list")