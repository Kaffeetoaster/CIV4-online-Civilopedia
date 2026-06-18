from pathlib import Path
from enum import Enum, auto


import config
from python.helper.game_data.xml_parser import parse_xml_file, resolve_button_path
from python.helper.game_data.extractFontSymbols import *
from python.helper.measure_duration import measure, start_new_log
from python.gameContext.preprocess import add_index

### load xml infos ###
GlobalGameContext = {
    # BasicInfos
    "CONCEPTS": parse_xml_file(config.INPUT_PATH / "Assets/XML/BasicInfos/CIV4BasicInfos.xml"),
    "UNIT_COMBATS": parse_xml_file(config.INPUT_PATH / "Assets/XML/BasicInfos/CIV4UnitCombatInfos.xml"),
    
    "DOMAINS": parse_xml_file(config.INPUT_PATH.parent.parent / "Assets/XML/BasicInfos/CIV4DomainInfos.xml"),
    
    # Buildings
    "BUILDINGS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Buildings/CIV4BuildingInfos.xml"),
    "BUILDING_CLASSES": parse_xml_file(config.INPUT_PATH / "Assets/XML/Buildings/CIV4BuildingClassInfos.xml"),
    "SPECIAL_BUILDINGS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Buildings/CIV4SpecialBuildingInfos.xml"),
    
    # Civilizations
    "CIVILIZATIONS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Civilizations/CIV4CivilizationInfos.xml"),
    "LEADERHEADS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Civilizations/CIV4LeaderHeadInfos.xml"),

    # GameInfo
    "CIVICS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4CivicInfos.xml"),
    "CIVIC_OPTIONS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4CivicOptionInfos.xml"),
    
    "COMMERCE": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4CommerceInfo.xml"),
    
    "CORPORATIONS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4CorporationInfo.xml"),
    
    "GAME_SPEEDS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4GameSpeedInfo.xml"),
    
    "CULTURE_LEVELS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4CultureLevelInfo.xml"),
    
    "ERAS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4EraInfos.xml"),
    
    "PAGAN_RELIGIONS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4PaganReligionInfos.xml"),
    
    "PROJECTS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4ProjectInfo.xml"),
    
    "RELIGIONS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4ReligionInfo.xml"),
    
    "SPECIALISTS": parse_xml_file(config.INPUT_PATH / "Assets/XML/GameInfo/CIV4SpecialistInfos.xml"),
    
    # Interface
    "COLORS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Interface/CIV4ColorVals.xml"),
    "PLAYER_COLORS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Interface/CIV4PlayerColorInfos.xml"),
    
    "ADVISORS": parse_xml_file(config.INPUT_PATH.parent.parent.parent / "Assets/XML/Interface/CIV4AdvisorInfos.xml"),
    
    # Misc
    "ROUTES": parse_xml_file(config.INPUT_PATH / "Assets/XML/Misc/CIV4RouteInfos.xml"),
    
    # Technologies
    "TECHS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Technologies/CIV4TechInfos.xml"),
    
    # Terrain 
    "BONI": parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4BonusInfos.xml"),
    "FEATURES": parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4FeatureInfos.xml"),
    "IMPROVEMENTS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4ImprovementInfos.xml"),
    "TERRAINS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Terrain/CIV4TerrainInfos.xml"),
    "YIELDS": parse_xml_file(config.INPUT_PATH.parent.parent.parent / "Assets/XML/Terrain/CIV4YieldInfos.xml"),
   
   
    # Units
    "UNITS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Units/CIV4UnitInfos.xml"),
    "UNIT_CLASSES": parse_xml_file(config.INPUT_PATH / "Assets/XML/Units/CIV4UnitClassInfos.xml"),
    "SPECIAL_UNITS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Units/CIV4SpecialUnitInfos.xml"),
    
    "PROMOTIONS": parse_xml_file(config.INPUT_PATH / "Assets/XML/Units/CIV4PromotionInfos.xml"),
    
    
    
    
}




# Art
dArtXML = {}

for file in Path(config.INPUT_PATH / "Assets/XML/Art/").glob("*.xml"):
    dArtXML_temp = parse_xml_file(file)
    dArtXML |= dArtXML_temp
    #print(f"Loaded {len(dArtXML_temp)} Art XML entries from {file.name}")
print(f"Loaded {len(dArtXML)} Art XML entries in total.")

GlobalGameContext["ART"] = dArtXML


# Text
dTextXML = {}
dTextXMLBase = {}
for file in Path(config.INPUT_PATH.parent.parent.parent / "Assets/XML/Text/").rglob("*.xml"):
    dTextXML_temp = parse_xml_file(file)
    dTextXMLBase |= dTextXML_temp
    #print(f"Loaded {len(dTextXML_temp)} Text XML entries from {file.name}")
