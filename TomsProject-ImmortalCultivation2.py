# Import tkinter
import tkinter as tk
import random
import sqlite3
from datetime import datetime


# List of realms-----------------------------------------------
REALMS = [
    "Mortal",
    "Qi Establishment I",
    "Qi Establishment II",
    "Qi Establishment III",
    "Qi Establishment IV",
    "Qi Establishment V",
    "Qi Establishment VI",
    "Qi Establishment VII",
    "Qi Establishment VIII",
    "Qi Establishment IX",
    "Foundation Establishment"
]
MEDITATION_EVENTS = [
    # --- SECT COURTYARD EVENTS (Safe, Low Yield, Recovery) ---
    {
        "title": "Quiet Breathing",
        "text": "You sit beneath the gaze of stone coyotes, gathering Qi while whispers crawl across the courtyard. It is slow, but steady.",
        "qi": 8,
        "health": 2,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "weight": 50
    },
    {
        "title": "Morning Chants",
        "text": "The wind carries old chants from sealed halls. Listening to the rhythm helps stabilize your wandering thoughts.",
        "qi": 10,
        "health": 4,
        "locations": ["Sect Courtyard"],
        "weight": 35
    },
    {
        "title": "Elder's Correction",
        "text": "An elder passes by and sharply corrects your posture. The adjustment clears a blockage in your meridians.",
        "qi": 14,
        "health": 0,
        "locations": ["Sect Courtyard"],
        "max_realm": 4,
        "weight": 20
    },
    {
        "title": "Sect Master's Gaze",
        "text": "Sect Master Howling Moon briefly watches from a shaded balcony. The sheer pressure of his gaze forces your Qi to condense.",
        "qi": 12,
        "health": 0,
        "min_realm": 3,
        "locations": ["Sect Courtyard"],
        "weight": 15
    },

    # --- COURTYARD STORY: DAWLARK ---
    {
        "title": "Strange Introductions",
        "text": "While meditating a strange man comes upon you. He claims his name is Daoist Dawlark but this seems false.",
        "qi": 12,
        "health": 5,
        "max_realm":1,
        "locations": ["Sect Courtyard"],
        "add_items": ["Dawlark_1"],
        "weight": 30
    },
    {
        "title": "Laughing at the Moon",
        "text": "Daoist Dawlark returns, teaching you that fear loses power when named aloud. You release a breath you didn't know you were holding.",
        "qi": 14,
        "health": 8,
        "locations": ["Sect Courtyard"],
        "required_items": ["Dawlark_1"],
        "remove_items": ["Dawlark_1"],
        "add_items": ["Dawlark_2"],
        "weight": 250
    },

    # --- COURTYARD STORY: JEALOUS JUNIORS ---
    {
        "title": "Disturbed Flow",
        "text": "Jealous Juniors gather nearby, loudly mocking your technique. The distraction ruins your focus, but you manage to scrape together a little Qi.",
        "qi": 6,
        "health": 0,
        "locations": ["Sect Courtyard"],
        "add_items": ["Rivalry_1"],
        "weight": 25
    },

    # --- MOONLIT FOREST EVENTS (High Yield, Damaging, Wild) ---
    {
        "title": "Flooding Moonlight",
        "text": "The unnaturally bright moonlight floods your meridians. It grants powerful Qi, but the cold yin energy burns your physical body.",
        "qi": 22,
        "health": -12,
        "wealth": 0,
        "excluded_items": ["Cracked Protection Talisman", "Butterfly_Ribbon"],
        "locations": ["Moonlit Forest"],
        "weight": 45
    },
    {
        "title": "Wild Yin Gathering",
        "text": "You kneel among the silver grass. The Qi here is wild and sharp, cutting into your health as it fills your core.",
        "qi": 18,
        "health": -8,
        "locations": ["Moonlit Forest"],
        "weight": 40
    },
    {
        "title": "Shadow Beast Disturbance",
        "text": "A shadow beast attacks mid-meditation! You drive it off, but its claws leave a lingering chill in your veins.",
        "qi": 14,
        "health": -18,
        "locations": ["Moonlit Forest"],
        "weight": 25
    },
    {
        "title": "Vision of Failure",
        "text": "The forest remembers the dead. You experience a terrifying hallucination of your own Foundation Establishment failure. The fear injures your mind, but brings deep insight.",
        "qi": 28,
        "excluded_items": ["Dawlark_2", "Sister_Secret_Note"],
        "health": -15,
        "min_realm": 6,
        "locations": ["Moonlit Forest"],
        "weight": 15
    },
    {
        "title": "Ghostly Coyote",
        "text": "Drawn to your long stillness, a ghostly coyote circles you. It breathes a wisp of pure beast insight into your dantian before vanishing.",
        "qi": 26,
        "health": -5,
        "min_meditation_streak": 3,
        "locations": ["Moonlit Forest"],
        "weight": 20
    },

    # --- FOREST STORY: SISTER BUTTERFLY ---
    {
        "title": "Moths to a Flame",
        "text": "Sister Butterfly appears, warning you not to overextend. 'Moths are what actually reach the flame,' she whispers. Her presence lessens the forest's bite.",
        "qi": 16,
        "health": -5,
        "locations": ["Moonlit Forest"],
        "add_items": ["Butterfly_1"],
        "weight": 25
    },

    # --- FOREST STORY: BROTHER HA ---
    {
        "title": "Traces of Brother Ha",
        "text": "You find traces of Brother Ha's old campsite. Meditating within his faded protective formations shields you slightly from the forest's sharp Qi.",
        "qi": 20,
        "health": -5,
        "locations": ["Moonlit Forest"],
        "required_items": ["Ha_1"],
        "remove_items": ["Ha_1"],
        "add_items": ["Ha_2"],
        "weight": 30
    },
# --- REALM-EXCLUSIVE & WEALTH DEPENDENT EVENTS ---
    {
        "title": "Bribing the Pavilion Guard",
        "text": "You slip a few coins to an outer disciple to let you meditate on a stone etched with a minor gathering array. A small price for steady progress.",
        "qi": 18,
        "health": 2,
        "wealth": -4,
        "min_realm": 1,
        "max_realm": 1,
        "min_wealth": 4,
        "locations": ["Sect Courtyard"],
        "weight": 20
    },
    {
        "title": "Purchasing Moon-Dew",
        "text": "You buy a vial of refined moon-dew before sitting down in the woods. It cools the burning in your meridians, allowing you to absorb much more wild Qi.",
        "qi": 28,
        "health": 5,
        "wealth": -8,
        "min_realm": 2,
        "max_realm": 2,
        "min_wealth": 8,
        "locations": ["Moonlit Forest"],
        "weight": 20
    },
    {
        "title": "A Beggar's Focus",
        "text": "With no wealth to buy incense or arrays, you are forced to meditate on the jagged rocks at the edge of the courtyard. The pain keeps you awake, but progress is slow.",
        "qi": 8,
        "health": -4,
        "max_wealth": 2,
        "min_realm": 3,
        "max_realm": 3,
        "locations": ["Sect Courtyard"],
        "weight": 25
    },
    {
        "title": "Grand Gathering Array",
        "text": "You exhaust a small fortune to lay down a grand spirit gathering array. The sheer density of the Qi almost crushes your lungs, but the gains are monstrous.",
        "qi": 45,
        "health": -5,
        "wealth": -30,
        "min_realm": 4,
        "max_realm": 4,
        "min_wealth": 30,
        "weight": 15
    },

    # --- THE "PUSH TO ADVENTURE" MECHANIC (High Realm Penalties) ---
    {
        "title": "Stagnant Core",
        "text": "The ambient Qi in the courtyard is now far too thin for your advanced realm. Sitting here safely only causes your dense core to stagnate and leak Qi. You must seek danger.",
        "qi": -10,
        "health": 0,
        "wealth": 0,
        "min_realm": 5, # Begins punishing players at Qi V
        "locations": ["Sect Courtyard"],
        "weight": 40
    },
    {
        "title": "The Beast Hungers",
        "text": "Your inner beast violently rejects this passive meditation. It hungers for blood, risk, and rare catalysts. Your Qi rebels against your stillness, tearing at your meridians.",
        "qi": -25,
        "health": -15,
        "min_realm": 6,
        "locations": ["Moonlit Forest"],
        "weight": 35
    },
    {
        "title": "Elder's Disappointment",
        "text": "Sister Abyss walks past and sneers at your cowardice. 'A cultivator of your level hiding on a mat? Pathetic.' The shame shatters your focus and drains your gathered Qi.",
        "qi": -20,
        "health": -5,
        "min_realm": 7,
        "locations": ["Sect Courtyard"],
        "weight": 30
    },
# --- AMBIENT STORY MEDITATION EVENTS (Low Impact, Non-Consuming) ---
    {
        "title": "Brother Ha's Snore",
        "text": "Brother Ha is meditating a few mats away. His breathing is loud, occasionally bordering on a snore. It isn't the most profound environment, but his steady presence puts your mind at ease.",
        "qi": 5,
        "health": 2,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Ha_Intro"],
        "weight": 12
    },
    {
        "title": "Distant Glare",
        "text": "Across the courtyard, you catch the Jealous Juniors glaring at you. You are forced to keep a fraction of your focus on your surroundings, causing a minor strain, but it keeps your Qi cycling actively.",
        "qi": 8,
        "health": -2,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Rivalry_Intro"],
        "weight": 10
    },
    {
        "title": "Feeding the Invisible",
        "text": "You open your eyes briefly to see Daoist Dawlark throwing breadcrumbs to birds that do not appear to exist. The absurdity of it breaks your tension, allowing a smooth flow of Qi.",
        "qi": 6,
        "health": 1,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Dawlark_Intro"],
        "weight": 10
    },
    {
        "title": "A Flash of Pale Robes",
        "text": "While meditating in the sharp, wild energy of the woods, you spot Sister Butterfly's pale, moth-embroidered robes in the distance. The reminder of mortality makes you more cautious with your Qi.",
        "qi": 12,
        "health": -5,
        "wealth": 0,
        "locations": ["Moonlit Forest"],
        "required_items": ["Butterfly_1"],
        "weight": 10
    },
    {
        "title": "The Perfect Smile",
        "text": "The Deceitful Senior Sister glides past your meditation spot. She offers a perfectly warm, completely unreadable smile. You subconsciously push your cultivation a little harder, straining your meridians slightly.",
        "qi": 1,
        "health": 3,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Sister_Intro"],
        "weight": 10
    },
# --- AMBIENT MIDLINE STORY MEDITATION EVENTS (Non-Consuming) ---
    {
        "title": "A Respectful Distance",
        "text": "The Jealous Juniors no longer dare to approach your mat. Instead, they huddle in the far corner of the courtyard, casting bitter but fearful glances your way. The newfound quiet allows you to gather Qi without interruption.",
        "qi": 10,
        "health": 0,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Rivalry_Escalation"],
        "weight": 12
    },
    {
        "title": "Brother Ha's Struggle",
        "text": "You notice Brother Ha sweating profusely on a nearby mat, his face pale as he forces Qi through his meridians. His desperation to keep up with you is evident. You push your own cultivation a little harder in solidarity, straining your body.",
        "qi": 12,
        "health": -3,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Ha_Bond"],
        "weight": 12
    },
    {
        "title": "A 'Misplaced' Gift",
        "text": "You arrive at your usual meditation spot to find a stick of premium, slow-burning incense resting on the stone. Across the courtyard, the Deceitful Senior Sister gives a knowing nod. The incense deeply enriches your session, though you wonder what it will cost you later.",
        "qi": 15,
        "health": 2,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Sister_Intro"],
        "weight": 10
    },
    {
        "title": "The Abbess's Ledger",
        "text": "Sister Abyss walks slowly through the courtyard, making notes in a black ledger. She pauses to look at you, her face unreadable, before moving on. The chilling reminder of the sect's high mortality rate sharpens your focus, though it makes your heart race.",
        "qi": 10,
        "health": -2,
        "wealth": 0,
        "locations": ["Sect Courtyard"],
        "required_items": ["Abyss_Intro"],
        "weight": 10
    },
    {
        "title": "Dawlark's Whistle",
        "text": "You meditate near the edge of the Moonlit Forest. Somewhere deep in the silver trees, you hear Daoist Dawlark whistling a bizarre, syncopated tune. Following the strange rhythm surprisingly helps smooth out a tangle in your Qi.",
        "qi": 14,
        "health": 0,
        "wealth": 0,
        "locations": ["Moonlit Forest"],
        "required_items": ["Dawlark_Intro"],
        "weight": 10
    },
{
    "title": "Meridian Collapse",
    "text": "Your mortal frame is too fragile for the Qi you've forced into it. A meridian shatters like glass, sending a spray of blood from your mouth.",
    "qi": -20,
    "health": -50,
    "max_realm": 0, # Mortal Only
    "locations": ["Sect Courtyard", "Moonlit Forest"],
    "weight": 80 # Highly likely for mortals who linger
},
{
    "title": "The False Path",
    "text": "You followed a deceptive flow of energy. By the time you realize the error, the 'False Qi' has eaten away at your vital organs.",
    "qi": -15,
    "health": -45,
    "max_realm": 0,
    "locations": ["Sect Courtyard"],
    "weight": 60
},
{
    "title": "Internal Demon's Whisper",
    "text": "You have sat in silence for too long. Your own mind turns against you, manifesting an 'Internal Demon' that claws at your spirit from the inside.",
    "qi": -30,
    "health": -50,
    "min_meditation_streak": 4, # Dangerous after 3 sessions
    "weight": 100 # High priority when conditions met
},
{
    "title": "Petrification of the Flesh",
    "text": "Like a statue, your body begins to calcify. Without the movement of adventure, your Qi turns to stone in your veins, causing agonizing fractures.",
    "qi": -10,
    "health": -40,
    "min_meditation_streak": 3,
    "weight": 70
},
{
    "title": "Meridian Engorgement",
    "text": "Your meridians at Qi IV are expanding, but the transition is violent. A surge of Qi attempts to widen your pathways prematurely, causing internal hemorrhaging.",
    "qi": 5,
    "health": -30,
    "min_realm": 4,
    "max_realm": 4,
    "locations": ["Sect Courtyard", "Moonlit Forest"],
    "weight": 75
},
{
    "title": "Echoes of the Abyss",
    "text": "Sister Abyss's influence lingers in the air. During your meditation, her cold aura invades your Dantian, freezing your blood and shattering your focus.",
    "qi": -40,
    "health": -20,
    "min_realm": 7,
    "max_realm": 7,
    "locations": ["Sect Courtyard"],
    "weight": 70
},
{
    "title": "Sect Enforcer's 'Inspection'",
    "text": "An enforcer notices your deep meditative state and 'tests' your defense with a palm strike to the chest. 'Weak,' he sneers, leaving you gasping for air.",
    "qi": -10,
    "health": -25,
    "wealth": -5,
    "min_realm": 4,
    "max_realm": 4,
    "locations": ["Sect Courtyard"],
    "weight": 60
},


]
#----------------------------------------------------------------------------

