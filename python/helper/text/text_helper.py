from python.gameContext.game import GlobalGameContext, TEMPLES_NEEDED_MULTIPLIKATOR
from config import OUTPUT_PATH
from PIL import Image
from pathlib import Path
import re
# provides helper functions for 
### text formatting
### html generation
### getting game object infos 

GC = GlobalGameContext


def format_text(text, var):
    return text.replace("%d1", str(var))

def get_text(key):
    return resolve_formattingTags(GC["TEXT"].get(key, {}).get("English", key))

def resolve_formattingTags(text):
    ## used to interpret the [..] tags in some Pedia and Strategy texts
    replacements = {
    "ICON_PRODUCTION": getHTMLForFontSymbol("YIELD_PRODUCTION_CHAR"),
    "ICON_FOOD": getHTMLForFontSymbol("YIELD_FOOD_CHAR"),
    "ICON_COMMERCE": getHTMLForFontSymbol("YIELD_COMMERCE_CHAR"),
    
    "ICON_GREATPEOPLE": getHTMLForFontSymbol("GREAT_PEOPLE_CHAR"),
    
    "ICON_GOLD": getHTMLForFontSymbol("COMMERCE_GOLD_CHAR"),
    "ICON_RESEARCH": getHTMLForFontSymbol("COMMERCE_RESEARCH_CHAR"),
    "ICON_CULTURE": getHTMLForFontSymbol("COMMERCE_CULTURE_CHAR"),
    "ICON_ESPIONAGE": getHTMLForFontSymbol("COMMERCE_ESPIONAGE_CHAR"),
    
    "NEWLINE": f" and ",
    "TAB": "<br>"
    }
    return re.sub(r"\[([^\]]+)\]", lambda m: replacements.get(m.group(1), ""), text)
    
def getFontSymbol(symbol_key):
    symbol = GlobalGameContext["SYMBOLS"].get(symbol_key, symbol_key)
    return symbol.get("display", symbol_key)
    
### HTML generation for symbols and links

def getHTMLForFontSymbol(symbol_key):
    symbol = GlobalGameContext["SYMBOLS"].get(symbol_key, symbol_key)
    if symbol != None:
        source = f"glyph_r{symbol.get('ID', symbol_key)}.png"
        name = symbol.get("display", symbol_key)
    return f'<img src="/Assets/Symbols/font_75/{source}" alt="{name}" class="Symbol">'
    
def getHTMLLinkForText(OGameObject):
    if OGameObject is None:
        return ""
    else:
        text = get_text(OGameObject.get("Description", ""))
        Category = getPediaCategory(OGameObject)
        link = f"/Categories/{Category}/#{text.replace(" ", "-").lower()}" 
    return f'<a class="text-link" href="{link}" title="{text}">{text}</a>'

def getPediaCategory(OGameObject):
    if OGameObject is None:
        return "Unknown_Category"
    
    # Buildings
    if OGameObject.get("GameObjectCategory", None) == "BUILDINGS":
        cat = getBuildingCategory(OGameObject)
        match cat:
            case 5:
                return "GreatWonders"
            case 4:
                return "NationalWonders"
            case 3:
                return "GreatPeopleBuildings"
            case 2:
                return "UniqueBuildings"
            case 1:
                return "ReligiousBuildings"
            case _:
                return "Buildings"
    # Units
    elif OGameObject.get("GameObjectCategory", None) == "UNITS":
        return "Units"
    
    
    return OGameObject.get("GameObjectCategory", "Unknown_Category").capitalize()    
        
        
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
    Category = getPediaCategory(OGameObject)
    link = f"/Categories/{Category}/#{text.replace(" ", "-").lower()}"
        
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
    YieldModifiers = getNestedTag(OBuilding, "YieldChanges", "iYield")
    for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
        iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
        Symbol_Key = f"{Yield['Type']}_CHAR"
        YieldInfos.append([iYieldModifier, Symbol_Key])
    return YieldInfos

