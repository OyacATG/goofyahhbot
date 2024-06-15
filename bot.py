import random
import nextcord
from nextcord.ext import commands
import datetime
import arrow
import re

# Bot setup
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Starting Character ID
character_id = 23

# Database for characters
characters = {}

# Custom emoji IDs
emoji_ids = {
    'Martial': '<:martial:1249437145979031745>',
    'Learning': '<:learning:1249437142233645198>',
    'Diplomacy': '<:diplomacy:1249437140300075049>',
    'Stewardship': '<:stewardship:1249437144146247741>',
    'Prowess': '<:prowess:1249437138861424741>',
    'Intrigue': '<:intrigue:1249439175871168555>'
}

# Default image URL
default_image_url = "https://cdn.discordapp.com/attachments/1249438918466863235/1249444370633986169/LifeInvader_GTAV_Lester_Profile_large.png?ex=6667533f&is=666601bf&hm=56c96568b38a1be705e659005358c342c619086b0ef1367968de5aa9cce71057&"

# Traits and effects
personality_traits = [
    "Ambitious", "Lazy", "Charismatic", "Just", "Arbitrary", "Patient", "Wroth", 
    "Honest", "Deceitful", "Brave", "Craven", "Diligent", "Slothful", "Greedy", 
    "Generous", "Proud", "Humble", "Lustful", "Chaste", "Temperate", "Gluttonous", 
    "Kind", "Cruel", "Shy", "Gregarious", "Zealous", "Cynical", "Paranoid", 
    "Trusting", "Ambitious", "Content", "Arrogant", "Modest", "Eloquent", 
    "Stubborn", "Cautious", "Reckless", "Wise", "Foolhardy", "Sympathetic", 
    "Callous", "Idealistic", "Realistic", "Forgiving", "Vindictive", "Diplomatic", "Blunt"
]

physical_traits = {
    "Blind": {"Martial": -40, "Diplomacy": -20, "description": "Severely reduces ability in Martial (-40) and Diplomacy (-20) due to lack of sight."},
    "Deaf": {"Diplomacy": -30, "Intrigue": -10, "description": "Reduces ability in Diplomacy (-30) and Intrigue (-10) due to inability to hear."},
    "Lame": {"Prowess": -30, "Martial": -10, "description": "Reduces Prowess (-30) and Martial (-10) due to difficulty in movement."},
    "Mute": {"Diplomacy": -50, "description": "Severely reduces ability in Diplomacy (-50) due to inability to speak."},
    "One-eyed": {"Martial": -20, "Prowess": -10, "description": "Reduces Martial (-20) and Prowess (-10) due to limited vision."},
    "Scarred": {"Diplomacy": -10, "Prowess": +10, "description": "Reduces Diplomacy (-10) but increases Prowess (+10) due to battle experience."},
    "Clubfooted": {"Prowess": -20, "Martial": -10, "description": "Reduces Prowess (-20) and Martial (-10) due to difficulty in movement."},
    "Hunchback": {"Prowess": -20, "Diplomacy": -20, "description": "Reduces Prowess (-20) and Diplomacy (-20) due to physical deformity."},
    "Albino": {"Diplomacy": -10, "Intrigue": +10, "description": "Reduces Diplomacy (-10) but increases Intrigue (+10) due to unique appearance."},
    "Dwarf": {"Prowess": -30, "Diplomacy": -10, "description": "Reduces Prowess (-30) and Diplomacy (-10) due to short stature."},
    "Giant": {"Prowess": +30, "Diplomacy": -20, "description": "Increases Prowess (+30) but reduces Diplomacy (-20) due to intimidating size."},
    "Obese": {"Prowess": -40, "Martial": -10, "Lifespan": -20, "description": "Severely reduces Prowess (-40) and Martial (-10) due to excessive weight, and lifespan by 20 years."},
    "Anemic": {"Prowess": -20, "Stewardship": -10, "description": "Reduces Prowess (-20) and Stewardship (-10) due to low energy levels."},
    "Paraplegic": {"Martial": -50, "Prowess": -50, "description": "Severely reduces Martial (-50) and Prowess (-50) due to paralysis of the lower body."},
    "Epileptic": {"Learning": -10, "Intrigue": -10, "description": "Reduces Learning (-10) and Intrigue (-10) due to unpredictable seizures."},
    "Leper": {"Diplomacy": -40, "Prowess": -20, "Lifespan": -40, "description": "Severely reduces Diplomacy (-40) and Prowess (-20) due to visible skin disease, and lifespan by 40 years."},
    "Hemophiliac": {"Prowess": -30, "Lifespan": -10, "description": "Reduces Prowess (-30) due to excessive bleeding from minor injuries, and lifespan by 10 years."},
    "Stutter": {"Diplomacy": -20, "Learning": -10, "description": "Reduces Diplomacy (-20) and Learning (-10) due to speech impediment."},
    "Tourette": {"Intrigue": -20, "Diplomacy": -10, "description": "Reduces Intrigue (-20) and Diplomacy (-10) due to involuntary outbursts."},
    "Amputee": {"Prowess": -30, "Martial": -10, "description": "Reduces Prowess (-30) and Martial (-10) due to loss of limb."},
    "Asthmatic": {"Prowess": -20, "Martial": -10, "description": "Reduces Prowess (-20) and Martial (-10) due to breathing difficulties."},
    "Chronic Pain": {"Prowess": -20, "Learning": -10, "description": "Reduces Prowess (-20) and Learning (-10) due to persistent pain."},
    "Psoriatic": {"Diplomacy": -10, "Intrigue": +5, "description": "Reduces Diplomacy (-10) but increases Intrigue (+5) due to unique skin condition."},
    "Diabetic": {"Stewardship": -10, "Lifespan": -20, "description": "Reduces Stewardship (-10) and lifespan by 20 years due to managing chronic illness."},
    "Arthritic": {"Prowess": -30, "Martial": -10, "description": "Reduces Prowess (-30) and Martial (-10) due to joint pain and stiffness."},
    "Migraine": {"Learning": -20, "Intrigue": -10, "description": "Reduces Learning (-20) and Intrigue (-10) due to severe headaches."},
    "Strong": {"Prowess": +20, "Martial": +10, "description": "Increases Prowess (+20) and Martial (+10) due to physical strength."},
    "Healthy": {"Lifespan": +20, "description": "Increases lifespan by 20 years due to robust health."},
    "Gifted": {"Learning": +10, "Intrigue": +10, "description": "Increases Learning (+10) and Intrigue (+10) due to quick thinking."},
    "Attractive": {"Diplomacy": +20, "Intrigue": +5, "description": "Increases Diplomacy (+20) and Intrigue (+5) due to appealing appearance."},
    "Brawny": {"Prowess": +20, "description": "Increases Prowess (+20) due to muscular build."},
    "Extremely Gifted": {"Learning": +20, "description": "Increases Learning (+20) due to exceptional intellect."},
    "Agile": {"Prowess": +10, "Intrigue": +10, "description": "Increases Prowess (+10) and Intrigue (+10) due to nimbleness."},
    "Hardy": {"Martial": +10, "Prowess": +10, "description": "Increases Martial (+10) and Prowess (+10) due to resilience."},
    "Tall": {"Prowess": +10, "Diplomacy": +5, "description": "Increases Prowess (+10) and Diplomacy (+5) due to impressive height."},
    "Charismatic": {"Diplomacy": +20, "description": "Increases Diplomacy (+20) due to charm and persuasiveness."}
}

