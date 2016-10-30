from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def post_create(request):
	return HttpResponse("<h1>Create")

def post_detail(request):
	return HttpResponse("<h1>Post detail")

def post_list(request):
	return HttpResponse("<h1>List view.")

def post_update(request):
	return HttpResponse("<h1>Update Post.")

def post_delete(request):
	return HttpResponse("<h1>Delete Post")