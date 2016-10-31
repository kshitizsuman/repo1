from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404

# Create your views here.
from .models import Post
def post_create(request):
	return HttpResponse("<h1>Create")

def post_detail(request):
	instance = get_object_or_404(Post, id=2)
	context ={
		"title" : "Detail",
		"instance" : instance,
	}
	return render(request,"single.html",context )

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