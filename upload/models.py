# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)





class Feedback(models.Model):

	feedback = models.CharField(max_length=200)


class VideoEntry(models.Model):

	username = models.CharField(max_length=32)
	videoUploaded = models.CharField(max_length=50)
	feedback = models.ManyToManyField(Feedback)
	processedVideoPath = models.CharField(max_length=300,default='') #to store the OP processed vídeo




