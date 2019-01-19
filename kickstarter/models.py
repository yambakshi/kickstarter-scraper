from django.db import models


class PopularCampaign(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.CharField(max_length=400, blank=True, null=True)
    backers = models.IntegerField(default=0, blank=True, null=True)    
    pledged = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