BREAKTHROUGH_SUCCESS_EVENTS = [
    {
        "title": "Clean Breakthrough",
        "text": "Your Qi surges in a steady current. The barrier before you cracks, then shatters.",
        "health": 0,
        "wealth": 0,
        "realm_change": 1,
        "weight": 30
    },
    {
        "title": "Inspired Breakthrough",
        "text": "A sudden insight guides your Qi through the final obstruction. Your foundation feels unusually stable.",
        "health": 5,
        "realm_change": 1,
        "weight": 20
    },
    {
        "title": "Costly Breakthrough",
        "text": "You force your way into the next realm, but the effort leaves your body trembling.",
        "health": -5,
        "realm_change": 1,
        "weight": 20
    },
    {
    "title": "Dawlark's Hidden Key",
    "text": "As your Qi hits the barrier, the Dawlark Key in your pocket resonates. It acts as a literal skeleton key for your meridians, unlocking the next realm with zero strain.",
    "health": 20,
    "realm_change": 1,
    "required_items": ["Dawlark_Key"],
    "weight": 25
    },
    {
    "title": "Butterfly's Graceful Transition",
    "text": "The Butterfly Ribbon glows with a soft light, weaving your chaotic Qi into a silk-like thread that glides through the breakthrough barrier effortlessly.",
    "health": 15,
    "qi": 10, # Retain a little Qi for the next level
    "realm_change": 1,
    "required_items": ["Butterfly_Ribbon"],
    "weight": 25
    },
    {
    "title": "Brother Ha's Stout Support",
    "text": "The memory of Ha's bond steadies your heart. When your Qi wavers, a surge of 'Warming Wine' energy from your core pushes you over the edge.",
    "health": 10,
    "wealth": 30,
    "realm_change": 1,
    "required_items": ["Ha_Bond"],
    "weight": 25
    },
    {
    "title": "The Senior Sister's Toll",
    "text": "The Wax-Sealed Note turns out to be a tracking spell. During your breakthrough, the Senior Sister siphons off a portion of your breakthrough energy for herself.",
    "health": -5,
    "qi": 0,
    "wealth": -10,
    "realm_change": 1,
    "required_items": ["Sister_Secret_Note"],
    "weight": 20
    },
    {
    "title": "The Abyss's Shadow Claim",
    "text": "Being on the Abbess's List was a curse. As you reach for the next realm, the 'Shadow names' on the page drag your spirit back down into the darkness.",
    "health": -3,
    "qi": 0,
    "realm_change": 1,
    "required_items": ["Abyss_List"],
    "weight": 20
    },
    {
    "title": "Junior's Spiteful Sabotage",
    "text": "You realize too late that the Rival Powder has been leaking into your meridians. It causes a 'hiccup' in your Qi flow at the worst possible moment.",
    "health": -10,
    "qi": 15, # Save some Qi, but fail the attempt
    "realm_change": 1,
    "required_items": ["Rival_Powder"],
    "weight": 20
    },
    {
    "title": "Mortal Shedding",
    "text": "The transition from Mortal to Qi I is violent. You vomit black bile—the impurities of the world—as your body finally accepts the energy of the heavens.",
    "health": -20,
    "realm_change": 1,
    "min_realm": 0,
    "max_realm": 0,
    "weight": 100
    },
    {
    "title": "Mortal Flesh",
    "text": "A mortal is closer to that of the immortal than one may think.",
    "health": 100,
    "realm_change": 2,
    "min_realm": 0,
    "max_realm": 0,
    "weight": 30
    },
    {
    "title": "The Mid-Way Wall",
    "text": "At Qi V, the barrier is no longer a curtain, but a mountain.",
    "health": 40,
    "realm_change": 1,
    "min_realm": 4,
    "max_realm": 5,
    "weight": 80
    },
    {
    "title": "Foundation's Glimmer",
    "text": "The final steps towards IX are terrifying. The world seems to slow down. You don't just break through; you begin to see the underlying fabric of the Nine Realms.",
    "health": 10,
    "qi": 20,
    "realm_change": 1,
    "min_realm": 8,
    "max_realm": 8,
    "weight": 90
    }
]


