# sunbot-python

My own Discord bot, the client part. It's written in Python.

## Commands

### General

#### <prefix> reload <cog name>

Reloads the selected cog. 

Requires: bot owner.

### Moderation Settings

#### <prefix> setmodrole <role ping or ID>

Sets the moderator role. Pass no arguments to reset it.

#### <prefix> setmuterole <role ping or ID> <optional "makemute">

Sets the muted role. Pass no arguments to reset it. Add "makemute" to mute the selected role in all channels.

### Misc

#### <prefix> ping

Replies with the bot latency. Tiny command that lets you check if the bot is up.