# Helper functions
def roll_stat():
    return random.randint(0, 100)

def roll_fertility():
    return random.randint(1, 6)

def get_stat_role(stat, category):
    categories = {
        "Martial": [
            (0, 10, ["Burden"]),
            (11, 20, ["Novice Fighter"]),
            (21, 30, ["Apprentice", "Water Apprentice", "Raider", "Inspiration"]),
            (31, 40, ["Basic Tactician"]),
            (41, 50, ["Competent General"]),
            (51, 60, ["Improving Apprentice", "Improving Water Apprentice", "Water Enjoyer"]),
            (61, 70, ["Trained General", "Trained Admiral"]),
            (71, 80, ["Army General"]),
            (81, 90, ["Veteran Commander"]),
            (91, 97, ["General of a Decade", "Admiral of a Decade"]),
            (97, 100, ["General of an Age", "Admiral of an Age", "Froggy Boy"])
        ],
        "Stewardship": [
            (0, 10, ["Incompetent Ruler"]),
            (11, 20, ["Inept Steward"]),
            (21, 30, ["Mediocre Steward"]),
            (31, 40, ["Basic Administrator"]),
            (41, 50, ["Capable Manager"]),
            (51, 60, ["Competent Ruler"]),
            (61, 70, ["Skilled Steward"]),
            (71, 80, ["Efficient Administrator"]),
            (81, 90, ["Master Steward"]),
            (91, 100, ["Administrative Genius"])
        ],
        "Learning": [
            (0, 10, ["Imbecile"]),
            (11, 20, ["Simpleton"]),
            (21, 30, ["Slow"]),
            (31, 40, ["Average Thinker"]),
            (41, 50, ["Adequate Learner"]),
            (51, 60, ["N/A"]),
            (61, 70, ["Quick Learner"]),
            (71, 80, ["Theologian"]),
            (81, 90, ["Scholarly Mind"]),
            (91, 96, ["Quick"]),
            (97, 100, ["Genius", "Inventor"])
        ],
        "Diplomacy": [
            (0, 10, ["Mute"]),
            (11, 20, ["Poor Communicator"]),
            (21, 30, ["Determined Peacemaker", "Ineffective Diplomat"]),
            (31, 40, ["Basic Negotiator"]),
            (41, 50, ["Average Negotiator"]),
            (51, 60, ["Ambitious", "Culture Student", "Capable Diplomat"]),
            (61, 70, ["Skilled Negotiator", "Diplomatic Envoy"]),
            (71, 80, ["Experienced Diplomat", "Cultural Envoy"]),
            (81, 90, ["Culture Master", "Insanely Good Peacemaker", "Master Negotiator"]),
            (91, 100, ["Master Diplomat", "Grand Ambassador"])
        ],
        "Intrigue": [
            (0, 10, ["Incapable Schemer", "Blundering Plotter"]),
            (11, 20, ["Novice Plotter", "Amateur Conspirator"]),
            (21, 30, ["Slightly Capable Schemer", "Aspiring Intriguer"]),
            (31, 40, ["Basic Schemer", "Cunning Plotter"]),
            (41, 50, ["Competent Schemer", "Devious Manipulator"]),
            (51, 60, ["Masterful Schemer", "Skilled Conspirator"]),
            (61, 70, ["Expert Schemer", "Shadow Operator"]),
            (71, 80, ["Mastermind Schemer", "Grand Deceiver"]),
            (81, 90, ["Elite Intriguer", "Master of Espionage"]),
            (91, 100, ["Shadow Master", "Supreme Schemer"])
        ],
        "Prowess": [
            (0, 10, ["Incompetent Dueler", "Weak Fighter", "Clumsy Combatant"]),
            (11, 20, ["Novice Duelist", "Handslicing Maniac", "Inept Warrior"]),
            (21, 30, ["Basic Fighter", "Average Duelist", "Beginner Swordsman"]),
            (31, 40, ["Competent Dueler", "Headroller", "Adept Swordsman"]),
            (41, 50, ["Skilled Fighter", "Duelist", "Battlefield Warrior"]),
            (51, 60, ["Expert Duelist", "Master Swordsman", "Combat Veteran"]),
            (61, 70, ["Elite Warrior", "Strong Man", "Master Duelist"]),
            (71, 80, ["Legendary Fighter", "Grand Duelist", "Champion"]),
            (81, 90, ["Supreme Duelist", "Heroic Warrior", "Grandmaster Duelist"]),
            (91, 100, ["Prowess Master", "Combat Legend", "Ultimate Duelist"])
        ]
    }

    for range_min, range_max, roles in categories[category]:
        if range_min <= stat <= range_max:
            return f"({stat}) {random.choice(roles)}"
    return f"({stat}) Unknown"