dTextXML |= dTextXMLBase
print(f"Loaded {len(dTextXMLBase)} basegame Text XML entries in total.")

dTextXMLBTS = {}
for file in Path(config.INPUT_PATH.parent.parent.parent / "Beyond the Sword/Assets/XML/Text/").rglob("*.xml"):
    dTextXML_temp = parse_xml_file(file)
    dTextXMLBTS |= dTextXML_temp
    #print(f"Loaded {len(dTextXML_temp)} BTS Text XML entries from {file.name}")
dTextXML |= dTextXMLBTS
print(f"Loaded {len(dTextXMLBTS)} BTS Text XML entries.")


dTextXMLWarlords = {}
for file in Path(config.INPUT_PATH.parent.parent.parent / "Warlords/Assets/XML/Text/").rglob("*.xml"):
    dTextXML_temp = parse_xml_file(file)
    dTextXMLWarlords |= dTextXML_temp
    #print(f"Loaded {len(dTextXML_temp)} Warlords Text XML entries from {file.name}")
dTextXML |= dTextXMLWarlords
print(f"Loaded {len(dTextXMLWarlords)} Warlords Text XML entries")


dTextXMLMod = {}
for file in Path(config.INPUT_PATH / "Assets/XML/Text/").rglob("*.xml"):
    dTextXML_temp = parse_xml_file(file)
    dTextXMLMod |= dTextXML_temp
    #print(f"Loaded {len(dTextXML_temp)} Text XML entries from {file.name}")
dTextXML |= dTextXMLMod
print(f"Loaded {len(dTextXMLMod)} Mod Text XMl entries. Now total count is {len(dTextXML)}")





GlobalGameContext["TEXT"] = dTextXML



# contains all symbols with the id/place in the fontatlas gamefont_75 and a default dispaly string
SYMBOLS = {
    "YIELD_FOOD_CHAR": {"ID": "04_00", "display": "food"},
    "YIELD_PRODUCTION_CHAR": {"ID": "04_01", "display": "production"},
    "YIELD_COMMERCE_CHAR": {"ID": "04_02", "display": "commerce"},
    
    "COMMERCE_GOLD_CHAR": {"ID": "05_00","display":"gold"},
    "COMMERCE_RESEARCH_CHAR": {"ID": "05_01","display":"research"},
    "COMMERCE_CULTURE_CHAR": {"ID": "05_02","display":"culture"}, 
    "COMMERCE_ESPIONAGE_CHAR": {"ID": "05_03","display":"espionage"},
    
    "RELIGION_JUDAISM_CHAR": {"ID": "07_00", "display": "judanism"},
    "RELIGION_JUDAISM_STATE_CHAR": {"ID": "07_01", "display": "judaism"},
    "RELIGION_ORTHODOXY_CHAR": {"ID": "07_02", "display": "orthodoxy"},
    "RELIGION_ORTHODOXY_STATE_CHAR": {"ID": "07_05", "display": "orthodoxy"},
    "RELIGION_CATHOLICISM_CHAR": {"ID": "07_06", "display": "catholicism"},
    "RELIGION_CATHOLICISM_STATE_CHAR": {"ID": "07_07", "display": "catholicism"},
    "RELIGION_PROTESTANTISM_CHAR": {"ID": "07_08", "display": "protestantism"},
    "RELIGION_PROTESTANTISM_STATE_CHAR": {"ID": "07_09", "display": "protestantism"},
    "RELIGION_ISLAM_CHAR": {"ID": "07_10", "display": "islam"},
    "RELIGION_ISLAM_STATE_CHAR": {"ID": "07_11", "display": "islam"},
    "RELIGION_HINDUISM_CHAR": {"ID": "07_12", "display": "hinduism"},
    "RELIGION_HINDUISM_STATE_CHAR": {"ID": "07_13", "display": "hinduism"},
    "RELIGION_BUDDHISM_CHAR": {"ID": "07_14", "display": "buddhism"},
    "RELIGION_BUDDHISM_STATE_CHAR": {"ID": "07_15", "display": "buddhism"},
    "RELIGION_CONFUCIANISM_CHAR": {"ID": "07_16", "display": "confucianism"},
    "RELIGION_CONFUCIANISM_STATE_CHAR": {"ID":"07_17", "display": "confucianism"},
    "RELIGION_TAOISM_CHAR": {"ID": "07_18", "display": "taoism"},
    "RELIGION_TAOISM_STATE_CHAR": {"ID": "07_20", "display": "taoism"},
    "RELIGION_ZOROASTRIANISM_CHAR": {"ID": "07_21", "display": "zoroastrianism"},
    "RELIGION_ZOROASTRIANISM_STATE_CHAR": {"ID": "07_22", "display": "zoroastrianism"},



    "HAPPY_CHAR": {"ID": "12_00", "display": "happy"},
	"UNHAPPY_CHAR": {"ID": "12_01", "display": "unhappy"},
	"HEALTHY_CHAR": {"ID": "12_02", "display": "healthy"},
	"UNHEALTHY_CHAR": {"ID": "12_03", "display": "unhealthy"},
    "BULLET_CHAR": {"ID": "12_04", "display": "bulletpoint"},
	"STRENGTH_CHAR": {"ID": "12_05", "display": "strength"},
	"MOVES_CHAR": {"ID": "12_06", "display": "moves"},
	"RELIGION_CHAR": {"ID": "12_07", "display": "religion"},
	"STAR_CHAR": {"ID": "12_08", "display": "star"},
	"SILVER_STAR_CHAR": {"ID": "12_09", "display": "silver star"},
	"TRADE_CHAR": {"ID": "12_10", "display": "trade"},
	"DEFENSE_CHAR": {"ID": "12_11", "display": "defense"},
	"GREAT_PEOPLE_CHAR": {"ID": "12_12", "display": "great people"},
	"BAD_GOLD_CHAR": {"ID": "12_13", "display": "bad gold"},
	"BAD_FOOD_CHAR": {"ID": "12_14", "display": "bad food"},
	"EATEN_FOOD_CHAR": {"ID": "12_15", "display": "eaten food"},
	"GOLDEN_AGE_CHAR": {"ID": "12_16", "display": "golden age"},
	"ANGRY_POP_CHAR": {"ID": "12_17", "display": "angry population"},
	"OPEN_BORDERS_CHAR": {"ID": "12_18", "display": "open borders"},
	"DEFENSIVE_PACT_CHAR": {"ID": "12_19", "display": "defensive pact"},
	"MAP_CHAR": {"ID": "12_20", "display": "map"},
	"OCCUPATION_CHAR": {"ID": "12_21", "display": "occupation"},
	"POWER_CHAR": {"ID": "12_22", "display": "power"},
    
	"CLEAN_POWER_CHAR": {"ID": "13_19", "display": "clean power"},
}

