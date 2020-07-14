"""Database models for automatic mgration.

TODO! When Django starts supporting composite primary keys, 
rewrite them properly!"""

from django.db import models


class User(models.Model):
    """User model."""
    user_id = models.BigIntegerField(primary_key=True)
    birthday = models.DateField(null=True, blank=True)
    steam = models.URLField(max_length=80, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    ign_ddo = models.CharField(max_length=50, null=True, blank=True)
    ign_warframe_pc = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return str(self.user_id)
    
    class Meta:
        db_table = "users"


class Messages(models.Model):
    """Info about user's posts - where and how much."""
    guild_id = models.BigIntegerField()
    channel_id = models.BigIntegerField()
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="messages", 
        db_column="user_id", # Django adds second "_id" otherwise
    )
    period = models.DateField()
    postcount = models.IntegerField(default=0,)
    attachments = models.IntegerField(default=0,)
    words = models.IntegerField(default=0,)

    def __str__(self):
        return f"{self.guild_id}/{self.channel_id} by {self.user_id} for {self.period}"
        
    class Meta:
        db_table = "messages"
        # Composite primary key workaround
        unique_together = [["guild_id", "channel_id", "user_id", "period"]]