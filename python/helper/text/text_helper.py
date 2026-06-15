from python.gameContext.game import GlobalGameContext
from config import OUTPUT_PATH
from PIL import Image
from pathlib import Path
# provides helper functions for 
### text formatting
### html generation
### getting game object infos 

GC = GlobalGameContext


def format_text(text, var):
	return text.replace("%d1", str(var))


def get_text(key):
	return GlobalGameContext["TEXT"].get(key, {}).get("English", key)


def getFontSymbol(symbol_key):
	symbol = GlobalGameContext["SYMBOLS"].get(symbol_key, symbol_key)
	return symbol.get("display", symbol_key)


	
### HTML generation for symbols and links

def getHTMLForFontSymbol(symbol_key):
	symbol = GlobalGameContext["SYMBOLS"].get(symbol_key, symbol_key)
	if symbol != None:
		source = f"glyph_r{symbol.get('ID', symbol_key)}.png"
		name = symbol.get("display", symbol_key)

	return f'<img src="/Assets/Symbols/font_75/{source}" alt="{name}" class="symbol">'
	
def getHTMLLinkForText(OGameObject):
	if OGameObject is None:
		return ""
	else:
		text = get_text(OGameObject.get("Description", ""))
		Category = OGameObject.get("GameObjectCategory", "Unknown_Category").capitalize()
		link = f"/Categories/{Category}/#{text.replace(" ", "-")}" 
	return f'<a class="text-link" href="{link}" title="{text}">{text}</a>'


def getHTMLLinkForButton(OGameObject):
	if OGameObject is None:
		return ""
	else: 
		if "ArtDefineTag" in OGameObject.keys():
			art_tag = OGameObject.get("ArtDefineTag", "")
			art = GlobalGameContext["ART"].get(art_tag, {})
			button_path = art.get("Button", "")
		elif "Button" in OGameObject.keys():
			button_path = OGameObject.get("Button", "")
		else:
			button_path = ""
	if button_path != "":
		button_path = str(Path(button_path).relative_to(OUTPUT_PATH))
	text = get_text(OGameObject.get("Description", "")) 
	Category = OGameObject.get("GameObjectCategory", "Unknown_Category").capitalize()
	link = f"/Categories/{Category}/#{text.replace(" ", "-") }"
		
	return f'<a href="{link}" title="{text}"><img src="/{button_path}" alt="{text}">  </a>'


### GameObject help

def getBuildingHelp(OBuilding):
	Entry = []
	return Entry


def getUnitHelp(OUnit):
	Entry = []
	return Entry









### styling

def addBulletpoints(contentList):
	dot = getHTMLForFontSymbol("BULLET_CHAR")
	return [f"{dot} {item}" for item in contentList]








### getting game Infos

def getYieldInfos(OBuilding):
	YieldInfos = []
	YieldModifiers = OBuilding.get("YieldChanges", {}).get("iYield", [])
	for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
		iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
		Symbol_Key = f"{Yield['Type']}_CHAR"
		YieldInfos.append([iYieldModifier, Symbol_Key])
	
	return YieldInfos

def getSeaPlotYieldChanges(OBuilding):
	YieldInfos = []
	YieldModifiers = OBuilding.get("SeaPlotYieldChanges", {}).get("iYield", [])
	for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
		iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
		Symbol_Key = f"{Yield['Type']}_CHAR"
		YieldInfos.append([iYieldModifier, Symbol_Key])
	
	return YieldInfos

def getFlatRiverPlotYieldChanges(OBuilding):
	YieldInfos = []
	YieldModifiers = OBuilding.get("FlatRiverPlotYieldChanges", {}).get("iYield", [])
	for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
		iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
		Symbol_Key = f"{Yield['Type']}_CHAR"
		YieldInfos.append([iYieldModifier, Symbol_Key])
	
	return YieldInfos


def getCommerceInfos(OBuilding):
	CommerceInfos = []
	CommerceModifiers = OBuilding.get("CommerceChanges", {}).get("iCommerce", [])
	ObsoleteSafeCommerceModifiers = OBuilding.get("ObsoleteSafeCommerceChanges", {}).get("iCommerce", [])
	for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
		iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
		iObsoleteSafeCommerceModifier = int(ObsoleteSafeCommerceModifiers[i]) if len(ObsoleteSafeCommerceModifiers) > i else 0
		Symbol_Key = f"{Commerce["Type"]}_CHAR"
		CommerceInfos.append([iCommerceModifier + iObsoleteSafeCommerceModifier, Symbol_Key])
	
	return CommerceInfos

