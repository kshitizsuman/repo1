from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Post
def post_create(request):
	return HttpResponse("<h1>Create")

def post_detail(request):
	context ={
		"title" : "Detail"
	}
	return render(request,"index.html",context )

def post_list(request):
	queryset = Post.objects.all()
	context ={
		"object_list" : queryset,
		"title" : "List"
	}
	return render(request,"index.html",context )

def post_update(request):
	return HttpResponse("<h1>Update Post.")

def post_delete(request):
	return HttpResponse("<h1>Delete Post")