from django.db import models

# Create your models here.


class ScoreTable(models.Model):
    """项目类型表"""
    id = models.AutoField(primary_key=True)
    client = models.CharField(verbose_name='客户端', max_length=100)
    score = models.IntegerField(verbose_name='分数')
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-score',)
        verbose_name = '排名'
        verbose_name_plural = '排名'