FontSymbols = [
    
	"CITIZEN_CHAR",
	"GENERAL_CHAR",
	"RELATION_CHAR",
	"FURIOUS_CHAR",
	"ANNOYED_CHAR",
	"CAUTIOUS_CHAR",
	"PLEASED_CHAR",
	"FRIENDLY_CHAR",
	"CROSS_CHAR",
	"COLLAPSING_CHAR",
	"UNSTABLE_CHAR",
	"SHAKY_CHAR",
	"STABLE_CHAR",
	"SOLID_CHAR",
	"PLAGUE_CHAR",
	"UP_CHAR",
	"EQUAL_CHAR",
	"DOWN_CHAR",
	"SUCCESS_CHAR",
	"FAILURE_CHAR",
	"SCALES_CHAR",
	"AIRPORT_CHAR",
	"SATELLITE_CHAR",
]

# contains paths to extrcated font symbols
FONTSYMBOLS_75 = extract_glyphs_from_tga(INPUT_TGA_GAMEFONT_75, OUTPUT_DIR_GAMEFONT_75, GAME_FONT_75_ROW_BLOCKS, ALPHA_THRESHOLD)
GlobalGameContext["FONT_SYMBOLS_75"] = FONTSYMBOLS_75

# FONTSYMBOLS = extract_glyphs_from_tga(INPUT_TGA_GAMEFONT, OUTPUT_DIR_GAMEFONT, GAME_FONT_ROW_BLOCKS, ALPHA_THRESHOLD)
# GlobalGameContext["FONT_SYMBOLS"] = FONTSYMBOLS

GlobalGameContext["SYMBOLS"] = SYMBOLS

### Constants
TEMPLES_NEEDED_MULTIPLIKATOR = 2 # Temples for Cathedrals




# Preprocessing

## adding indices to entries for easier access and reference
def add_indices():
    add_index(GlobalGameContext["CULTURE_LEVELS"])
    add_index(GlobalGameContext["ERAS"])
measure(add_indices)

## reference to own category.
def add_category_reference():
    for Category, Objects in GlobalGameContext.items():
        if isinstance(Objects, dict):
            for key, entry_dict in Objects.items():
                entry_dict["GameObjectCategory"] = Category
measure(add_category_reference)     
       
## resolving button paths
def resolve_button_entries():
    for Category, Objects in GlobalGameContext.items():
        if isinstance(Objects, dict):
            for ObjectKey, ObjectValues in Objects.items():
                file_name = ObjectKey
                new_file_name = f"{Category}/{file_name}"
                resolve_button_path(ObjectValues, new_file_name)
measure(resolve_button_entries)