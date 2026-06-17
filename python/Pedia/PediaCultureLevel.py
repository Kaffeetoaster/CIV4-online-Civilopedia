
# This file is responsible for provindg helper functions to build the text entries in the Pedia/* files.
# This includes html generation for links and images, some text formatting and
# also functions that extract infos from the game context.



from python.gameContext.game import GlobalGameContext
from python.helper.text.text_helper import *

def placeInfo(CultureLevel):
    
    title = get_text(CultureLevel["Description"])
    content = []
    iCulture =  CultureLevel["SpeedThresholds"]["SpeedThreshold"][2]["iThreshold"]
    Symbol = getHTMLForFontSymbol("COMMERCE_CULTURE_CHAR")
    content.append(f"Requires {iCulture} {Symbol} to reach this level.")    
    return {"title": title, "content": content}

    

def placeEffects(CultureLevel):
    # place effects for the culture level
    Effects = []
    
    iDefense = int(CultureLevel["iCityDefenseModifier"])
    Symbol = getHTMLForFontSymbol("DEFENSE_CHAR")
    if iDefense > 0:
        Effects.append(f"+{iDefense}% {Symbol}")
    
    iUnrest = int(CultureLevel["index"])
    Symbol = getHTMLForFontSymbol("OCCUPATION_CHAR")
    if iUnrest > 0:
        Effects.append(f"+{iUnrest} turns of {Symbol} on conquest")
    
    iWonderLimit = int(CultureLevel["iWonderLimit"])
    if iWonderLimit > 0:
        Effects.append(format_text(get_text("TXT_KEY_PEDIA_WONDER_LIMIT"), iWonderLimit))
    
    iNationalWonderLimit = int(CultureLevel["iNationalWonderLimit"])
    if iNationalWonderLimit > 0:
        Effects.append(format_text(get_text("TXT_KEY_PEDIA_NATIONAL_WONDER_LIMIT"), iNationalWonderLimit))
    
    return {
        "title": "Effects",
        "content": addBulletpoints(Effects)
    }


def placeBuildings(CultureLevel):
    Buildings = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        building_name = getHTMLLinkForText(OBuilding)
        
        # Commerce eg Gold, Research, Culture, Espionage Modifiers
        for CommerceInfo in getCultureCommerceInfos(OBuilding):
            
            iCommerceModifier = CommerceInfo[0]
            Symbol = getHTMLForFontSymbol(CommerceInfo[1])
            if iCommerceModifier > 0:
                #print(f"CommerceInfo: {CommerceInfo} of type {type(CommerceInfo)}")
                value = iCommerceModifier * (CultureLevel["index"])
                Buildings.append(f"{building_name}: +{value}% {Symbol}")
        
        # Great People Rate Modifier
        iGreatPeopleRateModifier = int(OBuilding.get("iCultureGreatPeopleRateModifier", 0))
        
        iValue = iGreatPeopleRateModifier * (CultureLevel["index"])
        Symbol = getHTMLForFontSymbol("GREAT_PEOPLE_CHAR")
        if iGreatPeopleRateModifier > 0:
            #print(f"modifier: {iGreatPeopleRateModifier} of type {type(iGreatPeopleRateModifier)}")
            Buildings.append(f"{building_name}: +{iValue}% {Symbol}")

        # Trade Route Modifier
        iTradeRouteModifier = int(OBuilding.get("iCultureTradeRouteModifier", 0))
        Symbol = getHTMLForFontSymbol("TRADE_CHAR")
        if iTradeRouteModifier > 0:
            iValue = iTradeRouteModifier * (CultureLevel["index"])
            Buildings.append(f"{building_name}: +{iValue}% {Symbol}")
        
        # Happiness Modifier
        iHappiness = int(OBuilding.get("iCultureHappiness", 0))
        Symbol = getHTMLForFontSymbol("HAPPY_CHAR")
        value = iHappiness * (CultureLevel["index"])
        if iHappiness > 0:
            Buildings.append(f"{building_name}: +{value} {Symbol}")
        
        
    return {
        "title": "Buildings",
        "content": addBulletpoints(Buildings)
        }


def placeSpecialists(CultureLevel):
    # place specialists for the culture level
    return {}


def build_CultureLevel_Entry(CultureLevel):
    Entry = []
    
    # place info
    Entry.append(placeInfo(CultureLevel))
    # place effects
    Entry.append(placeEffects(CultureLevel))
    # place buildings
    Entry.append(placeBuildings(CultureLevel))

    return Entry


def build_CultureLevel_Page():
    PageContent = []
    for CultureLevel in GlobalGameContext["CULTURE_LEVELS"].values():
            PageContent.append(build_CultureLevel_Entry(CultureLevel))
    return {"title": "Culture Levels", "content": PageContent}

    # return [build_CultureLevel_Entry(CultureLevel) for CultureLevel in GlobalGameContext["CULTURE_LEVELS"].values()]
    
    