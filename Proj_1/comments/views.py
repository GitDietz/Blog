from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404
from .forms import CommentForm
from .models import Comment

def comment_delete(request, id):
    obj = get_object_or_404(Comment, id=id)
    if request.method =="POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete
        messages.success(request, 'This has been deleted')
        return HttpResponseRedirect(parent_obj_url)
    context = {
        'object' : obj
    }
    return render(request, 'comment_delete.html', context)

def comment_thread(request,id):
    print('inside function')
    obj = get_object_or_404(Comment, id=id)
    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id
    }
    # print(initial_data)
    form = CommentForm(request.POST or None, initial=initial_data)
    # print(dir(form))
    if form.errors:
        print(form.errors)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
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
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        'comment': obj,
        'form': form,
    }

    return render(request, "comment_thread.html", context)
