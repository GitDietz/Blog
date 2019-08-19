from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","create_date","update_date","user"]
    list_filter = ["create_date","update_date"]
    search_fields = ["title","content"]
    fields = ('title','content','image','height_field','width_field','user','read_time')
    #look at documentation online for things to do with it
    class Meta:
        model = Post

admin.site.register(Post,PostModelAdmin)
#register the Post model to the admin site and also the new class



# Register your models here.
