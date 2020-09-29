from django.db import models
from django.conf import settings
import random
# Create your models here
User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    parent = models.ForeignKey('self',null=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,blank=True)#through=TweetLike)#one user to many tweets
    likes = models.ManyToManyField(User,related_name='tweet_user',blank=True)
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to ='images/',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
    # def __str__(self):
    #     return self.content


    @property
    def is_retweet(self):
        return self.parent != None


        
    def serialize(self):
        '''
        feel free to delete
        '''

        return {
            'id':self.id,
            'content':self.content,
            'likes':random.randint(0,200)
        }




