from urllib.parse import quote_plus
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from Proj_1.Proj_1.logger import mylog
from comments.forms import CommentForm
from comments.models import Comment 
from .models import Post, Robot
from .forms import PostForm, RobotForm

@login_required
def post_create(request): #when the form submits, it requests the same url, comes to this form and is then rendered again
    print(f'Create view, user = {request.user.username} is authenticated ? {request.user.is_authenticated()}')
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'Successfully saved')
        return redirect('list')

    context = {
        'form': form,
    }
    return render(request, 'post_form.html', context)


def is_published(publish_date):
    if publish_date != None:
        if publish_date >  timezone.now().date():
            return True
    return False

@login_required
def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)   # can use any parameter in the model
    if instance.draft or is_published(instance.publish):
        if not request.user.is_superuser or not request.user.is_staff:
            raise Http404
    share_string = quote_plus(instance.content)
    comments = Comment.objects.filter_by_instance(instance)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    # print('read time is ' + get_read_time(instance.content))
    # above removed to rather put it in the daatabse with the models
    # use get_markdown
    print(initial_data)
    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        content_type = ContentType.objects.get(model=c_type)
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        # some method to reload the

    context = {
        'instance': instance,
        'title': instance.title,
        'form': comment_form,
        'share_string': share_string,
        'comments': comments,
        'content':''
    }
    return render(request, 'post_detail.html', context)


def post_detail_old(request): # now replaced with the above
    # instance = Post.objects.get(id=2) #better method below
    instance = get_object_or_404(Post,id=id) #can use any parameter in the model
    context = {
        'obj':instance,
    }
    return render(request, 'base.html', context)
    #return HttpResponse("<p>Hellow Wolly - detail</p>")

def post_list(request):
    mylog.info('Comment|Thread ')
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())        #.all()   #.order_by("-create_date") no longer needed since adding the order to the model
    if not request.user.is_superuser or not request.user.is_staff:
        queryset_list = Post.objects.active() #this will now get the model manager version of the override on all, called active
    else:
        queryset_list = Post.objects.all()
    # now look for the get request value to filter the view
    query = request.GET.get('q') # the value that is after q=
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 3)
    page_request_var = 'lpage'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'title': 'The list of stuff for all',
        'object_list': queryset,
        'page_request_var': page_request_var
    }
    ########
    # one way to introduce conditions and alter the context or bahviour
    # if request.user.is_authenticated():
    #     context = {
    #         'title':'The list of stuff for authenticated users'
    #     }
    # else:
    #     context = {
    #         'title': 'The list of stuff of other casual visitors'
    #     }
    return render(request, 'post_list.html', context)

@login_required
def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)  # can use any parameter in the model
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form
    }
    return render(request, 'post_form.html', context)
    # return HttpResponse("<p>Hellow Wolly - update some</p>") The very basic to confirm the view responds

@login_required
def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    #if not request.user.is_authenticated():
    #    raise Http404    one way of preventing non logged in users from posting
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request, 'Successfully deleted')
    return redirect('list')

#################### ROBOTS ###########################
def robot_list(request):
    queryset = Robot.objects.all()
    paginator = Paginator(queryset, 10)
    page_request_var = 'lpage'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'title': 'List of all our Robots',
        'object_list': queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'robot_list.html', context)

def robot_create(request):
    form = RobotForm(request.POST or None, request.FILES or None)
    print('form loaded')
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get('name'))
        instance.save()
        messages.success(request,'Successfully saved')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Failed to saved')

    print('pre - context')
    context = {
        'form': form
    }
    return render(request, 'robot_form.html', context)

def robot_detail(request, id=None):
    instance = get_object_or_404(Robot, id=id) #can use any parameter in the model
    form = RobotForm(request.POST or None, request.FILES or None, instance=instance)
    print(instance)
    context = {
        'instance': instance,
        'form': form
    }
    return render(request, 'robot_detail.html', context)