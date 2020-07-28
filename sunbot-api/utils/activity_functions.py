"""Some helper functions"""

from datetime import datetime, timedelta

from api.models import Activity, Guild

def get_or_init_activity(data):
    try:
        # Find the existing activity entry
        activity = Activity.objects.get(
            guild_id=Guild(guild_id=data["guild_id"]),
            user_id=User(user_id=data["user_id"]),
            period=datetime.now().strftime("%Y-%m-01"),  # The first of the current month
        )
    except ObjectDoesNotExist:
        # Entry not found - create one!
        activity = Activity(
            guild_id=Guild(guild_id=data["guild_id"]),
            user_id=User(user_id=data["user_id"]),
            period=datetime.now().strftime("%Y-%m-01"),  # The first of the current month
        )
    return activity

def add_message_activity(message, guild):
    print("MESSAGE")
    print(message)
    print("GUILD")
    print(guild)
    
    activity = get_or_init_activity(message)

    if all([
        guild.activity_per_message,
        message.words >= guild.activity_min_message_words or message.attachmetns,
        message.channel_id not in guild.activity_channels_x0,
        datetime.now() > activity.last_active + timedelta(seconds=guild.activity_cooldown)
    ]):
        amount = guild.activity_per_message * \
            guild.activity_multi_per_word ** message.words + \
            guild.activity_per_attachment * message.attachmetns
        if message["channel_id"] in guild.activity_channels_x05:
            amount *= 0.5
        elif message["channel_id"] in guild.activity_channels_x2:
            amount *= 2
        activity.activity = amount
        print("ACTIVITY")
        print(activity)
        activity.save()