BREAKTHROUGH_FAILURE_EVENTS = [
    {
        "title": "Failed Breakthrough",
        "text": "Your Qi scatters before it can pierce the barrier. The attempt fails.",
        "health": 0,
        "wealth": 0,
        "realm_change": 0,
        "weight": 45
    },
    {
        "title": "Qi Backlash",
        "text": "The failed attempt rebounds through your meridians. Pain burns through your body.",
        "health": -40,
        "realm_change": 0,
        "weight": 30
    },
    {
        "title": "Cracked Meridians",
        "text": "Your meridians strain under the pressure. You survive, but the damage is severe.",
        "health": -20,
        "realm_change": 0,
        "weight": 15
    },
    {
        "title": "Stabilized by Talisman",
        "text": "Your breakthrough fails, but the Cracked Protection Talisman burns away and shields your meridians.",
        "health": 5,
        "realm_change": 0,
        "qi": 30,
        "required_items": ["Cracked Protection Talisman"],
        "remove_items": ["Cracked Protection Talisman"],
        "weight": 50
    }
]

ADVENTURE_EVENTS = [
# --- SECT GROUNDS: REGULAR EVENTS (Realms 0 - 3) ---
    {
        "title": "Sweeping the Medicine Hall",
        "text": "You spend hours sweeping the dust from the outer medicine hall. It is exhausting, tedious work, but the elder flips you a few coins, and you manage to pocket a stray, low-grade herb.",
        "qi": 6,
        "health": 5,
        "wealth": 3,
        "max_realm": 3,
        "locations": ["Sect Grounds"],
        "weight": 40
    },
    {
        "title": "Outer Disciple Sparring",
        "text": "You are roped into a mandatory sparring match in the training yards. You take several hard bruises to the ribs, but the intense physical exertion forces you to cycle your Qi faster.",
        "qi": 10,
        "health": -12,
        "wealth": 0,
        "max_realm": 3,
        "locations": ["Sect Grounds"],
        "weight": 35
    },
    {
        "title": "A Fortunate Find",
        "text": "While walking the cracked stone paths near the elder pavilions, you spot a dropped spirit coin sparkling in the dirt. You quickly pocket it, absorbing the faint residual Qi left on its surface.",
        "qi": 4,
        "health": 0,
        "wealth": 5,
        "max_realm": 3,
        "locations": ["Sect Grounds"],
        "weight": 35
    },
    {
        "title": "Hauling Freezing Water",
        "text": "Your daily sect chore requires hauling heavy wooden buckets from the freezing mountain well to the dormitories. The bitter cold bites at your hands, but the labor slowly tempers your physical foundation.",
        "qi": 8,
        "health": -8,
        "wealth": 2,
        "max_realm": 3,
        "locations": ["Sect Grounds"],
        "weight": 40
    },
    {
        "title": "Observing the Inner Sect",
        "text": "You pause your chores to watch the inner disciples practice sword forms from afar. The sheer pressure of their auras gives you a splitting headache, but you glean a sliver of genuine insight.",
        "qi": 12,
        "health": 2,
        "wealth": 0,
        "max_realm": 3,
        "locations": ["Sect Grounds"],
        "weight": 30
    },
    # --- SECT MARKET: POVERTY EVENTS (Wealth < 20) ---
    {
        "title": "The Debt Collector's Eye",
        "text": "The market enforcers spot your tattered coin pouch. They decide to 'tax' your health since you have no gold to offer, roughening you up to keep the riff-raff out.",
        "qi": 0,
        "health": -30,
        "wealth": 0,
        "max_wealth": 19,
        "locations": ["Sect Market"],
        "weight": 50
    },
    {
        "title": "Desperate Scavenging",
        "text": "You spend the day dodging kicks and insults to reach the discard piles behind the Alchemist's stall. You find a half-eaten herb, but the stress is immense.",
        "qi": 10,
        "health": -15,
        "wealth": 2,
        "max_wealth": 19,
        "add_items": ["Cracked Protection Talisman"],
        "locations": ["Sect Market"],
        "weight": 40
    },
    {
        "title": "The Rat's Bargain",
        "text": "A shady figure offers you a 'gift' because you look desperate. He slips you an item, but his hidden Qi strike leaves your meridians trembling.",
        "qi": 0,
        "health": -25,
        "wealth": 0,
        "max_wealth": 19,
        "add_items": ["Empty Wooden Bowl"],
        "locations": ["Sect Market"],
        "weight": 35
    },
    {
        "title": "Mocked by the Rich",
        "text": "Inner disciples throw copper coins at your feet for sport. You endure the humiliation to gather the scrap wealth, though your pride—and ribs—suffer.",
        "qi": -5,
        "health": -10,
        "wealth": 8,
        "max_wealth": 19,
        "locations": ["Sect Market"],
        "weight": 45
    },

    # --- SECT MARKET: AFFLUENT EVENTS (Wealth >= 20) ---
    {
        "title": "VIP Treatment",
        "text": "The jingling of your heavy purse acts as a talisman. Merchants bow and offer you seats in the shade. The comfort allows your Qi to settle beautifully.",
        "qi": 15,
        "health": 10,
        "wealth": 0,
        "min_wealth": 20,
        "locations": ["Sect Market"],
        "weight": 50
    },
    {
        "title": "Market Meditation Aura",
        "text": "You pay for a spot near the Great Spirit Pillar. The dense trading of spirit stones creates a secondary Qi vortex that nourishes your core.",
        "qi": 25,
        "health": 5,
        "wealth": -5,
        "min_wealth": 20,
        "locations": ["Sect Market"],
        "weight": 35
    },
    {
        "title": "The Senior's Respect",
        "text": "A Senior Sister notices your financial stability and assumes you are a rising star. She gifts you a pill to 'encourage' a future alliance.",
        "qi": 10,
        "health": 15,
        "wealth": 0,
        "add_items": ["Spare Qi Pill"],
        "min_wealth": 20,
        "locations": ["Sect Market"],
        "weight": 30
    },
# --- SECT MARKET: CHARACTER QUEST STARTERS (Neutral) ---
    {
        "title": "Dawlark's Delusion",
        "text": "You spot Daoist Dawlark arguing with a fruit vendor about whether a peach has a soul. He forgets his 'Bent Copper Key' on the counter. You pick it up, intending to return it.",
        "qi": 0,
        "health": 0,
        "wealth": 0,
        "add_items": ["Dawlark_Key"],
        "locations": ["Sect Market"],
        "weight": 5
    },
    {
        "title": "Brother Ha's Tab",
        "text": "Brother Ha is loudly haggling over a side of beef. In the confusion, he drops a 'Crinkled IOU'. It seems he owes the butcher quite a bit of spirit flour.",
        "qi": 0,
        "health": 0,
        "wealth": 1,
        "add_items": ["Ha_IOU"],
        "locations": ["Sect Market"],
        "weight": 4
    },
    {
        "title": "Sister Butterfly's Scent",
        "text": "Sister Butterfly passes through the crowd like a ghost. Where she stood, you find a 'Pale Silk Ribbon' snagged on a merchant's stall. It cold to the touch.",
        "qi": 0,
        "health": 10,
        "wealth": 0,
        "add_items": ["Butterfly_Ribbon"],
        "locations": ["Sect Market"],
        "weight": 4
    },
    {
        "title": "The Senior Sister's Trash",
        "text": "The Deceitful Senior Sister discards a 'Wax-Sealed Note' after reading it with a frown. You retrieve the crumpled parchment from the cobblestones.",
        "qi": 0,
        "health": 0,
        "wealth": 1,
        "add_items": ["Sister_Secret_Note"],
        "locations": ["Sect Market"],
        "weight": 5
    },
    {
        "title": "Sister Abyss's Shadow",
        "text": "Sister Abyss stands motionless in the center of the market. Everyone avoids her. When she leaves, a 'Black Ledger Page' flutters to the ground. It contains a list of names.",
        "qi": 0,
        "health": 0,
        "wealth": 3,
        "add_items": ["Abyss_List"],
        "locations": ["Sect Market"],
        "weight": 5
    },
    {
        "title": "The Jealous Junior's Mistake",
        "text": "A Jealous Junior is so busy glaring at you that he trips, spilling a 'Pouch of Itching Powder'. You scoop it up before he can recover his dignity.",
        "qi": 0,
        "health": 0,
        "wealth": 2,
        "add_items": ["Rival_Powder"],
        "locations": ["Sect Market"],
        "weight": 5
    },
# --- SHADOW CAVE: ITEM-CONSUMING RESONANCE ---
    {
        "title": "Unlocking the Dantian",
        "text": "You snap the 'Bent Copper Key' in two while focusing your intent. The symbolic 'unlocking' shatters a mental block in your cultivation, but the key is now useless.",
        "qi": 30,
        "health": 10,
        "locations": ["Shadow Cave"],
        "required_items": ["Dawlark_Key"],
        "remove_items": ["Dawlark_Key"],
        "weight": 15
    },
    {
        "title": "Burning the Debt",
        "text": "You set Brother Ha's 'Crinkled IOU' ablaze. The smoke forms a protective barrier that filters the cave's toxins. You feel lighter, as if a physical weight has left your soul.",
        "qi": 15,
        "health": 25,
        "locations": ["Shadow Cave"],
        "required_items": ["Ha_IOU"],
        "remove_items": ["Ha_IOU"],
        "weight": 12
    },
    {
        "title": "The Moth's Final Flight",
        "text": "You unravel the 'Pale Silk Ribbon' and let the cave wind take it. It glows intensely, drawing the local Shadow Beasts away from your position before disappearing into the dark.",
        "qi": 20,
        "health": 15,
        "locations": ["Shadow Cave"],
        "required_items": ["Butterfly_Ribbon"],
        "remove_items": ["Butterfly_Ribbon"],
        "weight": 15
    },
    {
        "title": "The Senior's Hidden Path",
        "text": "Following the 'Wax-Sealed Note', you find a hidden vein of pure Qi. The note crumbles as the secret is utilized, its ink fading into the stone.",
        "qi": 45,
        "health": 5,
        "locations": ["Shadow Cave"],
        "required_items": ["Sister_Secret_Note"],
        "remove_items": ["Sister_Secret_Note"],
        "weight": 10
    },
    {
        "title": "Closing the Ledger",
        "text": "You add your own insights to the 'Black Ledger Page' and bury it in the cave floor. The spirits of the fallen disciples mentioned on the page seem to grant you their strength in passing.",
        "qi": 10,
        "health": 30,
        "locations": ["Shadow Cave"],
        "required_items": ["Abyss_List"],
        "remove_items": ["Abyss_List"],
        "weight": 12
    },
    {
        "title": "Explosive Warding",
        "text": "You ignite the 'Pouch of Itching Powder' with a spark of Qi. The resulting cloud of irritants clears the chamber of shadow-mites entirely, leaving a pure, albeit stinging, environment.",
        "qi": 25,
        "health": 10,
        "locations": ["Shadow Cave"],
        "required_items": ["Rival_Powder"],
        "remove_items": ["Rival_Powder"],
        "weight": 15
    },
    {
    "title": "Shadow-Vein Resonance",
    "text": "The very walls of the cave pulse with a dark, ancient rhythm. By aligning your breathing with the stone, you draw in massive amounts of heavy Yin Qi.",
    "qi": 45,
    "health": -5,
    "min_realm": 6,
    "max_realm": 9,
    "locations": ["Shadow Cave"],
    "weight": 30
    },
    {
    "title": "Ancient Cultivator's Hoard",
    "text": "You find a skeleton sitting in perfect lotus position. In its lap lies a pile of discarded, high-grade spirit stones. Their Qi has faded, but their value remains.",
    "qi": 15,
    "wealth": 25,
    "min_realm": 6,
    "max_realm": 9,
    "locations": ["Shadow Cave"],
    "weight": 20
    },
    {
    "title": "Deep Cave Clarity",
    "text": "In the absolute silence of the deep earth, your mental blocks dissolve. Your meridians expand comfortably, healing old scars from previous failed breakthroughs.",
    "qi": 20,
    "health": 30,
    "min_realm": 6,
    "max_realm": 9,
    "locations": ["Shadow Cave"],
    "weight": 25
    },
    {
    "title": "Whispers of the Primordial",
    "text": "Ethereal voices from the darkness dictate a forgotten cultivation method. The knowledge is overwhelming and strains your mind, but the growth is undeniable.",
    "qi": 60,
    "health": -15,
    "min_realm": 6,
    "max_realm": 9,
    "locations": ["Shadow Cave"],
    "weight": 15
    },
    {
    "title": "Suffocating Miasma",
    "text": "The air in the cave turns into a thick, poisonous fog. Without a protective talisman or key to stabilize the environment, the toxins eat into your lungs.",
    "qi": 0,
    "health": -50,
    "min_realm": 3,
    "max_realm": 5,
    "excluded_items": ["Dawlark_Key", "Cracked Protection Talisman"], # See code change below
    "locations": ["Shadow Cave"],
    "weight": 100
    },
    {
    "title": "The Abyss Gazes Back",
    "text": "A mortal soul has no business in these depths. The sheer weight of the spiritual pressure crushes your ribs and shatters your puny dantian instantly.",
    "qi": -50,
    "health": -99,
    "min_realm": 0,
    "max_realm": 2,
    "locations": ["Shadow Cave"],
    "weight": 200
    },
# --- MOONLIT FOREST: AMBIENT & ITEM-BASED EVENTS ---
    {
        "title": "A Familiar Scent",
        "text": "The 'Spare Qi Pill' in your pocket resonates with the wild flora. A patch of Moon-Tulips blooms instantly, releasing a fragrance that clears your mind.",
        "qi": 5,
        "health": 2,
        "locations": ["Moonlit Forest"],
        "required_items": ["Spare Qi Pill"],
        "weight": 15
    },
    {
        "title": "The Vessel's Purpose",
        "text": "You set the 'Empty Wooden Bowl' on a flat stone. It catches the heavy silver dew dripping from the canopy, providing a refreshing, slightly magical drink.",
        "qi": 3,
        "health": 5,
        "locations": ["Moonlit Forest"],
        "required_items": ["Empty Wooden Bowl"],
        "weight": 12
    },
    {
        "title": "Glimmer in the Dark",
        "text": "A 'Spirit Coin' in your belt pouch catches a stray beam of moonlight. The reflection startles a Shadow Beast that was stalking you, giving you a rare moment of true peace.",
        "qi": 8,
        "health": 0,
        "locations": ["Moonlit Forest"],
        "required_items": ["Spirit Coin"],
        "weight": 10
    },
    {
        "title": "Talismanic Shield",
        "text": "The 'Cracked Protection Talisman' hums warmly against your chest. It filters the harsh Yin energy of the forest, making the air feel less like needles and more like silk.",
        "qi": 6,
        "health": 3,
        "locations": ["Moonlit Forest"],
        "required_items": ["Cracked Protection Talisman"],
        "weight": 15
    },
    {
        "title": "The Coyote's Recognition",
        "text": "Because you carry the 'Coyote's Favor', the predatory howls in the distance sound less like threats and more like a greeting. Your heart rate slows, stabilizing your Dantian.",
        "qi": 10,
        "health": 5,
        "locations": ["Moonlit Forest"],
        "required_items": ["Coyote's Favor"],
        "weight": 12
    },
    {
        "title": "Ha's Warming Spirit",
        "text": "The lingering scent of 'Meridian Warming Wine' from your bond with Brother Ha helps you resist the forest's bone-deep chill. You feel a surge of camaraderie and strength.",
        "qi": 7,
        "health": 4,
        "locations": ["Moonlit Forest"],
        "required_items": ["Ha_Bond"],
        "weight": 15
    },
# --- SECT GROUNDS: STORY INTRODUCTIONS ---
    {
        "title": "The First Seeds of Envy",
        "text": "A crowd of agitated figures blocks your path. They have noticed your steady cultivation and mock you under the guise of 'friendly advice.' You push past them, but their bitter resentment is palpable.",
        "qi": 0,
        "health": -5,
        "wealth": 0,
        "locations": ["Sect Grounds"],
        "add_items": ["Rivalry_Intro"],
        "weight": 15
    },
    {
        "title": "A Loud Laugh",
        "text": "A broad-shouldered disciple named Brother Ha claps you on the back, laughing loudly. 'Don't mind the others,' he says, handing you a spare Qi pill. 'Everyone laughs before the mountain gets steep.'",
        "qi": 8,
        "health": 5,
        "wealth": 0,
        "locations": ["Sect Grounds"],
        "add_items": ["Ha_Intro", "Spare Qi Pill"],
        "weight": 15
    },
    {
        "title": "The Empty Bowl",
        "text": "Daoist Dawlark, a cheerful elder in patched robes, stops you in the courtyard. He hands you an empty wooden bowl, claiming it contains exactly what you need. Confused, you tuck it into your robes.",
        "qi": 5,
        "health": 0,
        "wealth": 0,
        "locations": ["Sect Grounds"],
        "add_items": ["Dawlark_Intro", "Empty Wooden Bowl"],
        "weight": 15
    },
    {
        "title": "The Abbess's Chill",
        "text": "Sister Abyss catches you stepping out of line during morning formation. Her calm, unblinking presence forces you to your knees. As punishment, she makes you memorize the names of three dead outer disciples in the freezing wind.",
        "qi": 5,
        "health": -10,
        "wealth": 0,
        "locations": ["Sect Grounds"],
        "add_items": ["Abyss_Intro"],
        "weight": 15
    },
# --- SECT GROUNDS: REGULAR EVENTS (Realms 4 - 7) ---
    {
        "title": "Instructing the Outer Sect",
        "text": "As an established disciple, you are assigned to instruct the newest mortals in basic forms. It is tedious work that drains your stamina, but an elder rewards you with a handful of spirit coins and the repetition solidifies your own foundation.",
        "qi": 15,
        "health": -5,
        "wealth": 6,
        "min_realm": 4,
        "max_realm": 7,
        "locations": ["Sect Grounds"],
        "weight": 35
    },
    {
        "title": "Elder Pavilion Politics",
        "text": "You navigate the treacherous social web of the elder pavilions, running messages between rival factions. You avoid making enemies and earn a tidy sum of wealth, though the mental stress is exhausting.",
        "qi": 12,
        "health": -8,
        "wealth": 8,
        "min_realm": 4,
        "max_realm": 7,
        "locations": ["Sect Grounds"],
        "weight": 30
    },

    # --- SECT GROUNDS: STORY CONTINUATIONS (Realms 4 - 7) ---
    {
        "title": "Desperate Rivals",
        "text": "The Jealous Juniors see your meteoric rise and attempt a coordinated ambush near the dormitories. At your current realm, their forms are slow and clumsy. You scatter them easily, taking their gathered herbs as a tax.",
        "qi": 16,
        "health": -6,
        "wealth": 5,
        "min_realm": 4,
        "max_realm": 7,
        "locations": ["Sect Grounds"],
        "required_items": ["Rivalry_Intro"],
        "remove_items": ["Rivalry_Intro"],
        "add_items": ["Rivalry_Escalation"],
        "weight": 25
    },
    {
        "title": "Brother Ha's Confession",
        "text": "Brother Ha shares a jug of Meridian Warming Wine with you on the training pavilion roof. His loud laugh fades as he admits he fears falling behind your pace. He toasts to your shared road to Foundation Establishment, stabilizing your mind.",
        "qi": 14,
        "health": 10,
        "wealth": 0,
        "min_realm": 4,
        "max_realm": 7,
        "locations": ["Sect Grounds"],
        "required_items": ["Ha_Intro"],
        "remove_items": ["Ha_Intro"],
        "add_items": ["Ha_Bond"],
        "weight": 25
    },
    {
        "title": "The Senior Sister's Smile",
        "text": "A strict sect enforcer tries to fine you for a minor uniform infraction. Suddenly, the graceful Deceitful Senior Sister intervenes, smoothing over the issue with a charming smile and slipping you a pouch of coins. 'We must look out for each other,' she purrs.",
        "qi": 8,
        "health": 0,
        "wealth": 10,
        "min_realm": 4,
        "max_realm": 7,
        "locations": ["Sect Grounds"],
        "add_items": ["Sister_Intro"],
        "weight": 25
    },
    {
    "title": "Lunar Flare-up",
    "text": "The moon peaks through the silver canopy, and for a moment, the Qi becomes a physical weight. Your lungs burn as you inhale raw, unrefined power that tears at your internal lining.",
    "qi": 35,
    "health": -30,
    "min_realm": 4,
    "max_realm": 4,
    "locations": ["Moonlit Forest"],
    "weight": 80
    },
    {
    "title": "Silver Grass Lacerations",
    "text": "The grass here isn't just color; it's sharp as spiritual steel. A gust of wind causes the blades to whip around you mid-meditation, leaving deep, Qi-bleeding gashes.",
    "qi": 10,
    "health": -25,
    "min_realm": 4,
    "max_realm": 4,
    "locations": ["Moonlit Forest"],
    "weight": 70
    },
    {
    "title": "Coyote Matriarch's Presence",
    "text": "A massive, translucent coyote made of pure Yin energy steps into your clearing. It doesn't attack, but its mere presence causes your own Qi to freeze in terror, cracking your meridians.",
    "qi": -25,
    "health": -30,
    "min_realm": 7,
    "max_realm": 7,
    "locations": ["Moonlit Forest"],
    "weight": 85
    },
    {
    "title": "The Moon's Judgment",
    "text": "You've taken too much. The moonlight turns a deep, bruised purple. It siphons your life force to pay back the 'debt' of the Qi you've gathered so far.",
    "qi": 45,
    "health": -35,
    "min_realm": 7,
    "max_realm": 7,
    "locations": ["Moonlit Forest"],
    "weight": 75
    },
    {
    "title": "Jade Grass",
    "text": "It wriggles in the wind.",
    "qi": 20,
    "health": 35,
    "locations": ["Moonlit Forest"],
    "weight": 15
    },
    {
    "title": "Little Mushroom",
    "text": "Its a mushroom.",
    "qi": 1,
    "health": 5,
    "locations": ["Moonlit Forest"],
    "weight": 15
    },
    {
    "title": "Little Blue Mushroom",
    "text": "What were you expecting ?.",
    "qi": 1,
    "health": 5,
    "locations": ["Moonlit Forest"],
    "weight": 10
    },

]