def roll_lifespan():
    return random.randint(20, 80)

def calculate_death_year(birth_year, lifespan):
    return birth_year + lifespan

# Function to get the relative date
def get_relative_date():
    now = arrow.utcnow().to('local')
    if now.date() == (now - datetime.timedelta(days=1)).date():
        return "Yesterday"
    elif now.date() == (now + datetime.timedelta(days=1)).date():
        return "Tomorrow"
    else:
        return "Today"

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Apply traits to stats
def apply_traits(stats, traits):
    trait_descriptions = []
    lifespan_adjustment = 0
    for trait in traits:
        if trait in personality_traits:
            # Personality traits do not affect stats
            trait_descriptions.append(trait)
        elif trait in physical_traits:
            for key, value in physical_traits[trait].items():
                if key == "Lifespan":
                    lifespan_adjustment += value
                elif key != "description":
                    stats[key] = max(0, stats[key] + value)
            trait_descriptions.append(f"{trait}: {physical_traits[trait]['description']}")
    return stats, trait_descriptions, lifespan_adjustment

# Determine sexuality
def determine_sexuality():
    roll = random.random()
    if roll < 0.002:
        return "Asexual"
    elif roll < 0.012:
        return "Bisexual"
    elif roll < 0.062:
        return "Homosexual"
    else:
        return "Heterosexual"

# Event to set the bot's status
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name="Risk Universalis"))
    print(f'Logged in as {bot.user}')

# Helper function to roll for physical traits based on given probabilities
def roll_physical_trait():
    roll = random.random()
    if roll < 0.75:
        return None
    elif roll < 0.85:
        # Choose a good physical trait
        good_traits = [trait for trait, effects in physical_traits.items() if any(value > 0 for key, value in effects.items() if key != 'description')]
        return random.choice(good_traits)
    else:
        # Choose a bad physical trait
        bad_traits = [trait for trait, effects in physical_traits.items() if all(value <= 0 for key, value in effects.items() if key != 'description')]
        return random.choice(bad_traits)

