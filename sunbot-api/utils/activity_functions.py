"""Some helper functions"""

from datetime import datetime, timedelta, timezone

from django.core.exceptions import ObjectDoesNotExist

from api.models import Activity, Guild, User

def get_or_init_activity(data):
    try:
        # Find the existing activity entry
        activity = Activity.objects.get(
            guild_id=Guild(guild_id=data["guild_id"]),
            user_id=User(user_id=data.get("user_id", data.get("giver_id"))),
            period=datetime.now().strftime("%Y-%m-01"),  # The first of the current month
        )
    except ObjectDoesNotExist:
        # Entry not found - create one!
        activity = Activity(
            guild_id=Guild(guild_id=data["guild_id"]),
            user_id=User(user_id=data.get("user_id", data.get("giver_id"))),
            period=datetime.now().strftime("%Y-%m-01"),  # The first of the current month
        )
    return activity

def add_message_activity(message, guild):  
    activity = get_or_init_activity(message)
    if datetime.now(tz=timezone.utc) >= (activity.last_active or \
        datetime.strptime("01-01-2000 +0000", "%d-%m-%Y %z") + \
        timedelta(seconds=guild.activity_cooldown or 0)) and \
        message["channel_id"] not in guild.activity_channels_x0:

        amount = 0
        if guild.activity_per_message and \
            message["words"] >= guild.activity_min_message_words:

            amount += guild.activity_per_message * \
<<<<<<< HEAD
                guild.activity_multi_per_word ** \
                (message["words"] - guild.activity_min_message_words)
=======
                guild.activity_multi_per_word * message["words"]
>>>>>>> 7cb2b45e782a947d69c8a445b7f08d18c2a99fef
        if message["attachments"] and guild.activity_per_attachment:
            amount += guild.activity_per_attachment * message["attachments"]
        if message["channel_id"] in guild.activity_channels_x05:
            amount *= 0.5
        elif message["channel_id"] in guild.activity_channels_x2:
            amount *= 2
        activity.activity += amount
        if activity.activity:
            activity.save()
            
def add_reaction_activity(reaction, guild):    
    if not guild.activity_per_reaction:
        return
    activity = get_or_init_activity(reaction)
    if datetime.now(tz=timezone.utc) >= (activity.last_active or \
        datetime.strptime("01-01-2000 +0000", "%d-%m-%Y %z") + \
        timedelta(seconds=guild.activity_cooldown or 0)):

        activity.activity += guild.activity_per_reaction 
        if activity.activity:
            activity.save()
            
def add_voice_activity(voice, guild):    
    if not guild.activity_per_voice_minute:
        return
    activity = get_or_init_activity(voice)
    if datetime.now(tz=timezone.utc) >= (activity.last_active or \
        datetime.strptime("01-01-2000 +0000", "%d-%m-%Y %z") + \
        timedelta(seconds=guild.activity_cooldown or 0)):

        activity.activity += guild.activity_per_voice_minute * \
            guild.activity_multi_per_voice_member * (voice["members"] - 1)
        if activity.activity:
            activity.save()