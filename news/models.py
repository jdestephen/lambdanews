from django.db import models

# Create your models here.
class SubmissionManager(models.Manager):
    
    def popular(self):
        return sorted(models.Manager.get_query_set(self).all(), key=lambda x: x.points)


class Submission(models.Model):
    GRAVITY = 1.8

    objects = SubmissionManager()

    title = models.CharField(max_length=240)

    url = models.URLField(verify_exists=True, blank=True, default="")
    text = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=1)

    def upvote(self):
        self.upvotes += 1
        self.save()

    def points(self):
        from datetime import datetime, timedelta
        from future import __division__
        age = (datetime.now() - self.created_at).seconds / 3600
        return (self.upvotes-1) / (age+2)**Entry.GRAVITY
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('show', [self.pk])  

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    text = models.TextField()
    last_modified = models.DateTimeField(auto_now = True)
    submission = models.ForeignKey(Submission, null=True, blank=True, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies')

    @models.permalink
    def get_absolute_url(self):
        return ('reply_to_comment', [self.pk]) 

    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ['-last_modified']
