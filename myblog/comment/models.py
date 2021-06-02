from django.db import models
from django.db.models.deletion import CASCADE

from blog.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    target = models.ForeignKey(Post, CASCADE, verbose_name='评论目标')
    content = models.CharField('内容', max_length=2000)
    nickname = models.CharField('昵称', max_length=50)
    website = models.URLField('网站')
    email = models.EmailField('邮箱')
    status = models.PositiveIntegerField(
        '状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return self.target