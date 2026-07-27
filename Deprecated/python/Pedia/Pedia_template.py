
# This file is responsible for provindg helper functions to build the text entries in the Pedia/* files.
# This includes html generation for links and images, some text formatting and
# also functions that extract infos from the game context.

from numpy import info

from python.gameContext.game import GlobalGameContext
from python.helper.text.text_helper import *
GC = GlobalGameContext

def placeInfo(OBuilding):
    
    title = get_text(OBuilding["Description"])
    info = ""
    button_html = getHTMLLinkForButton(OBuilding)
    title = f"{button_html} {title}"
    
    # Yield
    for YieldInfo in getYieldInfos(OBuilding):
        iYieldModifier = YieldInfo[0]
        Symbol = getHTMLForFontSymbol(YieldInfo[1])
        if iYieldModifier > 0:
            info += f"+{iYieldModifier} {Symbol} "
    
    # Commerce
    for CommerceInfo in getCommerceChanges(OBuilding):
        iCommerceModifier = CommerceInfo[0]
        Symbol = getHTMLForFontSymbol(CommerceInfo[1])
        if iCommerceModifier > 0:
            info += f"+{iCommerceModifier} {Symbol} "
    
    # Happiness
    iHappiness = int(OBuilding.get("iHappiness", 0))
    
    if iHappiness > 0:
        Symbol = getHTMLForFontSymbol("HAPPY_CHAR")
        info += f"+{iHappiness} {Symbol} "
    elif iHappiness < 0:
        Symbol = getHTMLForFontSymbol("UNHAPPY_CHAR")
        info += f"+{abs(iHappiness)} {Symbol} "
    
    # Health
    iHealth = int(OBuilding.get("iHealth", 0))
    if iHealth > 0:
        Symbol = getHTMLForFontSymbol("HEALTHY_CHAR")
        info += f"+{iHealth} {Symbol} "
    elif iHealth < 0:
        Symbol = getHTMLForFontSymbol("UNHEALTHY_CHAR")
        info += f"+{abs(iHealth)} {Symbol} "
    
    # Cost
    iCost = int(OBuilding.get("iCost", 0))
    Symbol = getHTMLForFontSymbol("YIELD_PRODUCTION_CHAR")
    costString = ""
    if iCost > 0:
        costString = f"Cost: {iCost} {Symbol} "
        
    return {"title": title, "content": [info, costString] if costString!= "" else [info]}


def placeRequires(OBuilding):
    content = ""
    
    # Techs, TechTypes is used, when more than one prerequisite tech is needed
    PrereqTechs = []
    PrereqTech = GC["TECHS"].get(OBuilding.get("PrereqTech", None), None)
    PrereqTechs.append(PrereqTech)
    TechTypes = GC["TECHS"].get(OBuilding.get("TechTypes", {}).get("PrereqTech", None), None)
    PrereqTechs.append(TechTypes)
    
    for OTech in PrereqTechs:
        if OTech is not None:
            button = getHTMLLinkForButton(OTech)
            content += button
    # Bonus
    PrereqBonus = OBuilding.get("PrereqBonuses", {})
    if isinstance(PrereqBonus, str):
        PrereqBonus = [PrereqBonus]
    else:
        PrereqBonus = PrereqBonus.get("Bonus", [])
        if isinstance(PrereqBonus, dict):
            PrereqBonus = [PrereqBonus]
    if isinstance(PrereqBonus, list):
        for i, Bonus in enumerate(PrereqBonus):
            if i > 0:
                content += " or "
            OBonus = GC["BONUSES"].get(Bonus, None)
            if OBonus is not None:
                button = getHTMLLinkForButton(OBonus)
                content += button
                
                      
    # Civics
    PrereqCivic = GC["CIVICS"].get(OBuilding.get("PrereqCivic", None), None)
    content += getHTMLLinkForButton(PrereqCivic)
    
    # Religions
    content += getReligionPrereqString(OBuilding)        

    # Corporations
    PrereqCorporation = GC["CORPORATIONS"].get(OBuilding.get("PrereqCorporation", None), None)
    content += getHTMLLinkForButton(PrereqCorporation)        
    
    return {"title": "Requires", "content": [content]}

