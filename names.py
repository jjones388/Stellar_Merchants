import random

"""
Helper module for generating various names for the game.
"""

# Lists of name parts for procedural generation
first_name_parts = [
    "Al", "An", "Ar", "Bal", "Bar", "Bel", "Bor", "Bran", "Cal", "Cam", 
    "Car", "Cham", "Cor", "Dal", "Dan", "Dar", "Der", "Dom", "Dor", "Dra",
    "Dur", "El", "Er", "Far", "Fal", "Fel", "Fin", "Gar", "Gal", "Gan", 
    "Ger", "Gil", "Gor", "Gra", "Hal", "Han", "Har", "Hel", "Hor", "Il",
    "In", "Ir", "Jal", "Jar", "Jul", "Kag", "Kal", "Kel", "Kha", "Kol", 
    "Kor", "Kra", "Kur", "Lan", "Leo", "Lor", "Mal", "Mar", "Mer", "Mir",
    "Mor", "Nar", "Ner", "Nor", "Orl", "Orm", "Par", "Per", "Pol", "Por", 
    "Qar", "Qor", "Rad", "Rag", "Ran", "Ren", "Rha", "Rol", "Ron", "Sal",
    "Sam", "Sar", "Sel", "Ser", "Sha", "Sol", "Sul", "Syl", "Tal", "Tam", 
    "Tar", "Tel", "Thal", "Thar", "Ther", "Tir", "Tor", "Tul", "Tur", "Ul",
    "Val", "Van", "Var", "Vir", "Vor", "Xal", "Xar", "Xen", "Xer", "Yar", 
    "Yen", "Yor", "Yr", "Zal", "Zan", "Zel", "Zen", "Zer", "Zor", "Zur"
]

last_name_parts = [
    "adur", "amar", "amon", "anis", "ar", "arian", "arion", "arter", "as", 
    "astar", "aster", "aus", "ax", "azar", "bard", "baros", "beros", "borm",
    "born", "breaker", "bringer", "bwyn", "caster", "cyn", "dar", "del", 
    "des", "dex", "dian", "din", "dor", "doron", "dra", "dras", "duil", 
    "duin", "dur", "ean", "el", "elor", "emar", "en", "er", "eron", "esh",
    "essar", "este", "far", "fin", "fire", "fler", "flores", "forn", 
    "fornia", "gant", "garn", "geos", "ghal", "ghar", "gon", "heim", "herys",
    "ian", "iat", "ib", "ic", "idus", "igar", "ight", "ik", "il", "illius", 
    "in", "inas", "ine", "ing", "ion", "ious", "iros", "is", "ish", "isor",
    "ith", "ix", "lach", "lak", "lam", "lan", "lans", "lar", "las", "lech", 
    "len", "lian", "lias", "lin", "lis", "lor", "loth", "lune", "lus", 
    "mad", "man", "many", "mar", "mas", "moor", "mus", "nan", "narth", 
    "neel", "neth", "nir", "nis", "nius", "nos", "nus", "oad", "on", "or",
    "orn", "os", "oth", "pheus", "phor", "phyra", "pis", "polis", "por", 
    "qar", "qis", "qor", "quar", "ras", "rat", "ren", "ric", "rich", "rin",
    "ris", "ro", "roth", "ryn", "s", "seer", "sen", "ser", "ses", "set", 
    "shan", "shee", "shor", "sian", "siol", "sol", "soris", "spor", "star", 
    "stian", "sus", "tar", "ten", "ter", "thalos", "thar", "ther", "tia", 
    "ton", "tor", "tus", "us", "vain", "van", "var", "varen", "varin", 
    "vax", "ven", "ver", "vius", "vor", "vus", "wan", "wer", "wich", "wick", 
    "win", "wood", "wyn", "xar", "xath", "xen", "xis", "xor", "yar", "yen", 
    "ynor", "yr", "yth", "zar", "zen", "zor", "zus"
]

def get_first_name():
    """Generate a random first name"""
    if random.random() < 0.3:  # 30% chance for compound name
        return random.choice(first_name_parts) + random.choice(first_name_parts).lower()
    else:
        return random.choice(first_name_parts)

def get_last_name():
    """Generate a random last name"""
    if random.random() < 0.2:  # 20% chance for compound name
        return random.choice(first_name_parts) + random.choice(last_name_parts)
    else:
        if random.random() < 0.5:
            return random.choice(first_name_parts) + random.choice(last_name_parts)
        else:
            return random.choice(first_name_parts) + random.choice(first_name_parts).lower()

def get_full_name():
    """Generate a full name (first + last)"""
    return f"{get_first_name()} {get_last_name()}"