# Add Historical Character Command
@bot.slash_command(name="addhistorical", description="Add a historical character")
async def add_historical(interaction: nextcord.Interaction, name: str, dynasty: str, birthyear: int, deathyear: int, titles: str, biography: str):
    global character_id

    character = {
        'ID': character_id,
        'Name': name,
        'Gender': 'Unknown',
        'Parents': 'Unknown',
        'Lifespan': deathyear - birthyear,
        'Birth Year': birthyear,
        'Death Year': deathyear,
        'Dynasty': dynasty,
        'Fertility': roll_fertility(),
        'Owner': interaction.user.id,
        'Children': [],
        'Image': default_image_url,
        'Titles': titles,
        'Biography': biography,
        'Sexuality': determine_sexuality()
    }
    characters[character_id] = character
    character_id += 1

    current_time = arrow.utcnow().to('local').format('h:mm A')
    relative_date = get_relative_date()

    embed = nextcord.Embed(title=character['Name'], description=character['Biography'], color=nextcord.Color.gold())
    embed.add_field(name="Dynasty", value=character['Dynasty'], inline=False)
    embed.add_field(name="Titles", value=character['Titles'], inline=False)
    embed.add_field(name="Lifetime", value=f"{character['Birth Year']} - {character['Death Year']} ({character['Lifespan']} years)", inline=False)
    embed.add_field(name="Parents", value=character['Parents'], inline=False)
    embed.add_field(name="Gender", value=character['Gender'], inline=True)
    embed.add_field(name="Sexuality", value="Heterosexual", inline=True)
    embed.set_image(url=character['Image'])
    embed.set_footer(text=f"ID: {character['ID']} | {relative_date}, {current_time}")

    channel = nextcord.utils.get(interaction.guild.channels, name="🧺-characters")
    if channel:
        message = await channel.send(embed=embed)
        character['Message Link'] = message.jump_url
        await interaction.response.send_message(f"Historical character {character['Name']} added and sent to {channel.mention}")
    else:
        await interaction.response.send_message("Channel 🧺-characters not found.")

# Create Character Command
@bot.slash_command(name="createcharacter", description="Create a new character")
async def create_character(interaction: nextcord.Interaction, name: str, gender: str, birthyear: int, dynasty: str, titles: str, biography: str):
    global character_id
    lifespan = roll_lifespan()

    stats = {
        'Martial': roll_stat(),
        'Stewardship': roll_stat(),
        'Learning': roll_stat(),
        'Diplomacy': roll_stat(),
        'Intrigue': roll_stat(),
        'Prowess': roll_stat()
    }

    personality_trait = random.choice(personality_traits)
    physical_trait = roll_physical_trait()
    traits = [personality_trait] if not physical_trait else [physical_trait, personality_trait]
    stats, trait_descriptions, lifespan_adjustment = apply_traits(stats, traits)
    lifespan = max(0, lifespan + lifespan_adjustment)
    death_year = birthyear + lifespan

    sexuality = determine_sexuality()

    character = {
        'ID': character_id,
        'Name': name,
        'Gender': gender,
        'Martial': stats['Martial'],
        'Stewardship': stats['Stewardship'],
        'Learning': stats['Learning'],
        'Diplomacy': stats['Diplomacy'],
        'Intrigue': stats['Intrigue'],
        'Prowess': stats['Prowess'],
        'Parents': 'Unknown',
        'Lifespan': lifespan,
        'Birth Year': birthyear,
        'Death Year': death_year,
        'Dynasty': dynasty,
        'Fertility': roll_fertility(),
        'Owner': interaction.user.id,
        'Children': [],
        'Image': default_image_url,
        'Titles': titles,
        'Biography': biography,
        'Traits': traits,
        'Sexuality': sexuality
    }
    characters[character_id] = character
    character_id += 1

    current_time = arrow.utcnow().to('local').format('h:mm A')
    relative_date = get_relative_date()

    embed = nextcord.Embed(title=character['Name'], description=character['Biography'], color=nextcord.Color.blue())
    embed.add_field(name="Dynasty", value=character['Dynasty'], inline=False)
    embed.add_field(name="Titles", value=character['Titles'], inline=False)
    embed.add_field(name="Lifetime", value=f"{character['Birth Year']} - {character['Death Year']} ({character['Lifespan']} years)", inline=False)
    embed.add_field(name="Parents", value=character['Parents'], inline=False)
    embed.add_field(name="Gender", value=character['Gender'], inline=True)
    embed.add_field(name="Sexuality", value=character['Sexuality'], inline=True)
    embed.add_field(name="Stats", value=(
        f"{emoji_ids['Martial']} {get_stat_role(character['Martial'], 'Martial')}\n"
        f"{emoji_ids['Stewardship']} {get_stat_role(character['Stewardship'], 'Stewardship')}\n"
        f"{emoji_ids['Learning']} {get_stat_role(character['Learning'], 'Learning')}\n"
        f"{emoji_ids['Diplomacy']} {get_stat_role(character['Diplomacy'], 'Diplomacy')}\n"
        f"{emoji_ids['Intrigue']} {get_stat_role(character['Intrigue'], 'Intrigue')}\n"
        f"{emoji_ids['Prowess']} {get_stat_role(character['Prowess'], 'Prowess')}"
    ), inline=False)
    embed.add_field(name="Physical Traits", value=trait_descriptions[0] if physical_trait else "None", inline=False)
    embed.add_field(name="Personality Traits", value=trait_descriptions[1] if physical_trait else trait_descriptions[0], inline=False)
    embed.set_image(url=character['Image'])
    embed.set_footer(text=f"ID: {character['ID']} | {relative_date}, {current_time}")

    channel = nextcord.utils.get(interaction.guild.channels, name="🧺-characters")
    if channel:
        message = await channel.send(embed=embed)
        character['Message Link'] = message.jump_url
        await interaction.response.send_message(f"Character {character['Name']} created and sent to {channel.mention}")
    else:
        await interaction.response.send_message("Channel 🧺-characters not found.")