def placeEffects(OBuilding):
    BuildingClass = GC["BUILDING_CLASSES"].get(OBuilding.get("BuildingClass", ""), {})
    Effects = []
    
    # Unique Building and replaces ...
    if BuildingClass.get("DefaultBuilding") != OBuilding["Type"]:
        Civ = getCivForUniqueBuilding(OBuilding)
        if Civ is not None:
            Effects.append(f"Unique building for {getHTMLLinkForText(Civ)}")
        DefaultBuilding = GC["BUILDINGS"].get(BuildingClass.get("DefaultBuilding"), None)
        if DefaultBuilding is not None:
            Effects.append(f"Replaces {getHTMLLinkForText(DefaultBuilding)}")
    
    # Bonus Health Changes
    for Change in getBonusHealthChanges(OBuilding):
        Effects.append(Change)
    # Bonus Happiness Changes
    for Change in getBonusHappinessChanges(OBuilding):
        Effects.append(Change)
    
    # Commerce Modifiers
    for CommerceModifier in getCommerceModifiers(OBuilding):
        iCommerceModifier = CommerceModifier[0]
        Symbol = getHTMLForFontSymbol(CommerceModifier[1])
        if iCommerceModifier > 0:
            Effects.append(f"+{iCommerceModifier}% {Symbol}")
    # Help
    Help = get_text(OBuilding.get("Help", ""))
    if Help != "":
        Effects.append(Help)
        
    # prereq Religion is placed in requires
    # prereq Tech is placed in requires
    
    # Trade Routes
    iTradeRoutes = int(OBuilding.get("iTradeRoutes", 0))
    if iTradeRoutes > 0:
        Effects.append(f"+{iTradeRoutes} Trade Route(s)")
    # Global Trade Routes
    iGlobalTradeRoutes = int(OBuilding.get("iGlobalTradeRoutes", 0))
    if iGlobalTradeRoutes > 0:
        Effects.append(f"+{iGlobalTradeRoutes} Trade Route(s) in all cities")
        
    # Trade Route Modifier
    iTradeRouteModifier = int(OBuilding.get("iTradeRouteModifier", 0))
    Symbol = getHTMLForFontSymbol("TRADE_CHAR")
    if iTradeRouteModifier > 0:
        Effects.append(f"+{iTradeRouteModifier}% {Symbol}")
    # Foreign Trade Route Modifier
    iForeignTradeRouteModifier = int(OBuilding.get("iForeignTradeRouteModifier", 0))
    if iForeignTradeRouteModifier > 0:
        Effects.append(f"+{iForeignTradeRouteModifier}% {Symbol} to foreign Trade Routes")
    
    # Plot Yield changes
    for YieldInfo in getSeaPlotYieldChanges(OBuilding):
        iYieldModifier = YieldInfo[0]
        Symbol = getHTMLForFontSymbol(YieldInfo[1])
        if iYieldModifier > 0:
            Effects.append(f"+{iYieldModifier} {Symbol} on Sea Plots ")
    for YieldInfo in getFlatRiverPlotYieldChanges(OBuilding):
        iYieldModifier = YieldInfo[0]
        Symbol = getHTMLForFontSymbol(YieldInfo[1])
        if iYieldModifier > 0:
            Effects.append(f"+{iYieldModifier} {Symbol} on Flat River Plots ")
    
    # Great People Points
    GreatPeopleUnitClass = OBuilding.get("GreatPeopleUnitClass", "")
    iGreatPeopleRateChange = int(OBuilding.get("iGreatPeopleRateChange", 0))
    if GreatPeopleUnitClass != "" and iGreatPeopleRateChange !=0:
        Symbol = getHTMLForFontSymbol("GREAT_PEOPLE_CHAR")
        UnitTag = GC["UNIT_CLASSES"].get(GreatPeopleUnitClass,{}).get("DefaultUnit", "")
        link = getHTMLLinkForText(GC["UNITS"].get(UnitTag, None))
        Effects.append(f"+{iGreatPeopleRateChange}{Symbol} for {link}")
    
    # Specialits
    for Change in getSpecialistCount(OBuilding):
        Effects.append(Change)
    
    # Free Promotions
    
    # Free XP
        
    # free at era
    
    # requiers Access to Coast
    bWater = True if int(OBuilding.get("bWater", 0))==1 else False
    if bWater:
        Effects.append("Requires access to Coast")
    
    # requieres civic?
    
    # requeries % of base building.
    #PrereqBuildingClassPercents eg. National_theatre
    
    # requeirs Building in City
    
    # double production speed with civic
    
    # double production speed with bonus
    
    # obsolets
    
    # replaced by special buildings
    
    # requeired to build ...
    
    return {
        "title": "Effects",
        "content": addBulletpoints(Effects)
    }
    
    
    

