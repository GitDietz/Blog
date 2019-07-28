from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentManager(models.Manager):
    def filter_by_instance(self, instance): #now no need to specify the model since the instance belongs to a model
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs


class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # post        = models.ForeignKey(Post) #this makes the relation to the posts model, what if it is not related to a post?
    # above now removed to replace with the generic stuff
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')

    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)