# Chacter Class / Objects--------------------------------
class Character:
    def __init__(self, name):
        self.name = name
        # Qi is stored for breakthroughs
        self.qi = 0
        # Gained or lost during events. Can influence things.
        self.wealth = 5
        # Health 0 means death
        self.health = 100
        # Used to look up name inside realms
        self.realm_index = 0

        # Hidden behavior tracking

        # Hidden behavior tracking
        self.total_meditations = 0
        self.total_adventures = 0
        self.meditation_streak = 0
        self.adventure_streak = 0



        # Hidden Items for events / backend
        self.backpack = []

        self.alive = True
        self.ending = "Still cultivating"

    def realm_name(self):
        return REALMS[self.realm_index]

    def __str__(self):
        return f"{self.name} - {self.realm_name()} - Qi: {self.qi}"

# Streak tracking

def track_meditation(character):
    character.total_meditations += 1
    character.meditation_streak += 1
    character.adventure_streak = 0


def track_adventure(character):
    character.total_adventures += 1
    character.adventure_streak += 1
    character.meditation_streak = 0

def get_behavior_warning(character):
    if character.meditation_streak == 3:
        return (
            "You have spent many days in stillness.\n\n"
            "The elders whisper that a cultivator who never faces the world "
            "may find their Qi growing stagnant."
        )

    if character.adventure_streak == 3:
        return (
            "You have wandered through danger again and again.\n\n"
            "Even the bold must sometimes sit in silence, or their spirit will fray."
        )

    return ""

