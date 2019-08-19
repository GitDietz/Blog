from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    # url(r'^posts/$', "work_posts.views.post_home"), # the direct method this
    url(r'^posts/', include("work_posts.urls")),
    # this includes the urls file under the work_post folder, but only the part after "posts/"
    # in work_posts.urls you will only see the remaining part so posts/delete is split and routed
    ]

if settings.DEBUG:      # ensures that this will only be done in DEV
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    url(r'robot/', include('work_posts.robot_urls')),

    ]

