import discord
from discord.ext import commands

import json
from random import choice, randint, seed

from datetime import datetime, timedelta

class Oracle(commands.Cog):
       
    def __init__(self, bot):
        self.bot = bot
        self.no_question = [
            "What the fuck do you want?", "Hm?", "Are you mute?", "Um, what?",
            "Come on, you didn't ask anything", "What do you want to know?",
            "Ask your questions", "Huh?", "I'm listening", "Ask away", "Yes?", 
        ]
        self.no_mark = [
            "Is this a question?", "Is this a statement?", 
            "Learn to use question marks, you stupid bitch", 
            "Ever heard about question marks?", "It's not a question", 
            "Questions are usually marked with question marks", 
        ]
        self.rude = [
            "I'm a fucking bot, how am I supposed to know? Really, the answers are just random, what the fuck do you expect?", 
            "I don't fucking know mate", "Fuck you", "Ask your mom", "Piss off", 
            "Fuck you and your fucking questions", "Don't bother me", 
            "Shut the fuck up", 
        ]
        self.rude_triggers = [
            "Updog", "Joe", "Ligma", "Yuri",
        ]
        self.unclear = [
            "Reply hazy, try again", "Ask again later", "Cannot predict now", 
            "Better not tell you now", "Concentrate and ask again",
        ]
        self.yes = [
            "It is certain", "It is decidedly so", "Without a doubt", "Yep", 
            "Yes - definitely", "You may rely on it", "As I see it, yes", 
            "Most likely", "Outlook good", "Yes", "Signs point to yes", "Yeah", 
            "Of course", "Sure",
        ]
        self.no = [
            "Don't count on it", "My reply is no", "My sources say no", 
            "Outlook not so good", "Very doubtful", "No", "Nope", "No way"
        ]
        self.who = [
            "My sources say NAME", "Certainly, it's NAME", "NAME, probably", 
            "As far as I know, NAME", "NAME", "Must be NAME", 
            "All signs point to NAME", "What if I told you it's NAME?", 
            "My guess is NAME", "I'm rather sure it's NAME", "You", "Your mom", 
            "Me", "No one"]
        self.when_future = [
            "Today", "Tomorrow", "Never", "Soon", "On your next birthday", 
            "In a few days", "In a week", "In a couple of weeks", "In a month", 
            "In a few months", "In a year", "In a few years", 
            "When you get old", "When you die"]
        self.when_past = [
            "Today", "Yesterday", "Never", "A day ago", "A couple of days ago", 
            "A week ago", "A few weeks ago", "Month ago", 
            "A couple of months ago", "A year ago", "A few years ago", 
            "When the Universe was born", "On the seventh day"
        ]
        self.rate = [
            "I rate it GRADE", "It's GRADE", "GRADE", "GRADE, would rate again", 
            "GRADE and don't ask me again about this", "Fucking GRADE",
            "Fucking legendary", "Utter shit",
        ]
        self.why = [
            "Because God wanted it to be that way", "To reach enlightenment",
            "Because reasons", "There's absolutely no reason for that", 
            "To make me feel good", "For all the good reasons", "Why not?"
            "To make this world a better place", "Because fuck you, that's why", 
            "Because you're gay", "It was a good day for that", 
            "What are you talking about? It never happened",
        ]
        self.suggest = [
            "How about **ITEM**", "Maybe you'd like **ITEM**", "I suggest **ITEM**", 
            "**ITEM** is worth your attention", "You definitely should check **ITEM**",
        ]
        
        self.iq_range = [100] * 46
        for i in range(1, 46):
            self.iq_range += [100-j for j in range(1, i)]
            self.iq_range += [100+j for j in range(1, i)]

    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.web.get(
            'https://www.randomlists.com/data/recipes.json'
        ) as raw_recipes:   
            recipes = await raw_recipes.json(content_type=None)
        self.recipes = recipes["data"]
        async with self.bot.web.get(
            'https://pokeapi.co/api/v2/pokemon/?limit=1000'
        ) as raw_pokemons:   
            pokemons = await raw_pokemons.json(content_type=None)
        self.pokemons = pokemons["results"]

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.member)
    @commands.command(aliases=["8", "8ball", "o"]) 
    async def oracle(self, ctx, *, question=None):
        embed = discord.Embed(title="🔮 Oracle 🔮", color=ctx.author.color)
        # Refreshing random seed
        seed()
        # Preparing the question 
        parsed_question = question.lower().rstrip("?").split()
        parsed_question = [
            i if i not in ("i", "me", "my") 
            else ctx.author.mention for i in parsed_question
        ]
        parsed_question = [
            i if i  != 'now' 
            else str(datetime.utcnow().timestamp()) for i in parsed_question
        ]
        parsed_question = [
            i if i  != 'yesterday' else str(
                (datetime.utcnow() - timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                ).timestamp()) for i in parsed_question
        ]
        parsed_question = [
            i if i  != 'today' else str(
                (datetime.utcnow() + timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                ).timestamp()) for i in parsed_question
        ]
        parsed_question = [
            i if i  != 'tomorrow' else str(datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            ).timestamp()) for i in parsed_question
        ]
        parsed_question = ' '.join(parsed_question)

        clear = randint(0,30)
        polite = randint(0,100)
        # No question case
        if not parsed_question: 
            reply = choice(self.no_question)
        # No question mark case
        elif all((
            question[-1] != '?', 
            not parsed_question.startswith("rate"), 
            not parsed_question.startswith("suggest")
        )): 
            reply = choice(self.no_mark)
        # Unclear case
        elif not clear:
            reply = choice(self.unclear)
        # Rude case
        elif not polite: 
            reply = choice(self.rude + self.rude_triggers)
        # Special cases
        elif any((i in parsed_question for i in (
            "you're gay", "youre gay", "you gay", "you are gay", "suck dick", 
            "suck my dick", "you have autism"
        ))):
            reply = "Fuck you, you stupid bitch ass motherfucker, I wish I had arms so I could strangle you"
        elif parsed_question in (
            "who's joe", "whos joe", "who joe", "joe who",  "who is joe", "joe"
        ): 
            reply = "Joe mama"
        elif parsed_question in (
            "what's updog", "what is updog", "what updog", "updog"
        ): 
            reply = "Not much, you?"
        elif parsed_question in (
            "what's ligma", "what is ligma", "what ligma", "ligma"
        ): 
            reply = "Ligma balls"
        elif parsed_question in (
            "who's yuri", "whos yuri", "who yuri", 
            "yuri who", "who is yuri", "yuri"
        ): 
            reply = "Yuri Tarded"
        # Normal questions
        else: 
            seed(parsed_question)
            # Or questions
            if "or" in parsed_question.split():
                or_question = question.rstrip("?").lower()
                or_question = or_question.replace("am i", "you are")
                or_question = or_question.replace("i am", "you are")
                or_question = or_question.replace("should i", "you should")
                or_question = or_question.split()
                or_question = [
                    i if i not in ('im', "i'm") else "you are" for i in or_question
                ]
                or_question = [
                    i if i.lower() not in ('i', "me") else "you" for i in or_question
                ]
                or_question = [i if i != "my" else "your" for i in or_question]
                or_question = " ".join(or_question)
                variants = or_question.split(" or ")
                reply = choice(variants).capitalize()
            # IQ 
            elif 'iq' in parsed_question.split(): 
                reply = str(choice(self.iq_range))
            # Who questions
            elif parsed_question.startswith("who"): 
                # TODO Choose from a pool of active members
                # if self.bot.settings.get(ctx.guild.id, {}).get("track_messages"):
                members = [m for m in ctx.guild.members if not m.bot]
                who = choice(members)
                reply = choice(self.who).replace("NAME", f"**{who.display_name}**")
            # When questions
            elif parsed_question.startswith("when"): 
                # TODO Add different time ranges
                approximate = randint(0,4)
                if any((
                    i in parsed_question.split() for i in (
                        'was', 'did', 'were', 'have', 'had'
                    )
                )):
                    if approximate:
                        reply = choice(self.when_past)
                    else:
                        date = datetime.utcnow() - timedelta(days=randint(0,365*1000))
                        reply = date.strftime("%d %B %Y")
                else:
                    if approximate:
                        reply = choice(self.when_future)
                    else:
                        date = datetime.utcnow() + timedelta(days=randint(0,365*20))
                        reply = date.strftime("%d %B %Y")
            # Rate questions
            elif any((parsed_question.startswith(i) for i in (
                "rate", "how gay", "how much", "how nice", "how good", "how bad",
            ))): 
                grade = f"**{randint(1,10)}/10**"
                reply = choice(self.rate).replace("GRADE", grade)
            # Suggest
            elif parsed_question.startswith("suggest"): 
                # Food
                if any((
                    " eat" in parsed_question, 
                    " cook" in parsed_question,
                    " food" in parsed_question,
                    " recipe" in parsed_question,
                )):
                    dish = choice(self.recipes)
                    reply = choice(self.suggest).replace('ITEM', dish['t'])
                    reply += f"\n{dish['u']}"
                    embed.set_image(url=f"https://www.randomlists.com/{dish['i']}")
                else:
                    reply = 'There are no `suggest` replies for this topic yet.'
                # Game
                """
                elif " game" in parsed_question or " play" in parsed_question:
                    games = await get_games(self.bot.db)
                    reply = f"{choice(self.suggest)} **{choice(games)[0]}**"
                """
                    
            # What/which questions
            elif parsed_question.startswith("what") or parsed_question.startswith("which"): 
                # Food
                if any((
                    " eat" in parsed_question, 
                    " cook" in parsed_question,
                    " food" in parsed_question,
                    " recipe" in parsed_question,
                )):
                    dish = choice(self.recipes)
                    reply = choice(self.suggest).replace('ITEM', dish['t'])
                    reply += f"\n{dish['u']}"
                    embed.set_image(url=f"https://www.randomlists.com/{dish['i']}")
                # Pokemon                
                elif "pokemon" in parsed_question:
                    if not hasattr(self, "pokemons"):
                        async with self.bot.web.get(
                            'https://pokeapi.co/api/v2/pokemon/?limit=1000'
                        ) as raw_pokemons:   
                            pokemons = await raw_pokemons.json(content_type=None)
                        self.pokemons = pokemons["results"]
                    pokemon = choice(self.pokemons)
                    reply = f"**{pokemon['name'].capitalize()}**"
                    async with self.bot.web.get(pokemon["url"]) as raw_pokemon:   
                        pokemon = await raw_pokemon.json(content_type=None)
                    image = pokemon["sprites"].get("front_default")
                    if image:
                        embed.set_thumbnail(url=image)
                else:
                    reply = 'There are no `what` replies for this topic yet.'
            # How questions
            elif parsed_question.startswith("how"): 
                reply = 'There are no "how" replies in the bank yet'
            # Why questions
            elif parsed_question.startswith("why"): 
                reply = choice(self.why)
            # Yes or no question
            else: 
                good = randint(0,1)
                if good:
                    reply = choice(self.yes)
                else:
                    reply = choice(self.no)
        embed.add_field(
            name='The Question', 
            value=question[0].upper()+question[1:],
            inline=False
        )
        embed.add_field(
            name='The Answer', 
            value=reply,
            inline=False
        )
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Oracle(bot))