def getCultureCommmerceInfos(OBuilding):
	CommerceInfos = []
	CommerceModifiers = OBuilding.get("CultureCommerceModifiers", {}).get("iCommerce", [])
	for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
		iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
		Symbol_Key = f"{Commerce['Type']}_CHAR"
		CommerceInfos.append([iCommerceModifier, Symbol_Key])
	
	return CommerceInfos



def getBuildingCategory(OBuilding):
	# 0: normal building
	# 1: religious building
	# 2: unique building
	# 3: great people building
	# 4: national wonder
	# 5: great wonder
	BuildingClass = GC["BUILDING_CLASSES"].get(OBuilding.get("BuildingClass", ""), {})
	
	if int(BuildingClass.get("iMaxGlobalInstances")) == 1 and OBuilding.get("HolyCity", None) is None:
		return 5 # great wonder
	if int(BuildingClass.get("iMaxPlayerInstances")) == 1:
		return 4 # national wonder
	GreatPeopleBuildings = getGreatPeopleBuildings()
	if OBuilding["Type"] in GreatPeopleBuildings:
		return 3 # great people building
	
	if BuildingClass.get("DefaultBuilding") != OBuilding["Type"]:
		return 2 # unique building
	
	if OBuilding.get("ReligionType", None) is not None or OBuilding.get("HolyCity", None) is not None:
		return 1 # religious building
	return 0 # normal building

def getGreatPeopleBuildings():
	res = set()
	for OUnit in GlobalGameContext["UNITS"].values():
		building = OUnit.get("Buildings", None)
		# The Shrines are in a list and will be ignored here.
		if building is not None and isinstance(building["Building"], dict):
			res.add(building["Building"]["BuildingType"])
	return res


# Religion prereq for Buildings
def getReligionPrereqString(OBuilding):        
	Religion1  = getHTMLLinkForButton(GC["RELIGIONS"].get(OBuilding.get("PrereqReligion", None), None))
	Religion2 = getHTMLLinkForButton(GC["RELIGIONS"].get(OBuilding.get("OrPrereqReligion", None), None))
	StateReligion1 = getHTMLLinkForButton(GC["RELIGIONS"].get(OBuilding.get("StateReligion", None), None))
	StateReligion2 = getHTMLLinkForButton(GC["RELIGIONS"].get(OBuilding.get("OrStateReligion", None), None))
	
	PrereqString = ""
	if Religion1 != "":
		if Religion2 != "":
			PrereqString = f"({Religion1} or {Religion2}) in City"
		else:
			PrereqString = f"{Religion1} in City"

	StateReligionString = ""
	if StateReligion1 != "":
		if StateReligion2 != "":
			StateReligionString = f"({StateReligion1} or {StateReligion2}) as State Religion"
		else:
			StateReligionString = f"{StateReligion1} as State Religion"

	comma = " and " if StateReligionString != "" and PrereqString != "" else ""
	return f"{StateReligionString}{comma}{PrereqString}"


# Abstract function to get a string of HTMlButtonLinks
def getPrereqHTMLbuttons(OGameObject, key_outer, key_inner,Category):
    # key_outer: the key of the prereq in the game object, e.g. "PrereqBonuses"
	# key_inner: the key of the prereq in the prereq object, e.g. "Bonus"
	# The Category to get the actual Objects from, e.g. "BONUSES"
	content = ""
	Prereq = OGameObject.get(key_outer, {})
	if isinstance(Prereq, str):
		Prereq = [Prereq]
	else:
		Prereq = Prereq.get(key_inner, [])
		if isinstance(Prereq, dict):
			Prereq = [Prereq]
	if isinstance(Prereq, list):
		for req in Prereq:
			OReq = GC[Category].get(req, None)
			if OReq is not None:
				button = getHTMLLinkForButton(OReq)
				content += button







## sorting

def sortBuildingsByEra(Buildings):
	for OBuilding in Buildings:
		OTech = GlobalGameContext["TECHS"].get(OBuilding.get("PrereqTech", ""), {})
		OEra = OTech.get("Era", "")
		OBuilding["EraID"] = int(GlobalGameContext["ERAS"].get(OEra, {}).get("index", 0))
	
	# sort buildings by era, then by name
	
	Buildings.sort(key=lambda b: (b.get("EraID", 0), get_text(b.get("Description", ""))))