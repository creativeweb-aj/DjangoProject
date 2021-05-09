from django.db import models
from DjangoProject.settings import *
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Post(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Created By', related_name='Post_Created_By_user',
                                   on_delete=models.SET_NULL, null=True)
    title = models.CharField(verbose_name='Post Title', max_length=255, null=True)
    # tagged = models.ManyToManyField(AUTH_USER_MODEL, verbose_name='Tagged User', related_name='Tags')
    content = models.TextField(verbose_name='Post Content', null=True)
    post_image = models.ImageField(upload_to='posts/%d-%m-%y/', null=True)
    # hash_tag = models.CharField(verbose_name='Hash Tags', max_length=255, null=True)
    like = models.ManyToManyField(AUTH_USER_MODEL, verbose_name='Post Likes', related_name='Likes')
    comment = models.ManyToManyField(AUTH_USER_MODEL, verbose_name='Post Comments', related_name='Comments')
    created_on = models.BigIntegerField(verbose_name='Post Created Time', blank=True, null=True)
    updated_on = models.BigIntegerField(verbose_name='Post Updated Time', blank=True, null=True)
    is_delete = models.BooleanField(verbose_name='Deleted', default=False, null=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, verbose_name='User Id', related_name='User_Like',
                                on_delete=models.SET_NULL, null=True)
    post_id = models.ForeignKey(Post, verbose_name='Post Id', related_name='Post_Like',
                                on_delete=models.SET_NULL, null=True)


class Comment(MPTTModel):
    user_id = models.ForeignKey(AUTH_USER_MODEL, verbose_name='User Id', related_name='User_Comment',
                                on_delete=models.SET_NULL, null=True)
    post_id = models.ForeignKey(Post, verbose_name='Post Id', related_name='Post_Comment',
                                on_delete=models.SET_NULL, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = models.TextField(verbose_name='Post Comment', null=True)
    created_on = models.BigIntegerField(verbose_name='Comment Created Time', blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['created_on']
