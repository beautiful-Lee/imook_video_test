# coding: utf-8

from enum import Enum
from django.db import models


class VideoType(Enum):
    cold = 'cold'
    life = 'life'
    cartoon = 'cartoon'
    movie = 'movie'
    other = 'other'


VideoType.cold.label = '搞笑'
VideoType.life.label = '生活'
VideoType.cartoon.label = '卡通动漫'
VideoType.movie.label = '影视'
VideoType.other.label = '其他'


class FromType(Enum):
    youku = 'youku'
    custom = 'custom'


FromType.youku.label = '优酷'
FromType.custom.label = '自定义'


class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'


NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国'
NationalityType.other.label = '其他'


class IdentityType(Enum):
    starring = 'starring'
    director = 'director'
    costar = 'costar'


IdentityType.starring.label = '主演'
IdentityType.director.label = '导演'
IdentityType.costar.label = '配角'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=26, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'nationality')

    def __str__(self):
        return self.name


class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=200, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return "video : {0}, numebr : {1}".format(self.video.name, self.number)