# Fornicate Command
@bot.slash_command(name="fornicate", description="Create a child from two characters")
async def fornicate(interaction: nextcord.Interaction, motherid: int, fatherid: int, name: str, birthyear: int, titles: str, biography: str):
    global character_id
    father = characters.get(fatherid)
    if not father:
        await interaction.response.send_message(f"Father with ID {fatherid} not found.")
        return

    mother = characters.get(motherid)
    if not mother:
        await interaction.response.send_message(f"Mother with ID {motherid} not found.")
        return

    if father['Owner'] != interaction.user.id or mother['Owner'] != interaction.user.id:
        await interaction.response.send_message("You do not own one or both of these characters.")
        return

    if mother['Fertility'] <= 0:
        await interaction.response.send_message("The mother has no remaining fertility points.")
        return

    if father['Fertility'] <= 0:
        await interaction.response.send_message("The father is incapable of producing more children.")
        return

    lifespan = roll_lifespan()

    stats = {
        'Martial': roll_stat(),
        'Stewardship': roll_stat(),
        'Learning': roll_stat(),
        'Diplomacy': roll_stat(),
        'Intrigue': roll_stat(),
        'Prowess': roll_stat()
    }

    personality_trait = random.choice(personality_traits)
    physical_trait = roll_physical_trait()
    traits = [personality_trait] if not physical_trait else [physical_trait, personality_trait]
    stats, trait_descriptions, lifespan_adjustment = apply_traits(stats, traits)
    lifespan = max(0, lifespan + lifespan_adjustment)
    death_year = birthyear + lifespan

    child_character = {
        'ID': character_id,
        'Name': name,
        'Gender': random.choice(['Male', 'Female']),
        'Martial': stats['Martial'],
        'Stewardship': stats['Stewardship'],
        'Learning': stats['Learning'],
        'Diplomacy': stats['Diplomacy'],
        'Intrigue': stats['Intrigue'],
        'Prowess': stats['Prowess'],
        'Parents': f"[{mother['Name']}]({mother['Message Link']}) and [{father['Name']}]({father['Message Link']})",
        'Lifespan': lifespan,
        'Birth Year': birthyear,
        'Death Year': death_year,
        'Dynasty': father['Dynasty'],
        'Fertility': roll_fertility(),
        'Owner': interaction.user.id,
        'Children': [],
        'Image': default_image_url,
        'Titles': titles,
        'Biography': biography,
        'Traits': traits,
        'Sexuality': determine_sexuality()
    }
    characters[character_id] = child_character
    character_id += 1

    father['Fertility'] -= 1
    mother['Fertility'] -= 1

    current_time = arrow.utcnow().to('local').format('h:mm A')
    relative_date = get_relative_date()

    # Send message to channel and get the message link for
    # Send message to channel and get the message link for child
    embed = nextcord.Embed(title=child_character['Name'], description=child_character['Biography'], color=nextcord.Color.green())
    embed.add_field(name="Dynasty", value=child_character['Dynasty'], inline=False)
    embed.add_field(name="Titles", value=child_character['Titles'], inline=False)
    embed.add_field(name="Lifetime", value=f"{child_character['Birth Year']} - {child_character['Death Year']} ({child_character['Lifespan']} years)", inline=False)
    embed.add_field(name="Parents", value=child_character['Parents'], inline=False)
    embed.add_field(name="Gender", value=child_character['Gender'], inline=True)
    embed.add_field(name="Sexuality", value=child_character['Sexuality'], inline=True)
    embed.add_field(name="Stats", value=(
        f"{emoji_ids['Martial']} {get_stat_role(child_character['Martial'], 'Martial')}\n"
        f"{emoji_ids['Stewardship']} {get_stat_role(child_character['Stewardship'], 'Stewardship')}\n"
        f"{emoji_ids['Learning']} {get_stat_role(child_character['Learning'], 'Learning')}\n"
        f"{emoji_ids['Diplomacy']} {get_stat_role(child_character['Diplomacy'], 'Diplomacy')}\n"
        f"{emoji_ids['Intrigue']} {get_stat_role(child_character['Intrigue'], 'Intrigue')}\n"
        f"{emoji_ids['Prowess']} {get_stat_role(child_character['Prowess'], 'Prowess')}"
    ), inline=False)
    embed.add_field(name="Physical Traits", value=trait_descriptions[0] if physical_trait else "None", inline=False)
    embed.add_field(name="Personality Traits", value=trait_descriptions[1] if physical_trait else trait_descriptions[0], inline=False)
    embed.set_image(url=child_character['Image'])
    embed.set_footer(text=f"ID: {child_character['ID']} | {relative_date}, {current_time}")

    channel = nextcord.utils.get(interaction.guild.channels, name="🧺-characters")
    if channel:
        message = await channel.send(embed=embed)
        child_character['Message Link'] = message.jump_url

        # Update parents' children with the link to the child's message
        child_link = f"[{child_character['Name']}]({child_character['Message Link']})"
        mother['Children'].append(child_link)
        father['Children'].append(child_link)

        await interaction.response.send_message(f"Child {child_character['Name']} created and sent to {channel.mention}")
    else:
        await interaction.response.send_message("Channel 🧺-characters not found.")