def placeHistory(OBuilding):
    History = []
    # Stratgey
    Strategy = get_text(OBuilding.get("Strategy", ""))
    History.append(Strategy)
    # Civilopedia
    Civilopedia = get_text(OBuilding.get("Civilopedia", ""))
    History.append(Civilopedia)
    return {
        "title": "History",
        "content": History}
    
def build_Building_Entry(OBuilding):
    Entry = []
    
    # place info
    Entry.append(placeInfo(OBuilding))
    # place requires
    Entry.append(placeRequires(OBuilding))
    # # place effects
    Entry.append(placeEffects(OBuilding))
    # place History
    Entry.append(placeHistory(OBuilding))

    return Entry


def build_Building_Page():
    Buildings = []
    PageContent = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        if getBuildingCategory(OBuilding) == 0: # normal building
            Buildings.append(OBuilding)
    
    Buildings.sort(key=lambda b: get_text(b["Description"]))  
    for OBuilding in Buildings:    
        PageContent.append(build_Building_Entry(OBuilding))
    return {"title": "Buildings", "content": PageContent}

    # return [build_CultureLevel_Entry(CultureLevel) for CultureLevel in GlobalGameContext["CULTURE_LEVELS"].values()]

def build_ReligiousBuilding_Page():
    PageContent = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        if getBuildingCategory(OBuilding) == 1: # religious building
            PageContent.append(build_Building_Entry(OBuilding))
    return {"title": "Religious Buildings", "content": PageContent}

def build_UniqueBuilding_Page():
    Buildings = []
    PageContent = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        if getBuildingCategory(OBuilding) == 2: # unique building
            Buildings.append(OBuilding)            
    Buildings.sort(key=lambda b: get_text(b["Description"]))       
    for OBuilding in Buildings:
        PageContent.append(build_Building_Entry(OBuilding))
    return {"title": "Unique Buildings", "content": PageContent}

def build_GreatPeopleBuilding_Page():
    PageContent = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        if getBuildingCategory(OBuilding) == 3: # great people building
            PageContent.append(build_Building_Entry(OBuilding))
    return {"title": "Great People Buildings", "content": PageContent}

def build_NationalWonder_Page():
    PageContent = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        if getBuildingCategory(OBuilding) == 4: # national wonder
            PageContent.append(build_Building_Entry(OBuilding))
    return {"title": "National Wonders", "content": PageContent}

def build_GreatWonder_Page():
    Buildings = []
    PageContent = []
    for OBuilding in GlobalGameContext["BUILDINGS"].values():
        if getBuildingCategory(OBuilding) == 5: # great wonder
            Buildings.append(OBuilding)
    Buildings.sort(key=lambda b: get_text(b["Description"]))
    for OBuilding in Buildings:
        PageContent.append(build_Building_Entry(OBuilding))
    return {"title": "Great Wonders", "content": PageContent}