# Lists for planet name generation
planet_prefixes = [
    "New", "Old", "Great", "Lesser", "Upper", "Lower", "Inner", "Outer",
    "Central", "Northern", "Southern", "Eastern", "Western", "Bright",
    "Dark", "Red", "Blue", "Green", "Yellow", "White", "Black", "Golden",
    "Silver", "Azure", "Crimson", "Jade", "Amber", "Crystal", "Shadow",
    "Twin", "Sacred", "Holy", "Divine", "Cursed", "Lost", "Hidden", "Forbidden"
]

planet_types = [
    "Prime", "Minor", "Major", "Alpha", "Beta", "Gamma", "Delta", "Epsilon",
    "Zeta", "Theta", "Iota", "Kappa", "Lambda", "Sigma", "Tau", "Omega",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "Station", "Colony", "Outpost", "Base", "Port", "Hub", "Nexus", "Gate",
    "World", "Planet", "Moon", "Satellite", "Rock", "Giant", "Dwarf"
]

def get_planet_name():
    """Generate a random planet name"""
    name_type = random.randint(1, 5)
    
    if name_type == 1:
        # FirstName + LastName + Type (e.g. "Thomas Jefferson Prime")
        return f"{get_first_name()} {get_last_name()} {random.choice(planet_types)}"
    elif name_type == 2:
        # Prefix + LastName (e.g. "New Andoria")
        return f"{random.choice(planet_prefixes)} {get_last_name()}"
    elif name_type == 3:
        # LastName + Type (e.g. "Rigel Prime")
        return f"{get_last_name()} {random.choice(planet_types)}"
    elif name_type == 4:
        # Simple LastName (e.g. "Meridian")
        return get_last_name()
    else:
        # FirstName (e.g. "Xandar")
        return get_first_name()

# Lists for ship name generation
ship_prefixes = [
    "ISS", "USS", "HMS", "CSS", "RSV", "NSC", "ESS", "FSS", "GSS",
    "ITS", "MCS", "PSF", "TSC", "WSF", "XSS", "DSV", "SSV", "MSV",
    "FTL", "ASV", "BSC", "TCS", "NCC", "STS", "OSS"
]

ship_names = [
    "Reliant", "Defiant", "Intrepid", "Sovereign", "Valiant", "Odyssey",
    "Voyager", "Enterprise", "Discovery", "Excelsior", "Challenger", "Endeavor",
    "Dauntless", "Phoenix", "Pegasus", "Orion", "Polaris", "Antares", "Sirius",
    "Vega", "Rigel", "Andromeda", "Cassiopeia", "Perseus", "Hercules", "Taurus",
    "Aurora", "Eclipse", "Horizon", "Zenith", "Nadir", "Meridian", "Cardinal",
    "Tempest", "Maelstrom", "Typhoon", "Hurricane", "Tornado", "Cyclone", "Avalanche",
    "Barracuda", "Stingray", "Manta", "Leviathan", "Kraken", "Hydra", "Cerberus",
    "Chimera", "Basilisk", "Griffin", "Manticore", "Sphinx", "Minotaur", "Wyvern",
    "Dragon", "Falcon", "Eagle", "Hawk", "Osprey", "Condor", "Raven", "Phoenix",
    "Spitfire", "Hellfire", "Firestorm", "Inferno", "Blaze", "Ember", "Comet",
    "Meteor", "Asteroid", "Nova", "Pulsar", "Quasar", "Nebula", "Stardust", "Cosmos",
    "Infinity", "Eternity", "Destiny", "Legacy", "Heritage", "Vanguard", "Sentinel",
    "Guardian", "Protector", "Defender", "Avenger", "Vindicator", "Retribution", "Justice"
]

ship_modifiers = [
    "Mark II", "Mark III", "Mark IV", "Mark V", "A", "B", "C", "X", "Alpha", "Omega",
    "Prime", "Redux", "Refit", "Advanced", "Prototype", "Experimental", "Enhanced",
    "Modified", "Custom", "Special", "Elite", "Superior", "Ultimate", "Supreme", 
    "Maximus", "Plus", "Pro", "Ultra", "Hyper", "Super", "Mega", "Turbo"
]