def getYieldModifiers(OBuilding):
    YieldInfos = []
    YieldModifiers = getNestedTag(OBuilding, "YieldModifiers", "iYield")
    for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
        iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
        Symbol_Key = f"{Yield['Type']}_CHAR"
        YieldInfos.append([iYieldModifier, Symbol_Key])
    return YieldInfos

def getSeaPlotYieldChanges(OBuilding):
    YieldInfos = []
    YieldModifiers = getNestedTag(OBuilding, "SeaPlotYieldChanges", "iYield")
    for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
        iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
        Symbol_Key = f"{Yield['Type']}_CHAR"
        YieldInfos.append([iYieldModifier, Symbol_Key])
    return YieldInfos

def getFlatRiverPlotYieldChanges(OBuilding):
    YieldInfos = []
    YieldModifiers = getNestedTag(OBuilding, "FlatRiverPlotYieldChanges", "iYield")
    for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
        iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
        Symbol_Key = f"{Yield['Type']}_CHAR"
        YieldInfos.append([iYieldModifier, Symbol_Key])
    return YieldInfos


def getCommerceModifiers(OBuilding):
    CommerceInfos = []
    CommerceModifiers = getNestedTag(OBuilding, "CommerceModifiers", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
        Symbol_Key = f"{Commerce['Type']}_CHAR"
        CommerceInfos.append([iCommerceModifier, Symbol_Key])
    return CommerceInfos

def getCommerceChanges(OBuilding):
    CommerceInfos = []
    CommerceChanges = getNestedTag(OBuilding, "CommerceChanges", "iCommerce")
    ObsoleteSafeCommerceChanges = getNestedTag(OBuilding, "ObsoleteSafeCommerceChanges", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceChanges[i]) if len(CommerceChanges) > i else 0
        iObsoleteSafeCommerceModifier = int(ObsoleteSafeCommerceChanges[i]) if len(ObsoleteSafeCommerceChanges) > i else 0
        Symbol_Key = f"{Commerce["Type"]}_CHAR"
        CommerceInfos.append([iCommerceModifier + iObsoleteSafeCommerceModifier, Symbol_Key])
    return CommerceInfos

def getCommerceHappinessModifiers(OBuilding):
    CommerceInfos = []
    CommerceHappinessModifiers = getNestedTag(OBuilding, "CommerceHappinesses", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceHappinessModifiers[i]) if len(CommerceHappinessModifiers) > i else 0
        iCommerceModifier = 100//iCommerceModifier if iCommerceModifier != 0 else 0  # convert to per percent value
        Symbol_Key = f"{Commerce['Type']}_CHAR"
        Symbol_Happiness = getHTMLForFontSymbol("HAPPY_CHAR")
        if iCommerceModifier > 0:
            CommerceInfos.append(f"+1{Symbol_Happiness} per {iCommerceModifier}% {getHTMLForFontSymbol(Symbol_Key)} Rate")
    return ", ".join(CommerceInfos)


def getCultureCommerceInfos(OBuilding):
    CommerceInfos = []
    CommerceModifiers = getNestedTag(OBuilding, "CultureCommerceModifiers", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
        Symbol_Key = f"{Commerce['Type']}_CHAR"
        CommerceInfos.append([iCommerceModifier, Symbol_Key])
    return CommerceInfos

def getSpecialistExtraCommerces(OBuilding):
    CommerceInfos = []
    CommerceModifiers = getNestedTag(OBuilding, "SpecialistExtraCommerces", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
        Symbol_Key = f"{Commerce['Type']}_CHAR"
        CommerceInfos.append([iCommerceModifier, Symbol_Key])
    return CommerceInfos

def getStateReligionCommerces(OBuilding):
    CommerceInfos = []
    CommerceModifiers = getNestedTag(OBuilding, "StateReligionCommerces", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
        Symbol_Key = f"{Commerce['Type']}_CHAR"
        CommerceInfos.append([iCommerceModifier, Symbol_Key])
    return CommerceInfos


def getBonusYieldChanges(OBuilding):
    info = {}
    Changes = [] # list of strings
    BonusYieldChanges = getNestedTag(OBuilding, "BonusYieldChanges", "BonusYieldChange")
    for BonusYieldChange in BonusYieldChanges:
        Bonus = GC["BONI"].get(BonusYieldChange.get("BonusType", ""), None)
        YieldChanges = getYieldInfos(BonusYieldChange)
        YieldChangesStr = ", ".join([f"+{change[0]} {getHTMLForFontSymbol(change[1])}" for change in YieldChanges if change[0]>0])
        if Bonus is not None and YieldChanges != []:
            Boni = info.get(YieldChangesStr, [])
            if Boni == []:
                info[YieldChangesStr] = [getHTMLLinkForText(Bonus)]
            else:
                Boni.append(getHTMLLinkForText(Bonus))
    for YieldChangesStr, BonusLink in info.items():
        infstr = f"{YieldChangesStr} on improved {' , '.join(BonusLink)} resources"
        Changes.append(infstr)
    return Changes

def getBonusYieldModifiers(OBuilding):
    info = {}
    Changes = [] # list of strings
    BonusYieldModifiers = getNestedTag(OBuilding, "BonusYieldModifiers", "BonusYieldModifier")
    for BonusYieldModifier in BonusYieldModifiers:
        Bonus = GC["BONI"].get(BonusYieldModifier.get("BonusType", ""), None)
        YieldModifers = getYieldModifiers(BonusYieldModifier)
        
        YieldModifiersStr = ", ".join([f"+{change[0]}% {getHTMLForFontSymbol(change[1])}" for change in YieldModifers if change[0]>0])
        if Bonus is not None and YieldModifers != []:
            Boni = info.get(YieldModifiersStr, [])
            if Boni == []:
                info[YieldModifiersStr] = [getHTMLLinkForText(Bonus)]
            else:
                Boni.append(getHTMLLinkForText(Bonus))
    for YieldModifiersStr, Boni in info.items():
        infstr = f"{YieldModifiersStr} from {' , '.join(Boni)}"
        Changes.append(infstr)
    return Changes

def getBonusHealthChanges(OBuilding):
    info = {}
    Changes = [] # list of strings
    BonusHealthChanges = getNestedTag(OBuilding, "BonusHealthChanges", "BonusHealthChange")
    for BonusHealthChange in BonusHealthChanges:
        Bonus = GC["BONI"].get(BonusHealthChange.get("BonusType", ""), None)
        iHealthChange = BonusHealthChange.get("iHealthChange", "")
        if Bonus is not None and iHealthChange != "":
            Boni = info.get(iHealthChange, [])
            if Boni == []:
                info[iHealthChange] = [getHTMLLinkForText(Bonus)]
            else:
                Boni.append(getHTMLLinkForText(Bonus))
    for iHealthChange, Boni in info.items():
        if int(iHealthChange) > 0:
            Symbol = getHTMLForFontSymbol("HEALTHY_CHAR")
        elif int(iHealthChange) < 0:
            Symbol = getHTMLForFontSymbol("UNHEALTHY_CHAR")
            iHealthChange = abs(int(iHealthChange))
        infstr = f"+{iHealthChange} {Symbol} from {", ".join(Boni)}"
        Changes.append(infstr)
    return Changes

def getBonusHappinessChanges(OBuilding):
    # orders the happiness changes by the amount of happiness change, adds the symbol and returns a list of strings, eg +1 :) for ....
    info = {}
    Changes = [] # list of strings
    BonusHappinessChanges = getNestedTag(OBuilding, "BonusHappinessChanges", "BonusHappinessChange")
    for BonusHappinessChange in BonusHappinessChanges:
        Bonus = GC["BONI"].get(BonusHappinessChange.get("BonusType", ""), None)
        iHappinessChange = BonusHappinessChange.get("iHappinessChange", "")
        if Bonus is not None and iHappinessChange != "":
            Boni = info.get(iHappinessChange, [])
            if Boni == []:
                info[iHappinessChange] = [getHTMLLinkForText(Bonus)]
            else:
                Boni.append(getHTMLLinkForText(Bonus))
    for iHappinessChange, Boni in info.items():
        if int(iHappinessChange) > 0:
            Symbol = getHTMLForFontSymbol("HAPPY_CHAR")
        elif int(iHappinessChange) < 0:
            Symbol = getHTMLForFontSymbol("UNHAPPY_CHAR")
            iHappinessChange = abs(int(iHappinessChange))
        infstr = f"+{iHappinessChange} {Symbol} from {', '.join(Boni)}"
        Changes.append(infstr)
    return Changes

## Powereffects

def getPowerYieldModifiers(OBuilding):
    YieldInfos = []
    YieldModifiers = getNestedTag(OBuilding, "PowerYieldModifiers", "iYield")
    for i, Yield in enumerate(GlobalGameContext["YIELDS"].values()):
        iYieldModifier = int(YieldModifiers[i]) if len(YieldModifiers) > i else 0
        Symbol_Key = f"{Yield['Type']}_CHAR"
        YieldInfos.append([iYieldModifier, Symbol_Key])
    return YieldInfos

def getPowerCommerceModifiers(OBuilding):
    CommerceInfos = []
    CommerceModifiers = getNestedTag(OBuilding, "PowerCommerceModifiers", "iCommerce")
    for i, Commerce in enumerate(GlobalGameContext["COMMERCE"].values()):
        iCommerceModifier = int(CommerceModifiers[i]) if len(CommerceModifiers) > i else 0
        Symbol_Key = f"{Commerce['Type']}_CHAR"
        CommerceInfos.append([iCommerceModifier, Symbol_Key])
    return CommerceInfos

### Units and XP
def getDomainFreeExperiences(OBuilding):
    ExperienceInfos = []
    DomainFreeExperiences = getNestedTag(OBuilding, "DomainFreeExperiences", "DomainFreeExperience")
    for DomainFreeExperience in DomainFreeExperiences:
        Domain = GC["DOMAINS"].get(DomainFreeExperience.get("DomainType", ""), None)
        iExperience = int(DomainFreeExperience.get("iExperience", 0))
        if Domain is not None and iExperience > 0:
            ExperienceInfos.append(f"New {get_text(Domain['Description'])} receive +{iExperience} Experience Points")
    return ExperienceInfos
            
def getUnitCombatFreeExperiences(OBuilding):
    ExperienceInfos = []
    UnitCombatFreeExperiences = getNestedTag(OBuilding, "UnitCombatFreeExperiences", "UnitCombatFreeExperience")
    for UnitCombatFreeExperience in UnitCombatFreeExperiences:
        UnitCombat = GC["UNIT_COMBATS"].get(UnitCombatFreeExperience.get("UnitCombatType", ""), None)
        iExperience = int(UnitCombatFreeExperience.get("iExperience", 0))
        if UnitCombat is not None and iExperience > 0:
            ExperienceInfos.append(f"New {get_text(UnitCombat['Description'])} receive +{iExperience} Experience Points")
    return ExperienceInfos

def getSpecialistCount(OBuilding):
    info = {}
    Changes = [] # list of strings
    SpecialistCounts = getNestedTag(OBuilding, "SpecialistCounts", "SpecialistCount")
    for SpecialistCount in SpecialistCounts:
        Specialist = GC["SPECIALISTS"].get(SpecialistCount.get("SpecialistType", ""), None)
        iSpecialistCount = SpecialistCount.get("iSpecialistCount", "")
        if Specialist is not None and iSpecialistCount != "":
            Boni = info.get(iSpecialistCount, [])
            if Boni == []:
                info[iSpecialistCount] = [getHTMLLinkForText(Specialist)]
            else:
                Boni.append(getHTMLLinkForText(Specialist))
    for iSpecialistCount, Boni in info.items():
        infstr = f"Can turn {iSpecialistCount} Citizen(s) into {', '.join(Boni)}"
        Changes.append(infstr)
    return Changes

def getFreeSpecialistCounts(OBuilding):
    info = {}
    Changes = [] # list of strings
    FreeSpecialistCounts = getNestedTag(OBuilding, "FreeSpecialistCounts", "SpecialistCount")
    for FreeSpecialistCount in FreeSpecialistCounts:
        Specialist = GC["SPECIALISTS"].get(FreeSpecialistCount.get("SpecialistType", ""), None)
        iFreeSpecialistCount = FreeSpecialistCount.get("iSpecialistCount", "")
        if Specialist is not None and iFreeSpecialistCount != "":
            Boni = info.get(iFreeSpecialistCount, [])
            if Boni == []:
                info[iFreeSpecialistCount] = [getHTMLLinkForText(Specialist)]
            else:
                Boni.append(getHTMLLinkForText(Specialist))
    for iFreeSpecialistCount, Boni in info.items():
        infstr = f"Provides {iFreeSpecialistCount} free {', '.join(Boni)}"
        Changes.append(infstr)
    return Changes

def getDomainProductionModifiers(OBuilding):
    info = {}
    Modifiers = []
    DomainProductionModifiers = getNestedTag(OBuilding, "DomainProductionModifiers", "DomainProductionModifier")
    for DomainProductionModifier in DomainProductionModifiers:
        Domain = GC["DOMAINS"].get(DomainProductionModifier.get("DomainType", ""), None)
        iProductionModifier = DomainProductionModifier.get("iProductionModifier", "")
        if Domain is not None and iProductionModifier != "":
            Modifier = info.get(iProductionModifier, [])
            if Modifier == []:
                info[iProductionModifier] = [get_text(Domain["Description"])]
            else:
                Modifier.append(get_text(Domain["Description"]))
    for iProductionModifier, Domain in info.items():
        infstr = f"Builds {', '.join(Domain)} +{iProductionModifier}%  faster "
        Modifiers.append(infstr)
    return Modifiers

def getBonusProductionModifiers(OBuilding):
    info = {}
    Changes = [] # list of strings
    BonusProductionModifiers = getNestedTag(OBuilding, "BonusProductionModifiers", "BonusProductionModifier")
    for BonusProductionModifier in BonusProductionModifiers:
        Bonus = GC["BONI"].get(BonusProductionModifier.get("BonusType", ""), None)
        iProductionModifier = BonusProductionModifier.get("iProductonModifier", "")
        
        if Bonus is not None and iProductionModifier != "":
            Modifier = info.get(iProductionModifier, [])
            if Modifier == []:
                info[iProductionModifier] = [getHTMLLinkForText(Bonus)]
            else:
                Modifier.append(getHTMLLinkForText(Bonus))
    for iProductionModifier, Boni in info.items():
        infstr = f"+{iProductionModifier}% Production Speed with {', '.join(Boni)}"
        Changes.append(infstr)
    return Changes

def getCivicProductionModifiers(OBuilding):
    Modifiers = []
    for OCivic in GC["CIVICS"].values():
        CivicProductionModifiers = getBuildingProductionModifiers(OCivic)
        for CivicProductionModifier in CivicProductionModifiers:
            if CivicProductionModifier[1] == OBuilding["BuildingClass"]:
                iProductionModifier = CivicProductionModifier[0]
                Modifiers.append(f"+{iProductionModifier}% Production Speed with {getHTMLLinkForText(OCivic)}")
    return Modifiers

def getCivicHappinessChanges(OBuilding):
    Changes = []
    for OCivic in GC["CIVICS"].values():
        CivicHappinessChanges = getBuildingHappinessChanges(OCivic)
        for CivicHappinessChange in CivicHappinessChanges:
            if CivicHappinessChange[1] == OBuilding["BuildingClass"]:
                iHappinessChange = CivicHappinessChange[0]
                if iHappinessChange > 0:
                    Symbol = getHTMLForFontSymbol("HAPPY_CHAR")
                elif iHappinessChange < 0:
                    Symbol = getHTMLForFontSymbol("UNHAPPY_CHAR")
                    iHappinessChange = abs(iHappinessChange)
                Changes.append(f"+{iHappinessChange} {Symbol} with {getHTMLLinkForText(OCivic)}")
    return Changes

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

def getReplacementBuildings(OBuilding):
    BuildingClass = GC["BUILDING_CLASSES"].get(OBuilding.get("BuildingClass", ""), {})
    Replacements = []
    if BuildingClass.get("DefaultBuilding") == OBuilding["Type"]:
        for OBuilding2 in GlobalGameContext["BUILDINGS"].values():
            if OBuilding2.get("BuildingClass", "") == OBuilding.get("BuildingClass", "") and OBuilding2["Type"] != OBuilding["Type"]:
                Replacements.append(getHTMLLinkForText(OBuilding2))
        
    return f"Replaced by {", ".join(Replacements)}" if Replacements != [] else ""
    

def getCivForUniqueBuilding(OBuilding):
    for OCivilization in GlobalGameContext["CIVILIZATIONS"].values():
        UniqueBuildings = getNestedTag(OCivilization, "Buildings", "Building")
        for UniqueBuilding in UniqueBuildings:
            if UniqueBuilding["BuildingType"] == OBuilding["Type"]:
                return OCivilization
    return None

def getCivForUniqueUnit(OUnit):
    for OCivilization in GlobalGameContext["CIVILIZATIONS"].values():
        UniqueUnits = getNestedTag(OCivilization, "Units", "Unit")
        for UniqueUnit in UniqueUnits:
            if UniqueUnit["UnitType"] == OUnit["Type"]:
                return OCivilization
    return None

def getRequiredToBuild(OBuilding):
    # returns all Buildings, that need OBuilding.
    Classes= set()
    for OBuildingCandidate in GlobalGameContext["BUILDINGS"].values():
        PrereqBuildingClasses = getNestedTag(OBuildingCandidate, "BuildingClassNeededs", "BuildingClassNeeded")
        for PrereqBuildingClass in PrereqBuildingClasses:
            BuildingClassType = PrereqBuildingClass.get("BuildingClassType", "")
            if BuildingClassType == OBuilding["BuildingClass"] and OBuildingCandidate != OBuilding:
                link = getHTMLLinkForText(OBuildingCandidate)
                Classes.add(link)
        
    return f"Required to build {', '.join(Classes)}" if Classes != set() else ""

def getBuildingClassesNeeded(OBuilding):
    Classes = []
    PrereqBuildingClasses = getNestedTag(OBuilding, "BuildingClassNeededs", "BuildingClassNeeded")
    for PrereqBuildingClass in PrereqBuildingClasses:
        BuildingClass = GC["BUILDING_CLASSES"].get(PrereqBuildingClass.get("BuildingClassType", ""), None)
        if BuildingClass is not None:
            DefaultBuilding = GC["BUILDINGS"].get(BuildingClass.get("DefaultBuilding"), None)
            link = getHTMLLinkForText(DefaultBuilding)
            Classes.append(f"Requires {link} in city")
    return Classes

def getPrereqBuildingClasses(OBuilding):
    Classes = []
    PrereqBuildingClasses = getNestedTag(OBuilding, "PrereqBuildingClasses", "PrereqBuildingClass")
    for PrereqBuildingClass in PrereqBuildingClasses:
        BuildingClass = GC["BUILDING_CLASSES"].get(PrereqBuildingClass.get("BuildingClassType", ""), None)
        iNumBuildingNeeded = int(PrereqBuildingClass.get("iNumBuildingNeeded", 0))
        if BuildingClass is not None:
            DefaultBuilding = GC["BUILDINGS"].get(BuildingClass.get("DefaultBuilding"), None)
            link = getHTMLLinkForText(DefaultBuilding)
            Classes.append(f"Requires {link} ({iNumBuildingNeeded * TEMPLES_NEEDED_MULTIPLIKATOR} in total)")
    return Classes
    
    
    
    
def getPrereqBuildingClassPercents(OBuilding):
    Classes = []
    PrereqBuildingClassPercents = getNestedTag(OBuilding, "PrereqBuildingClassPercents", "PrereqBuildingClassPercent")
    
    for PrereqBuildingClassPercent in PrereqBuildingClassPercents:
        BuildingClass = GC["BUILDING_CLASSES"].get(PrereqBuildingClassPercent.get("BuildingClassType", ""), None)
        iPercent = PrereqBuildingClassPercent.get("iBuildingNeededPercent", "")
        if BuildingClass is not None and iPercent != "":
            DefaultBuilding = GC["BUILDINGS"].get(BuildingClass.get("DefaultBuilding"), None)
            link = getHTMLLinkForText(DefaultBuilding)
            Classes.append(f"Requires {link} in {iPercent}% of cities")
    return Classes


def getCultureLevelBoni(OBuilding):
    Boni = []
    # Commerce eg Gold, Research, Culture, Espionage Modifiers
    for CommerceInfo in getCultureCommerceInfos(OBuilding):
        iCommerceModifier = CommerceInfo[0]
        Symbol = getHTMLForFontSymbol(CommerceInfo[1])
        if iCommerceModifier > 0:
            Boni.append(f"+{iCommerceModifier}% {Symbol}")
    
    # Great People Rate Modifier
    iGreatPeopleRateModifier = int(OBuilding.get("iCultureGreatPeopleRateModifier", 0))
    Symbol = getHTMLForFontSymbol("GREAT_PEOPLE_CHAR")
    if iGreatPeopleRateModifier > 0:
        Boni.append(f"+{iGreatPeopleRateModifier}% {Symbol}")

    # Trade Route Modifier
    iTradeRouteModifier = int(OBuilding.get("iCultureTradeRouteModifier", 0))
    Symbol = getHTMLForFontSymbol("TRADE_CHAR")
    if iTradeRouteModifier > 0:
        Boni.append(f"+{iTradeRouteModifier}% {Symbol}")
    
    # Happiness Modifier
    iHappiness = int(OBuilding.get("iCultureHappiness", 0))
    Symbol = getHTMLForFontSymbol("HAPPY_CHAR")
    if iHappiness > 0:
        Boni.append(f"+{iHappiness} {Symbol}")
    return f"{', '.join(Boni)} per Culture Level" if Boni != [] else ""

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
    
    if BuildingClass.get("DefaultBuilding") != OBuilding["Type"] and OBuilding.get("bPagan", 0) != 1:
        return 2 # unique building, but exclude pagan temple replacements.
    
    if OBuilding.get("ReligionType", None) is not None or OBuilding.get("HolyCity", None) is not None:
        return 1 # religious building
    return 0 # normal building


def getNestedTag(OGameObject, key_outer, key_inner):
    # always returns a list, even if there is only one entry or no entry
    outer = OGameObject.get(key_outer, {})
    
    res = outer.get(key_inner, []) if isinstance(outer, dict) else []
    if isinstance(res, dict):
        return [res]
    elif isinstance(res, str):
        return[res]
    elif isinstance(res, list):
        return res
    return None


# Abstract function to get a string of HTMlButtonLinks
def getPrereqHTMLbuttons(OGameObject, key_outer, key_inner,Category):
    # key_outer: the key of the prereq in the game object, e.g. "PrereqBonuses"
    # key_inner: the key of the prereq in the prereq object, e.g. "Bonus"
    # The Category to get the actual Objects from, e.g. "BONI"
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
    
    
    
## Civics

def getBuildingProductionModifiers(OCivic):
    Modifiers = [] 
    BuildingProductionModifiers = getNestedTag(OCivic, "BuildingProductionModifiers", "BuildingProductionModifier")
    for BuildingProductionModifier in BuildingProductionModifiers:
        BuildingClass = BuildingProductionModifier.get("BuildingType", "")
         # BuildingClass = GC["BUILDING_CLASSES"].get(BuildingProductionModifier.get("BuildingType", ""), None)
        iProductionModifier = BuildingProductionModifier.get("iProductionModifier", "")
        if BuildingClass is not None and iProductionModifier != "":
            Modifiers.append([iProductionModifier, BuildingClass])
        
    return Modifiers


def getBuildingHappinessChanges(OCivic):
    Changes = []
    BuildingHappinessChanges = getNestedTag(OCivic, "BuildingHappinessChanges", "BuildingHappinessChange")
    for BuildingHappinessChange in BuildingHappinessChanges:
        BuildingClass = BuildingHappinessChange.get("BuildingType", "")
        iHappinessChange = int(BuildingHappinessChange.get("iHappinessChange", ""))
        if BuildingClass is not None and iHappinessChange != "":
            Changes.append([iHappinessChange, BuildingClass])
    return Changes