# General Command
@bot.slash_command(name="general", description="Create a new general")
async def general(interaction: nextcord.Interaction, name: str, country: str, startyear: int):
    global character_id
    bonus = random.randint(1, 4)
    years_of_service = random.randint(1, 40)
    end_year = startyear + years_of_service

    current_time = arrow.utcnow().to('local').format('h:mm A')
    relative_date = get_relative_date()

    embed = nextcord.Embed(title=f"General {name}", description="General Details", color=nextcord.Color.red())
    embed.add_field(name="Bonus", value=f"+{bonus}", inline=False)
    embed.add_field(name="Country", value=country, inline=False)
    embed.add_field(name="Years of Service", value=f"{startyear} - {end_year} ({years_of_service} years)", inline=False)
    embed.set_footer(text=f"ID: {character_id} | {relative_date}, {current_time}")

    channel = nextcord.utils.get(interaction.guild.channels, name="⚔-general")
    if channel:
        message = await channel.send(embed=embed)
        await interaction.response.send_message(f"General {name} created and sent to {channel.mention}")
        characters[character_id] = {
            'ID': character_id,
            'Name': name,
            'Country': country,
            'Start Year': startyear,
            'End Year': end_year,
            'Years of Service': years_of_service,
            'Bonus': bonus,
            'Owner': interaction.user.id,
            'Message Link': message.jump_url
        }
        character_id += 1
    else:
        await interaction.response.send_message("Channel ⚔-general not found.")

# Admiral Command
@bot.slash_command(name="admiral", description="Create a new admiral")
async def admiral(interaction: nextcord.Interaction, name: str, country: str, startyear: int):
    global character_id
    bonus = random.randint(1, 6)
    years_of_service = random.randint(1, 40)
    end_year = startyear + years_of_service

    current_time = arrow.utcnow().to('local').format('h:mm A')
    relative_date = get_relative_date()

    embed = nextcord.Embed(title=f"Admiral {name}", description="Admiral Details", color=nextcord.Color.blue())
    embed.add_field(name="Bonus", value=f"+{bonus}", inline=False)
    embed.add_field(name="Country", value=country, inline=False)
    embed.add_field(name="Years of Service", value=f"{startyear} - {end_year} ({years_of_service} years)", inline=False)
    embed.set_footer(text=f"ID: {character_id} | {relative_date}, {current_time}")

    channel = nextcord.utils.get(interaction.guild.channels, name="🧭-admirals")
    if channel:
        message = await channel.send(embed=embed)
        await interaction.response.send_message(f"Admiral {name} created and sent to {channel.mention}")
        characters[character_id] = {
            'ID': character_id,
            'Name': name,
            'Country': country,
            'Start Year': startyear,
            'End Year': end_year,
            'Years of Service': years_of_service,
            'Bonus': bonus,
            'Owner': interaction.user.id,
            'Message Link': message.jump_url
        }
        character_id += 1
    else:
        await interaction.response.send_message("Channel 🧭-admirals not found.")

# Tutorial Command
@bot.slash_command(name="tutorial", description="Show the tutorial")
async def tutorial(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Bot Tutorial",
        description="Welcome to the bot tutorial! Here are the steps to get started:",
        color=nextcord.Color.blue()
    )
    embed.add_field(name="1. Creating a Character", value="Use `/createcharacter` to create a new character. You need to provide the name, gender, birth year, dynasty, titles, and biography.", inline=False)
    embed.add_field(name="2. Adding a Historical Character", value="Use `/addhistorical` to add a historical character. You need to provide the name, dynasty, birth year, death year, titles, and biography.", inline=False)
    embed.add_field(name="3. Fornicate", value="Use `/fornicate` to create a child from two characters. You need to provide the mother ID, father ID, name, birth year, titles, and biography.", inline=False)
    embed.add_field(name="4. Editing a Character", value="Use `/editfictional` to edit a fictional character's attributes. You can change the name, dynasty, gender, image URL, titles, biography, traits, and color.", inline=False)
    embed.add_field(name="5. Checking Character Ownership", value="Use `/whois` to check who owns a character. You need to provide the character ID.", inline=False)
    embed.add_field(name="6. Transferring a Character", value="Use `/transfer` to transfer a character to someone else. You need to provide the character ID and the new owner.", inline=False)
    embed.add_field(name="7. Viewing the Leaderboard", value="Use `/leaderboard` to display a leaderboard of characters. You can sort by overall, martial, learning, diplomacy, stewardship, intrigue, prowess, or lifetime.", inline=False)
    embed.add_field(name="8. Resetting Characters (Admin Only)", value="Use `/resetcharacters` to reset the character ID back to 1 and void all existing characters. This command is only available to administrators.", inline=False)
    embed.set_footer(text="Use `/help` to see a list of all commands.")

    await interaction.response.send_message(embed=embed)