# Database !!!

DATABASE_NAME = "graveyard.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS graveyard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            final_realm TEXT NOT NULL,
            qi INTEGER NOT NULL,
            wealth INTEGER NOT NULL,
            health INTEGER NOT NULL,
            ending TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_to_graveyard(character, ending):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO graveyard (
            name,
            final_realm,
            qi,
            wealth,
            health,
            ending,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        character.name,
        character.realm_name(),
        character.qi,
        character.wealth,
        character.health,
        ending,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def load_graveyard():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, final_realm, qi, wealth, health, ending, created_at
        FROM graveyard
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records

#

def show_graveyard():
    records = load_graveyard()

    popup = tk.Toplevel(root)
    popup.title("Sect Records")
    popup.geometry("800x500")
    popup.config(bg=BG_COLOR)

    title_label = tk.Label(
        popup,
        text="Sect Records",
        font=("Times New Roman", 26, "bold"),
        bg=BG_COLOR,
        fg=GOLD
    )
    title_label.pack(pady=20)

    if len(records) == 0:
        empty_label = tk.Label(
            popup,
            text="No cultivators have been recorded yet.",
            font=("Georgia", 14),
            bg=BG_COLOR,
            fg=PALE_GOLD
        )
        empty_label.pack(pady=30)
    else:
        text_box = tk.Text(
            popup,
            width=90,
            height=18,
            bg=PANEL_COLOR,
            fg=PALE_GOLD,
            font=("Georgia", 11),
            wrap="word"
        )
        text_box.pack(padx=20, pady=10)

        for record in records:
            name, final_realm, qi, wealth, health, ending, created_at = record

            text_box.insert(
                tk.END,
                f"Name: {name}\n"
                f"Final Realm: {final_realm}\n"
                f"Qi: {qi} | Wealth: {wealth} | Health: {health}\n"
                f"Ending: {ending}\n"
                f"Recorded: {created_at}\n"
                f"{'-' * 70}\n"
            )

        text_box.config(state="disabled")

    close_button = tk.Button(
        popup,
        text="Return",
        font=("Georgia", 12, "bold"),
        bg=BUTTON_BG,
        fg=PALE_GOLD,
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        command=popup.destroy
    )
    close_button.pack(pady=10)



# Item based / backpack commands
def has_item(character, item_name):
    return item_name in character.backpack


def add_item(character, item_name):
    character.backpack.append(item_name)


def remove_item(character, item_name):
    if item_name in character.backpack:
        character.backpack.remove(item_name)


# New Game --------------------------------------------

def start_new_game():
    popup = tk.Toplevel(root)
    popup.title("Create New Character")
    popup.geometry("400x220")

    name_var = tk.StringVar()

    title = tk.Label(
        popup,
        text="Enter your cultivator's name:",
        font=("Helvetica", 14, "bold")
    )
    title.pack(pady=15)

    name_entry = tk.Entry(
        popup,
        textvariable=name_var,
        font=("Helvetica", 14)
    )
    name_entry.pack(pady=10)

    def create_character():
        global player

        name = name_var.get().strip()

        if name == "":
            warning_label.config(text="Name cannot be blank.")
            return

        player = Character(name)
        update_stat_labels()
        popup.destroy()

    start_button = tk.Button(
        popup,
        text="Start Cultivating",
        font=("Helvetica", 12),
        command=create_character
    )
    start_button.pack(pady=10)

    warning_label = tk.Label(
        popup,
        text="",
        font=("Helvetica", 10),
        fg="red"
    )
    warning_label.pack()


# Temp Player ---------
player = Character("Young Disciple")
#-----------------------------------------\


# Fortunate Son

def reset_to_fortunate_son():
    global player

    player = Character("Fortunate Son")
    update_stat_labels()

def reset_to_Wretch():
    global player
    player = Character("Wretchful Soul")
    update_stat_labels()
# Death Function

def check_end_conditions():
    if player.health <= 0:
        show_death_screen()

def show_death_screen():
    ending = "A miselrly death"
    save_to_graveyard(player, ending)
    show_popup(
        "Your Path Ends",
        f"{player.name}'s cultivation path has ended.\n\n"
        f"Final Realm: {player.realm_name()}\n"
        f"Final Qi: {player.qi}\n"
        f"Final Wealth: {player.wealth}\n\n"
        "Another soul steps onto the path...",
        reset_to_Wretch
    )

# Function to update stat labels every time there is a change
def update_stat_labels():
    breakthrough_chance = calculate_breakthrough_chance(player)

    name_label.config(text=f"Name: {player.name}")
    realm_label.config(text=f"Realm: {player.realm_name()}")
    qi_label.config(text=f"Qi: {player.qi}")
    wealth_label.config(text=f"Wealth: {player.wealth}")
    health_label.config(text=f"Health: {player.health}")
    breakthrough_label.config(text=f"Breakthrough Chance: {breakthrough_chance:.1f}%")

# - Changing Location for meditation

def show_meditation_location_choice():
    popup = tk.Toplevel(root)
    popup.title("Choose Meditation Location")
    popup.geometry("500x300")
    popup.config(bg="#0b0b0b")

    title_label = tk.Label(
        popup,
        text="Where will you meditate?",
        font=("Times New Roman", 22, "bold"),
        bg="#0b0b0b",
        fg="#d8b26e"
    )
    title_label.pack(pady=25)

    description_label = tk.Label(
        popup,
        text="Different locations may shape the Qi you gather and the events you encounter.",
        font=("Georgia", 13),
        wraplength=400,
        justify="center",
        bg="#0b0b0b",
        fg="#fff1c1"
    )
    description_label.pack(pady=10)

    button_frame = tk.Frame(popup, bg="#0b0b0b")
    button_frame.pack(pady=25)

    courtyard_button = tk.Button(
        button_frame,
        text="Sect Courtyard",
        font=("Georgia", 12, "bold"),
        bg="#2b2b2b",
        fg="#fff1c1",
        padx=12,
        pady=6,
        command=lambda: meditate_at_location(popup, "Sect Courtyard")
    )
    courtyard_button.pack(side=tk.LEFT, padx=10)

    forest_button = tk.Button(
        button_frame,
        text="Moonlit Forest",
        font=("Georgia", 12, "bold"),
        bg="#2b2b2b",
        fg="#fff1c1",
        padx=12,
        pady=6,
        command=lambda: meditate_at_location(popup, "Moonlit Forest")
    )
    forest_button.pack(side=tk.LEFT, padx=10)

# Event Chooser
# Event Chooser
def choose_event(event_list, character, location=None):
    possible_events = []

    for event in event_list:
        min_realm = event.get("min_realm", 0)
        max_realm = event.get("max_realm", len(REALMS) - 1)

        min_wealth = event.get("min_wealth", 0)
        max_wealth = event.get("max_wealth", 999999)

        min_meditation_streak = event.get("min_meditation_streak", 0)
        max_meditation_streak = event.get("max_meditation_streak", 999999)

        min_adventure_streak = event.get("min_adventure_streak", 0)
        max_adventure_streak = event.get("max_adventure_streak", 999999)

        allowed_locations = event.get("locations", None)
        required_items = event.get("required_items", [])

        realm_allowed = min_realm <= character.realm_index <= max_realm
        wealth_allowed = min_wealth <= character.wealth <= max_wealth

        meditation_streak_allowed = (
            min_meditation_streak
            <= character.meditation_streak
            <= max_meditation_streak
        )

        adventure_streak_allowed = (
            min_adventure_streak
            <= character.adventure_streak
            <= max_adventure_streak
        )

        if allowed_locations is None:
            location_allowed = True
        else:
            location_allowed = location in allowed_locations

        items_allowed = True
        # Check if player lacks a required item
        for item in required_items:
            if not has_item(character, item):
                items_allowed = False

        # New: Check if player has an item they SHOULDN'T have
        excluded_items = event.get("excluded_items", [])
        for item in excluded_items:
            if has_item(character, item):
                items_allowed = False

        if (
            realm_allowed
            and wealth_allowed
            and location_allowed
            and items_allowed
            and meditation_streak_allowed
            and adventure_streak_allowed
        ):
            possible_events.append(event)

    if len(possible_events) == 0:
        return None

    weights = []
    for event in possible_events:
        weights.append(event.get("weight", 1))

    return random.choices(possible_events, weights=weights, k=1)[0]


# Test Meditate Button ------------------------
def meditate():
    show_meditation_location_choice()

def meditate_at_location(location_popup, location):
    location_popup.destroy()

    track_meditation(player)

    event = choose_event(MEDITATION_EVENTS, player, location)

    if event is None:
        show_meditation_popup(
            f"You meditate at the {location}.\n\n"
            "Nothing unusual happens."
        )
        return

    qi_change = event.get("qi", 0)
    health_change = event.get("health", 0)
    wealth_change = event.get("wealth", 0)

    player.qi += qi_change
    player.health += health_change
    player.wealth += wealth_change

    # Prevent Qi and wealth from going below 0
    if player.qi < 0:
        player.qi = 0

    if player.wealth < 0:
        player.wealth = 0

    # Add items from the event
    for item in event.get("add_items", []):
        add_item(player, item)

    # Remove items from the event
    for item in event.get("remove_items", []):
        remove_item(player, item)

    update_stat_labels()
    check_end_conditions()
    warning = get_behavior_warning(player)
    show_meditation_popup(
        f"{event['title']}\n\n"
        f"{event['text']}\n\n"
        f"Location: {location}\n"
        f"Qi: {qi_change:+}\n"
        f"Health: {health_change:+}\n"
        f"Wealth: {wealth_change:+}\n\n"
        f"{warning}"
    )

# Adventure Functions
def adventure():
    show_adventure_location_choice()


def show_adventure_location_choice():
    popup = tk.Toplevel(root)
    popup.title("Choose Adventure Location")
    popup.geometry("600x350")
    popup.config(bg=BG_COLOR)

    title_label = tk.Label(
        popup,
        text="Where will you adventure?",
        font=("Times New Roman", 22, "bold"),
        bg=BG_COLOR,
        fg=GOLD
    )
    title_label.pack(pady=25)

    description_label = tk.Label(
        popup,
        text="Each location holds different dangers, rewards, and hidden encounters.",
        font=("Georgia", 13),
        wraplength=450,
        justify="center",
        bg=BG_COLOR,
        fg=PALE_GOLD
    )
    description_label.pack(pady=10)

    button_frame = tk.Frame(popup, bg=BG_COLOR)
    button_frame.pack(pady=25)

    locations = ["Sect Grounds", "Moonlit Forest", "Sect Market", "Shadow Cave"]

    for location in locations:
        location_button = tk.Button(
            button_frame,
            text=location,
            font=("Georgia", 11, "bold"),
            bg=BUTTON_BG,
            fg=PALE_GOLD,
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            padx=10,
            pady=6,
            command=lambda chosen_location=location: adventure_at_location(popup, chosen_location)
        )
        location_button.pack(side=tk.LEFT, padx=6)

def apply_event(event, character):
    """Utility to apply all dictionary-based changes to the character."""
    character.qi += event.get("qi", 0)
    character.health += event.get("health", 0)
    character.wealth += event.get("wealth", 0)
    character.realm_index += event.get("realm_change", 0)

    # Floor values at 0
    if character.qi < 0: character.qi = 0
    if character.wealth < 0: character.wealth = 0

    # Handle Items
    for item in event.get("add_items", []):
        add_item(character, item)
    for item in event.get("remove_items", []):
        remove_item(character, item)

def adventure_at_location(location_popup, location):
    location_popup.destroy()

    track_adventure(player)

    event = choose_event(ADVENTURE_EVENTS, player, location)

    if event is None:
        show_adventure_popup(
            f"You travel to the {location}.\n\n"
            "Nothing unusual happens."
        )
        return

    apply_event(event, player)
    update_stat_labels()
    check_end_conditions()
    warning = get_behavior_warning(player)

    show_adventure_popup(
        f"{event['title']}\n\n"
        f"{event['text']}\n\n"
        f"Location: {location}\n"
        f"Qi: {event.get('qi', 0):+}\n"
        f"Health: {event.get('health', 0):+}\n"
        f"Wealth: {event.get('wealth', 0):+}\n\n"
        f"{warning}"
    )

def show_adventure_popup(message):
    popup = tk.Toplevel(root)
    popup.title("Adventure")
    popup.geometry("800x800")
    popup.config(bg="#120b0b")

    title_label = tk.Label(
        popup,
        text="Adventure",
        font=("Times New Roman", 26, "bold"),
        bg="#120b0b",
        fg="#d8b26e"
    )
    title_label.pack(pady=20)

    popup_label = tk.Label(
        popup,
        text=message,
        font=("Georgia", 15),
        wraplength=500,
        justify="center",
        bg="#120b0b",
        fg="#fff1c1"
    )
    popup_label.pack(pady=30)

    close_button = tk.Button(
        popup,
        text="Return",
        font=("Georgia", 12, "bold"),
        bg=BUTTON_BG,
        fg=PALE_GOLD,
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        command=popup.destroy
    )
    close_button.pack(pady=10)

# basic Popup ----------------------------
def show_popup(title, message, close_command=None):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("650x420")
    popup.config(bg="#0b0b0b")

    outer_frame = tk.Frame(
        popup,
        bg="#0b0b0b"
    )
    outer_frame.pack(expand=True)

    title_label = tk.Label(
        outer_frame,
        text=title,
        font=("Times New Roman", 32, "bold"),
        bg="#0b0b0b",
        fg="#d8b26e"
    )
    title_label.pack(pady=(10, 20))

    message_frame = tk.Frame(
        outer_frame,
        bg="#8b4a16",
        padx=25,
        pady=25,
        highlightbackground="#d8b26e",
        highlightthickness=2
    )
    message_frame.pack(pady=10)

    popup_label = tk.Label(
        message_frame,
        text=message,
        font=("Georgia", 16),
        wraplength=500,
        justify="center",
        bg="#8b4a16",
        fg="#fff1c1"
    )
    popup_label.pack()

    def close_popup():
        popup.destroy()

        if close_command is not None:
            close_command()

    close_button = tk.Button(
        outer_frame,
        text="Continue",
        font=("Georgia", 13, "bold"),
        bg="#2b2b2b",
        fg="#fff1c1",
        activebackground="#3a2a1a",
        activeforeground="#ffffff",
        padx=18,
        pady=6,
        command=close_popup
    )
    close_button.pack(pady=(25, 5))

# Meditation Popup -----------------------------------
def show_meditation_popup(message):
    popup = tk.Toplevel(root)
    popup.title("Meditation")
    popup.geometry("700x500")
    popup.config(bg="midnightblue")

    title_label = tk.Label(
        popup,
        text="Meditation",
        font=("Times New Roman", 24, "bold"),
        bg="midnightblue",
        fg="lightcyan"
    )
    title_label.pack(pady=20)

    popup_label = tk.Label(
        popup,
        text=message,
        font=("Helvetica", 14),
        wraplength=450,
        justify="center",
        bg="midnightblue",
        fg="white"
    )
    popup_label.pack(pady=30)

    close_button = tk.Button(
        popup,
        text="Return",
        font=("Helvetica", 12),
        bg="gray20",
        fg="white",
        command=popup.destroy
    )
    close_button.pack(pady=10)

# Breakthrough Logic -------------------------------------------------------

def attempt_breakthrough():
    if player.realm_index >= len(REALMS) - 1:
        show_popup(
            "Peak Reached",
            "You have already reached Foundation Establishment.",
            reset_to_fortunate_son
        )
        return

    breakthrough_chance = calculate_breakthrough_chance(player)
    roll = random.randint(1, 100)
    spent_qi = player.qi

    # All Qi is spent on the breakthrough attempt
    player.qi = 0

    if roll <= breakthrough_chance:
        event = choose_event(BREAKTHROUGH_SUCCESS_EVENTS, player)
        result_text = "Success"
    else:
        event = choose_event(BREAKTHROUGH_FAILURE_EVENTS, player)
        result_text = "Failure"

    if event is None:
        show_popup(
            "Breakthrough",
            "Nothing unusual happens, but your Qi has still been spent."
        )
        update_stat_labels()
        check_end_conditions()
        return

    apply_event(event, player)
    update_stat_labels()
    check_end_conditions()

    if player.realm_name() == "Foundation Establishment":
        save_to_graveyard(player, "Ascended to Foundation Establishment")
        show_popup(
            "Ascension!",
            f"{event['title']}\n\n"
            f"{event['text']}\n\n"
            f"Result: {result_text}\n"
            f"Qi Spent: {spent_qi}\n"
            "You successfully reached Foundation Establishment!\n\n"
            "Game won!",
            reset_to_fortunate_son
        )
    else:
        show_popup(
            event["title"],
            f"{event['text']}\n\n"
            f"Result: {result_text}\n"
            f"Realm: {player.realm_name()}\n"
            f"Health: {event.get('health', 0):+}\n"
        )

# Breakthrough Logic

def get_required_qi(character):
    next_realm_number = character.realm_index + 1
    return next_realm_number * 10

def calculate_breakthrough_chance(character):
    # If the player is already at the final realm,
    # there is no next breakthrough.
    if character.realm_index >= len(REALMS) - 1:
        return 0

    required_qi = get_required_qi(character)

    # The required Qi gives a 90% chance.
    success_chance = character.qi / required_qi * 90

    # Cap the chance at 90%
    if success_chance > 90:
        success_chance = 90

    return success_chance

# Theming !!!!
BG_COLOR = "#0b0b0b"
PANEL_COLOR = "#1a1410"
GOLD = "#d8b26e"
PALE_GOLD = "#fff1c1"
BUTTON_BG = "#2b2b2b"
BUTTON_HOVER = "#3a2a1a"

# Create the main GUI window--------------------------------------
root = tk.Tk()
root.title( "Howling Coyote Sect: Trial of the Nine Realms")
root.geometry("700x600")
root.config(bg=BG_COLOR)


# Title Label----------------------------------------------------
title_label = tk.Label(
    root,
    text="Trial of the Nine Realms",
    font=("Times New Roman", 32, "bold"),
    fg=GOLD,
    bg=BG_COLOR
)
title_label.pack(pady=(30, 25))
# Title ^

# Character stat labels ---------------------------

stat_frame = tk.Frame(
    root,
    bg=PANEL_COLOR,
    padx=35,
    pady=20,
    highlightbackground=GOLD,
    highlightthickness=2
)
stat_frame.pack(pady=10)
name_label = tk.Label(
    stat_frame,
    text=f"Name: {player.name}",
    font=("Georgia", 15),
    fg = PALE_GOLD,
    bg = PANEL_COLOR
)
name_label.pack(pady=5)

realm_label = tk.Label(
    stat_frame,
    text=f"Realm: {player.realm_name()}",
    font=("Georgia", 15),
    fg=PALE_GOLD,
    bg=PANEL_COLOR
)
realm_label.pack(pady=5)

qi_label = tk.Label(
    stat_frame,
    text=f"Qi: {player.qi}",
    font=("Georgia", 15),
    fg=PALE_GOLD,
    bg=PANEL_COLOR
)
qi_label.pack(pady=5)

wealth_label = tk.Label(
    stat_frame,
    text=f"Wealth: {player.wealth}",
    font=("Georgia", 15),
    fg=PALE_GOLD,
    bg=PANEL_COLOR
)
wealth_label.pack(pady=5)

health_label = tk.Label(
    stat_frame,
    text=f"Health: {player.health}",
    font=("Georgia", 15),
    fg=PALE_GOLD,
    bg=PANEL_COLOR
)
health_label.pack(pady=5)
# Stat Labels ^^^ ----------------------------


# First button frame: main action buttons
main_button_frame = tk.Frame(root, bg=BG_COLOR)
main_button_frame.pack(pady=20)

meditate_button = tk.Button(
    main_button_frame,
    text="Meditate",
    font=("Georgia", 14, "bold"),
    bg=BUTTON_BG,
    fg=PALE_GOLD,
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    padx=16,
    pady=6,
    command=meditate
)
meditate_button.pack(side=tk.LEFT, padx=10)

adventure_button = tk.Button(
    main_button_frame,
    text="Adventure",
    font=("Georgia", 14, "bold"),
    bg=BUTTON_BG,
    fg=PALE_GOLD,
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    padx=16,
    pady=6,
    command=adventure
)
adventure_button.pack(side=tk.LEFT, padx=10)

breakthrough_button = tk.Button(
    main_button_frame,
    text="Breakthrough",
    font=("Georgia", 14, "bold"),
    bg=BUTTON_BG,
    fg=PALE_GOLD,
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    padx=16,
    pady=6,
    command=attempt_breakthrough
)
breakthrough_button.pack(side=tk.LEFT, padx=10)


# Second button frame: secondary/menu buttons
secondary_button_frame = tk.Frame(root, bg=BG_COLOR)
secondary_button_frame.pack(pady=5)

start_anew_button = tk.Button(
    secondary_button_frame,
    text="Start Anew",
    font=("Georgia", 13, "bold"),
    bg="#1f1f1f",
    fg=GOLD,
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    padx=14,
    pady=5,
    command=start_new_game
)
start_anew_button.pack(side=tk.LEFT, padx=10)

graveyard_button = tk.Button(
    secondary_button_frame,
    text="Records",
    font=("Georgia", 13, "bold"),
    bg="#1f1f1f",
    fg=GOLD,
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    padx=14,
    pady=5,
    command=show_graveyard
)
graveyard_button.pack(side=tk.LEFT, padx=10)


breakthrough_label = tk.Label(
    root,
    font=("Georgia", 15, "bold"),
    fg=GOLD,
    bg=BG_COLOR
)
breakthrough_label.pack(pady=18)

update_stat_labels()
# Mainloop Starts Program
create_database()
root.mainloop()

