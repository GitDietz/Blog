from datetime import datetime
from django.conf import settings  #needed to get access to user
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from markdown_deux import markdown

from comments.models import Comment

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # below is the same as stating Post.objects.all() = super(PostManager, self).all(). Not anymore it now applies filters
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    # now getting the last id incrementing it
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" % (new_id, filename)


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              height_field='height_field',
                              width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    # first one on initial creation set it, second indicates update each time its saved
    update_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager() # this instanciated the class

    def __str__(self):
        return str(self.id) + ". " + self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})
        # return reverse('detail', kwargs={'id': self.id}) #so it refers to the named pattern 'detail' and passes in the id
        #return '/posts/%s' %(self.id) # works with <a href='{{ obj.get_absolute_url }}'>
        # works with <a href='{% url "detail" id=obj.id %}'>{{ obj.title }}</a> in the template

    class Meta:
        ordering = ["-create_date"] # will govern the sort order

    def get_markdown(self):
        content = self.content
        marked_down = markdown(content)
        return mark_safe(marked_down) # now it is marked safe and the html will be rendered

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None: # handles the case where its not the first call and new_slug exists
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id') # - makes it order in reverse
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id) # this gets the first object from the query set, (the Id property) so the latest
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


# def pre_save_post_receiver(sender, instance,*args, **kwargs):
#     slug = slugify(instance.title)
#     exists = Post.objects.filter(slug=slug).exists() #short for filter the post objects where the slug = this new slug, if there is one that matches return True
#     if exists:
#         slug = "%s-%s" %(slug, instance.id) # mod the slug by appending the "-id" to it
#     instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)
    # sender is the model name

class Robot(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=7)
    job = models.CharField(max_length=300)
    create_date = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.name + ' : ' + self.number

    def get_absolute_url(self):
        return reverse('robot_detail', kwargs={'id': self.id})