# Help Command
@bot.slash_command(name="help", description="List all available commands")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Bot Commands",
        description="Here is a list of all available commands:",
        color=nextcord.Color.green()
    )
    embed.add_field(name="/createcharacter", value="Create a new character.", inline=False)
    embed.add_field(name="/addhistorical", value="Add a historical character.", inline=False)
    embed.add_field(name="/fornicate", value="Create a child from two characters.", inline=False)
    embed.add_field(name="/editfictional", value="Edit a fictional character's attributes.", inline=False)
    embed.add_field(name="/whois", value="Check who owns a character.", inline=False)
    embed.add_field(name="/transfer", value="Transfer a character to someone else.", inline=False)
    embed.add_field(name="/leaderboard", value="Display a leaderboard of characters.", inline=False)
    embed.add_field(name="/resetcharacters", value="Reset the character ID back to 1 and void all existing characters (Admin only).", inline=False)
    embed.add_field(name="/tutorial", value="Show the tutorial.", inline=False)
    embed.set_footer(text="Use `/tutorial` to get a detailed tutorial on how to use the bot.")

    await interaction.response.send_message(embed=embed)

# Edit Fictional Character Command
@bot.slash_command(name="editfictional", description="Edit a fictional character's attributes")
async def edit_fictional(
    interaction: nextcord.Interaction,
    characterid: int,
    name: str = None,
    dynasty: str = None,
    gender: str = None,
    image_url: str = None,
    titles: str = None,
    biography: str = None,
    traits: str = None,
    color: str = None
):
    character = characters.get(characterid)
    if not character:
        await interaction.response.send_message(f"Character with ID {characterid} not found.")
        return

    if character['Owner'] != interaction.user.id:
        await interaction.response.send_message("You do not own this character.")
        return

    # Ensure all required keys exist in the character dictionary
    required_keys = ['Name', 'Dynasty', 'Gender', 'Image', 'Titles', 'Biography', 'Traits', 'Message Link', 'Martial', 'Stewardship', 'Learning', 'Diplomacy', 'Intrigue', 'Prowess', 'Birth Year', 'Death Year', 'Lifespan', 'Parents', 'Sexuality']
    for key in required_keys:
        if key not in character:
            await interaction.response.send_message(f"Error: Missing required key '{key}' in the character data.")
            return

    if name:
        character['Name'] = name
    if dynasty:
        character['Dynasty'] = dynasty
    if gender:
        character['Gender'] = gender
    if image_url:
        if is_valid_url(image_url):
            character['Image'] = image_url
        else:
            await interaction.response.send_message("Invalid image URL. Using the default image.")
            character['Image'] = default_image_url
    if titles:
        character['Titles'] = titles
    if biography:
        character['Biography'] = biography
    if traits:
        character['Traits'] = traits.split(", ")

    # Determine the embed color
    color_dict = {
        "red": nextcord.Color.red(),
        "green": nextcord.Color.green(),
        "blue": nextcord.Color.blue(),
        "purple": nextcord.Color.purple(),
        "orange": nextcord.Color.orange(),
        "yellow": nextcord.Color.gold(),
        "black": nextcord.Color.default(),
        "white": nextcord.Color.lighter_grey()
    }

    if color:
        if color.lower() in color_dict:
            embed_color = color_dict[color.lower()]
        else:
            try:
                embed_color = nextcord.Color(int(color.strip("#"), 16))
            except ValueError:
                await interaction.response.send_message("Invalid color value. Please provide a valid color name or hexadecimal color code.")
                return
    else:
        embed_color = nextcord.Color.purple()

    current_time = arrow.utcnow().to('local').format('h:mm A')
    relative_date = get_relative_date()

    embed = nextcord.Embed(title=character['Name'], color=embed_color)
    embed.add_field(name="Biography", value=character['Biography'], inline=False)
    embed.add_field(name="Dynasty", value=character['Dynasty'], inline=False)
    embed.add_field(name="Titles", value=character['Titles'], inline=False)
    embed.add_field(name="Lifetime", value=f"{character['Birth Year']} - {character['Death Year']} ({character['Lifespan']} years)", inline=False)
    embed.add_field(name="Parents", value=character['Parents'], inline=False)
    embed.add_field(name="Gender", value=character['Gender'], inline=True)
    embed.add_field(name="Sexuality", value=character['Sexuality'], inline=True)
    embed.add_field(name="Stats", value=(
        f"{emoji_ids['Martial']} {get_stat_role(character['Martial'], 'Martial')}\n"
        f"{emoji_ids['Stewardship']} {get_stat_role(character['Stewardship'], 'Stewardship')}\n"
        f"{emoji_ids['Learning']} {get_stat_role(character['Learning'], 'Learning')}\n"
        f"{emoji_ids['Diplomacy']} {get_stat_role(character['Diplomacy'], 'Diplomacy')}\n"
        f"{emoji_ids['Intrigue']} {get_stat_role(character['Intrigue'], 'Intrigue')}\n"
        f"{emoji_ids['Prowess']} {get_stat_role(character['Prowess'], 'Prowess')}"
    ), inline=False)
    embed.add_field(name="Physical Traits", value=", ".join(character['Traits']), inline=False)
    embed.set_image(url=character['Image'])
    embed.set_footer(text=f"ID: {character['ID']} | {relative_date}, {current_time}")

    channel = nextcord.utils.get(interaction.guild.channels, name="🧺-characters")
    if channel:
        message = await channel.fetch_message(int(character['Message Link'].split('/')[-1]))
        await message.edit(embed=embed)
        await interaction.response.send_message(f"Character {character['Name']} has been edited. [Jump to message]({character['Message Link']})")
    else:
        await interaction.response.send_message("Channel 🧺-characters not found.")