def get_ship_name():
    """Generate a random ship name"""
    name_type = random.randint(1, 5)
    
    if name_type == 1:
        # Prefix + Name (e.g. "ISS Reliant")
        return f"{random.choice(ship_prefixes)} {random.choice(ship_names)}"
    elif name_type == 2:
        # Name + Modifier (e.g. "Phoenix Mark II")
        return f"{random.choice(ship_names)} {random.choice(ship_modifiers)}"
    elif name_type == 3:
        # Prefix + Name + Modifier (e.g. "USS Enterprise A")
        return f"{random.choice(ship_prefixes)} {random.choice(ship_names)} {random.choice(ship_modifiers)}"
    elif name_type == 4:
        # The + Adjective + Noun (e.g. "The Mighty Voyager")
        adjectives = ["Mighty", "Swift", "Bold", "Brave", "Valiant", "Fearless", "Iron", "Steel",
                     "Golden", "Silver", "Crimson", "Azure", "Emerald", "Royal", "Imperial",
                     "Eternal", "Ancient", "Vengeful", "Relentless", "Silent", "Vigilant"]
        return f"The {random.choice(adjectives)} {random.choice(ship_names)}"
    else:
        # Simple Name (e.g. "Nebula")
        return random.choice(ship_names)

# Lists for corporation/faction name generation
corp_prefixes = [
    "Alpha", "Beta", "Gamma", "Delta", "Omega", "Apex", "Prime", "Core", "Nova",
    "Stellar", "Galactic", "Cosmic", "Astral", "Solar", "Lunar", "Orbital",
    "Trans", "Inter", "Ultra", "Mega", "Giga", "Micro", "Nano", "Quantum", "Fusion",
    "Neo", "Meta", "Para", "Omni", "Multi", "Uni", "Poly", "Dyna", "Syn", "Gen"
]

corp_roots = [
    "tech", "corp", "corp", "dyne", "sys", "soft", "ware", "net", "web", "com",
    "data", "info", "mech", "bot", "tron", "chip", "ware", "craft", "forge", "found",
    "mine", "source", "fuel", "power", "energy", "drive", "pulse", "beam", "wave", "flux",
    "space", "star", "planet", "world", "orbit", "astro", "cosmic", "solar", "lunar", "terra",
    "eco", "bio", "gen", "life", "med", "health", "care", "shield", "defense", "guard",
    "arms", "weapon", "force", "strike", "combat", "tactical", "strat", "command", "control"
]

corp_suffixes = [
    "Corp", "Corporation", "Incorporated", "Inc", "Industries", "Enterprises", "Group",
    "Consortium", "Conglomerate", "Holdings", "Partners", "Associates", "Alliance",
    "Federation", "Coalition", "Union", "United", "Collective", "Collaborative",
    "International", "Global", "Universal", "Galactic", "Interstellar", "Planetary",
    "Systems", "Solutions", "Innovations", "Technologies", "Dynamics", "Mechanics",
    "Robotics", "Cybernetics", "Networks", "Communications", "Transmissions",
    "Research", "Development", "Laboratories", "Sciences", "Applications", "Engineering",
    "Manufacturing", "Production", "Construction", "Fabrication", "Materials",
    "Resources", "Mining", "Excavation", "Exploration", "Surveying", "Shipping",
    "Transport", "Freight", "Logistics", "Distribution", "Trade", "Commerce",
    "Financial", "Investment", "Securities", "Ventures", "Capital", "Assets",
    "Limited", "LLC", "LTD", "Company", "Co", "Organization", "Foundation"
]

def get_corporation_name():
    """Generate a random corporation name"""
    name_type = random.randint(1, 6)
    
    if name_type == 1:
        # Prefix + Root + Suffix (e.g. "MegaTech Industries")
        return f"{random.choice(corp_prefixes)}{random.choice(corp_roots)} {random.choice(corp_suffixes)}"
    elif name_type == 2:
        # LastName + Suffix (e.g. "Andoria Corp")
        return f"{get_last_name()} {random.choice(corp_suffixes)}"
    elif name_type == 3:
        # LastName & LastName (e.g. "Weyland & Yutani")
        return f"{get_last_name()} & {get_last_name()}"
    elif name_type == 4:
        # FirstName LastName + Suffix (e.g. "Howard Industries")
        return f"{get_first_name()} {get_last_name()} {random.choice(corp_suffixes)}"
    elif name_type == 5:
        # The + Noun + Collective (e.g. "The Mining Collective")
        nouns = ["Mining", "Trading", "Shipping", "Manufacturing", "Engineering", "Research",
                "Development", "Exploration", "Defense", "Security", "Medical", "Agricultural",
                "Energy", "Technology", "Transport", "Salvage", "Recycling", "Terraforming",
                "Colonization", "Pharmaceutical", "Weapons", "Communications", "Entertainment"]
        collectives = ["Collective", "Alliance", "Consortium", "Union", "Federation", "Coalition",
                      "Syndicate", "Conglomerate", "Cooperative", "Association", "League",
                      "Network", "Brotherhood", "Society", "Community", "Guild", "Council"]
        return f"The {random.choice(nouns)} {random.choice(collectives)}"
    else:
        # Acronym (e.g. "UNATCO")
        length = random.randint(3, 5)
        return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length))
