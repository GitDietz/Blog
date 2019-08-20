from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse
from .forms import CommentForm
from .models import Comment

def comment_delete(request, id):
    # obj = get_object_or_404(Comment, id=id)
    try:
        obj = Comment.objects.get(id=id)
        print(f'object id is {obj.id}')
    except:
        raise Http404

    if obj.user != request.user:
        # messages.success(request,"you have no premission to do this")
        # raise Http404
        response = HttpResponse("you have no permission to do this")
        response.status_code = 403
        return response

    if request.method == "POST":
        # print(f'POST returned from delete with id = {obj.object_id}')  # this happens to be the post id not the comment object so irrelevant
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, 'This has been deleted')
        return HttpResponseRedirect(parent_obj_url)

    context = {
        'object' : obj
    }
    return render(request, 'comment_delete.html', context)

def comment_thread(request,id):
    # print('inside function')
    # obj = get_object_or_404(Comment, id=id) this could be an issue if the wrong id is inserted, make more robust
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent # get the real parent if it not the parent

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