# Whois Command
@bot.slash_command(name="whois", description="Check who owns a character")
async def whois(interaction: nextcord.Interaction, characterid: int):
    character = characters.get(characterid)
    if not character:
        await interaction.response.send_message(f"Character with ID {characterid} not found.")
        return

    owner = await bot.fetch_user(character['Owner'])
    await interaction.response.send_message(f"Character {character['Name']} (ID: {characterid}) is owned by {owner.mention}.")

# Transfer Command
@bot.slash_command(name="transfer", description="Transfer a character to someone else")
async def transfer(interaction: nextcord.Interaction, characterid: int, new_owner: nextcord.User):
    character = characters.get(characterid)
    if not character:
        await interaction.response.send_message(f"Character with ID {characterid} not found.")
        return

    if character['Owner'] != interaction.user.id:
        await interaction.response.send_message("You do not own this character.")
        return

    character['Owner'] = new_owner.id
    await interaction.response.send_message(f"Character {character['Name']} (ID: {characterid}) has been transferred to {new_owner.mention}.")

# Leaderboard Command
@bot.slash_command(name="leaderboard", description="Display a leaderboard of characters")
async def leaderboard(interaction: nextcord.Interaction, sort_by: str):
    if sort_by not in ["overall", "martial", "learning", "diplomacy", "stewardship", "intrigue", "prowess", "lifetime"]:
        await interaction.response.send_message(f"Invalid sort_by option. Choose from: overall, martial, learning, diplomacy, stewardship, intrigue, prowess, lifetime.")
        return

    def get_stat_total(character):
        return character['Martial'] + character['Stewardship'] + character['Learning'] + character['Diplomacy'] + character['Intrigue'] + character['Prowess']

    if sort_by == "overall":
        sorted_characters = sorted(characters.values(), key=get_stat_total, reverse=True)
    elif sort_by == "lifetime":
        sorted_characters = sorted(characters.values(), key=lambda c: c['Lifespan'], reverse=True)
    else:
        sorted_characters = sorted(characters.values(), key=lambda c: c[sort_by.capitalize()], reverse=True)

    leaderboard_text = f"**Leaderboard sorted by {sort_by.capitalize()}**\n\n"
    for i, character in enumerate(sorted_characters[:10], start=1):
        owner = await bot.fetch_user(character['Owner'])
        character_link = f"[{character['Name']}]({character['Message Link']})"
        leaderboard_text += f"{i}. {character_link} (ID: {character['ID']}) - Owner: {owner.mention} - "
        if sort_by == "overall":
            leaderboard_text += f"Total Stats: {get_stat_total(character)}\n"
        elif sort_by == "lifetime":
            leaderboard_text += f"Lifetime: {character['Lifespan']} years\n"
        else:
            leaderboard_text += f"{sort_by.capitalize()}: {character[sort_by.capitalize()]}\n"

    await interaction.response.send_message(leaderboard_text)

# Reset Characters Command
@bot.slash_command(name="resetcharacters", description="Reset the character ID back to 1 and void all existing characters")
@commands.has_permissions(administrator=True)
async def reset_characters(interaction: nextcord.Interaction):
    global character_id
    character_id = 1

    # Void all existing characters
    for char_id in characters:
        characters[char_id]['ID'] = -1

    # Clear the characters dictionary
    characters.clear()

    await interaction.response.send_message("Character ID has been reset to 1 and all existing characters have been voided.")

# Add the reset_characters command to the bot
bot.add_application_command(reset_characters)

# Error handling for missing required arguments and key errors
@create_character.error
@fornicate.error
@add_historical.error
@edit_fictional.error
async def missing_argument_error(interaction: nextcord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message(f"Error: Missing required argument: {error.param}")
    elif isinstance(error, KeyError):
        await interaction.response.send_message(f"Error: Missing required key in the command.")
    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You do not have the necessary permissions to use this command.")
    else:
        await interaction.response.send_message(f"An unexpected error occurred: {str(error)}")

# Run the bot
bot.run('noneofyobusinessbrody')
