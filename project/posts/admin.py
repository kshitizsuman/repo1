from django.contrib import admin


from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp"]
	list_display_links = ["updated"]
	class Meta:
		model = Post


admin.site.register(Post)