
# This file is responsible for provindg helper functions to build the text entries in the Pedia/* files.
# This includes html generation for links and images, some text formatting and
# also functions that extract infos from the game context.

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
            OBonus = GC["BONI"].get(Bonus, None)
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
        info = ""
        Civ = getCivForUniqueBuilding(OBuilding)
        if Civ is not None:
            info += f"Unique building for {getHTMLLinkForText(Civ)}"
        DefaultBuilding = GC["BUILDINGS"].get(BuildingClass.get("DefaultBuilding"), None)
        if DefaultBuilding is not None:
            info += f", replaces {getHTMLLinkForText(DefaultBuilding)}"
        Effects.append(info)
    
    # Replaced by
    replace = getReplacementBuildings(OBuilding)
    if replace != "":
        Effects.append(replace)
    
    
    # Culture Level Boni
    Boni = getCultureLevelBoni(OBuilding)
    if Boni != "":
        Effects.append(Boni)
    
    # Bonus Health Changes
    for Change in getBonusHealthChanges(OBuilding):
        Effects.append(Change)
    # Bonus Happiness Changes
    for Change in getBonusHappinessChanges(OBuilding):
        Effects.append(Change)
    # Bonus Yield Changes
    for Change in getBonusYieldChanges(OBuilding):
        Effects.append(Change)
    
    # Bonus Yield Modifiers
    for YieldModifier in getBonusYieldModifiers(OBuilding):
        Effects.append(YieldModifier)
        
    # Commerce Modifiers
    for CommerceModifier in getCommerceModifiers(OBuilding):
        iCommerceModifier = CommerceModifier[0]
        Symbol = getHTMLForFontSymbol(CommerceModifier[1])
        if iCommerceModifier > 0:
            Effects.append(f"+{iCommerceModifier}% {Symbol}")
    
    # Yield Modifiers        
    for YieldModifier in getYieldModifiers(OBuilding):
        iYieldModifier = YieldModifier[0]
        Symbol = getHTMLForFontSymbol(YieldModifier[1])
        if iYieldModifier > 0:
            Effects.append(f"+{iYieldModifier}% {Symbol}")
              
    # Happiness per Commerce Rate, eg Arena        
    CommercePerHappiness = getCommerceHappinessModifiers(OBuilding)        
    if CommercePerHappiness != "":
        Effects.append(CommercePerHappiness)

    # Happiness from State Religion
    iStateReligionHappiness = int(OBuilding.get("iStateReligionHappiness", 0))
    if iStateReligionHappiness > 0:
        SymbolHappiness = getHTMLForFontSymbol("HAPPY_CHAR")
        ReligionType = OBuilding.get("ReligionType", "")
        if ReligionType != "":
            SymbolReligion = getHTMLForFontSymbol(f"{ReligionType}_CHAR") 
        Effects.append(f"+{iStateReligionHappiness} {SymbolHappiness}, if {SymbolReligion} is State {getHTMLForFontSymbol('RELIGION_CHAR')} ")
    
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
     
    #### Power
    
    # Power (dirty)
    bDirtyPower = True if int(OBuilding.get("bDirtyPower", 0))==1 else False
    Bonus = GC["BONI"].get(OBuilding.get("PowerBonus", ""), None)
    if bDirtyPower and Bonus is not None:
        SymbolPower = getHTMLForFontSymbol("POWER_CHAR")
        SymbolUnhealthy = getHTMLForFontSymbol("UNHEALTHY_CHAR")
        Effects.append(f"Provides Power ({SymbolPower}) with {getHTMLLinkForText(Bonus)} (+2{SymbolUnhealthy})")
    
    # Power (clean)
    bPower = True if int(OBuilding.get("bPower", 0))==1 else False
    if bPower:
        SymbolPower = getHTMLForFontSymbol("CLEAN_POWER_CHAR")
        Effects.append(f"Provides Clean Power ({SymbolPower})")
    
    # Power Yield Modifier
    for YieldModifier in getPowerYieldModifiers(OBuilding):
        iYieldModifier = YieldModifier[0]
        Symbol = getHTMLForFontSymbol(YieldModifier[1])
        SymbolPower = getHTMLForFontSymbol("POWER_CHAR")
        if iYieldModifier > 0:
            Effects.append(f"+{iYieldModifier}% {Symbol} with Power ({SymbolPower})")    

    # Power Commerce Modifier
    for CommerceModifier in getPowerCommerceModifiers(OBuilding):
        iCommerceModifier = CommerceModifier[0]
        Symbol = getHTMLForFontSymbol(CommerceModifier[1])
        SymbolPower = getHTMLForFontSymbol("POWER_CHAR")
        if iCommerceModifier > 0:
            Effects.append(f"+{iCommerceModifier}% {Symbol} with Power ({SymbolPower})")
    
    
    # Help
    Help = get_text(OBuilding.get("Help", ""))
    if Help != "":
        Effects.append(Help)
    
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
    
    # Maintenance Modifier
    iMaintenanceModifier = int(OBuilding.get("iMaintenanceModifier", 0))
    if iMaintenanceModifier < 0:
        Effects.append(f"-{abs(iMaintenanceModifier)}% Maintenance Cost")

    # Great People Points
    GreatPeopleUnitClass = OBuilding.get("GreatPeopleUnitClass", "")
    iGreatPeopleRateChange = int(OBuilding.get("iGreatPeopleRateChange", 0))
    if GreatPeopleUnitClass != "" and iGreatPeopleRateChange !=0:
        Symbol = getHTMLForFontSymbol("GREAT_PEOPLE_CHAR")
        UnitTag = GC["UNIT_CLASSES"].get(GreatPeopleUnitClass,{}).get("DefaultUnit", "")
        link = getHTMLLinkForText(GC["UNITS"].get(UnitTag, None))
        Effects.append(f"+{iGreatPeopleRateChange} {Symbol} for {link}")
        
    iGreatPeopleRateModifier = int(OBuilding.get("iGreatPeopleRateModifier", 0))
    if iGreatPeopleRateModifier > 0:
        Symbol = getHTMLForFontSymbol("GREAT_PEOPLE_CHAR")
        Effects.append(f"+{iGreatPeopleRateModifier}% {Symbol} Birth Rate")
    
    # Specialits
    for Change in getSpecialistCount(OBuilding):
        Effects.append(Change)
    for Change in getFreeSpecialistCounts(OBuilding):
        Effects.append(Change)
    
    
    # Free Promotions
    FreePromotion = GC["PROMOTIONS"].get(OBuilding.get("FreePromotion", ""), None)
    if FreePromotion is not None:
        Effects.append(f"Free {getHTMLLinkForText(FreePromotion)} Promotion for Units built in this City")

    # Free XP
    for XP in getDomainFreeExperiences(OBuilding):
        Effects.append(XP)
    for XP in getUnitCombatFreeExperiences(OBuilding):
        Effects.append(XP)
    
    # Healing
    iHealRateChange = int(OBuilding.get("iHealRateChange", 0))
    if iHealRateChange > 0:
        Effects.append(f"Heals Units extra {iHealRateChange}% Damage per Turn")
    
    # Defense
    iDefense = int(OBuilding.get("iDefense", 0))
    if iDefense > 0:
        Effects.append(f"+{iDefense}% {getHTMLForFontSymbol('DEFENSE_CHAR')} (Execpt vs Gunpoweder-based Units)")
    # Bombard Defense
    iBombardDefense = int(OBuilding.get("iBombardDefense", 0))
    if iBombardDefense > 0:
        Effects.append(f"-{iBombardDefense}% Damage to {getHTMLForFontSymbol('DEFENSE_CHAR')} from Bombardment (Defense vs Gunpowder-based Units)")
    
    
    # Espionage Defense
    iEspionageDefense = int(OBuilding.get("iEspionageDefense", 0))
    if iEspionageDefense > 0:
        Effects.append(f"+{iEspionageDefense}% Defense against Espionage")
    
    # Corporation unhealth defense
    iCorporationUnhealthModifier = int(OBuilding.get("iCorporationUnhealthModifier", 0))
    if iCorporationUnhealthModifier < 0:
        Symbol = getHTMLForFontSymbol("UNHEALTHY_CHAR")
        Effects.append(f"{iCorporationUnhealthModifier}% {Symbol} from Corporations")
        
    # free at era
    FreeStartEra = GC["ERAS"].get(OBuilding.get("FreeStartEra", None), None)
    if FreeStartEra is not None:
        Effects.append(f"Available for free from {getHTMLLinkForText(FreeStartEra)} era onwards")
    
    # keep Food after Growth
    iFoodKept = int(OBuilding.get("iFoodKept", 0))
    if iFoodKept > 0:
        Symbol = getHTMLForFontSymbol("YIELD_FOOD_CHAR")
        Effects.append(f"Stores {iFoodKept}% of {Symbol} after city growth")
    
    # required to build.....
    Buildings = getRequiredToBuild(OBuilding)
    if Buildings != "":
        Effects.append(Buildings)
    
    #### Requirements
    # prereq Religion is placed in requires
    # prereq Tech is placed in requires
    # requeries Paganism
    bPagan = True if int(OBuilding.get("bPagan", 0))==1 else False
    if bPagan:
        Effects.append("Requires Paganism")
    
    # requieres Access to Coast
    bWater = True if int(OBuilding.get("bWater", 0))==1 else False
    if bWater:
        Effects.append("Requires access to Coast")
    # requieres Access to River
    bRiver = True if int(OBuilding.get("bRiver", 0))==1 else False
    if bRiver:        
        Effects.append("Requires access to River")
    
    # requiers UnitLvl
    iLevelPrereq = int(OBuilding.get("iLevelPrereq", 0))
    if iLevelPrereq > 0:
        Effects.append(f"Requires a Unit of at least Level {iLevelPrereq}")
    
    # requeries % of base building.
    #PrereqBuildingClassPercents eg. National_theatre
    for Needed in getPrereqBuildingClassPercents(OBuilding):
        Effects.append(Needed)
    
    # requieres Building(s) in City
    for Needed in getBuildingClassesNeeded(OBuilding):
        Effects.append(Needed)
    
    for Needed in getPrereqBuildingClasses(OBuilding):
        Effects.append(Needed)
    
    # happiness from civic
    for Change in getCivicHappinessChanges(OBuilding):
        Effects.append(Change)
    
    # production speed with civic
    for Modifier in getCivicProductionModifiers(OBuilding):
        Effects.append(Modifier)
    
    
    # production speed with bonus
    for Modifier in getBonusProductionModifiers(OBuilding):
        Effects.append(Modifier)
        
    # extra production speed for domain
    for Modifier in getDomainProductionModifiers(OBuilding):
        Effects.append(Modifier)
        
    # obsolets
    ObsoleteTech = GC["TECHS"].get(OBuilding.get("ObsoleteTech", None), None)
    if ObsoleteTech is not None:
        Effects.append(f"Obsolets with {getHTMLLinkForText(ObsoleteTech)}")
    
    #### Wonder effects
    
    # free Building
    FreeBuildingClass = GC["BUILDING_CLASSES"].get(OBuilding.get("FreeBuilding", ""), None)
    FreeBuilding = GC["BUILDINGS"].get(FreeBuildingClass.get("DefaultBuilding", ""), None) if FreeBuildingClass is not None else None
    if FreeBuilding is not None:
        Effects.append(f"Free {getHTMLLinkForText(FreeBuilding)} in every city")

    # Hurry Modifer
    iGlobalHurryModifier = int(OBuilding.get("iGlobalHurryModifier", 0))
    if iGlobalHurryModifier < 0:
        Effects.append(f"-{abs(iGlobalHurryModifier)}% Hurry Production Cost")
    
    # power on continent
    bAreaCleanPower = True if int(OBuilding.get("bAreaCleanPower", 0))==1 else False
    if bAreaCleanPower:
        SymbolPower = getHTMLForFontSymbol("CLEAN_POWER_CHAR")
        Effects.append(f"Provides Clean Power ({SymbolPower}) to all cities on the same continent")
    
    # free specialists
    iFreeSpecialist = int(OBuilding.get("iFreeSpecialist", 0))
    if iFreeSpecialist > 0:
        Effects.append(f"+{iFreeSpecialist} Free Specialist(s)")
    iGlobalFreeSpecialist = int(OBuilding.get("iGlobalFreeSpecialist", 0))
    if iGlobalFreeSpecialist > 0:
        Effects.append(f"+{iGlobalFreeSpecialist} Free Specialist(s) in all cities")
    
        
    # extra Commerce per Specialist 
    for CommerceModifier in getSpecialistExtraCommerces(OBuilding):
        iCommerceModifier = CommerceModifier[0]
        Symbol = getHTMLForFontSymbol(CommerceModifier[1])
        if iCommerceModifier > 0:
            Effects.append(f"+{iCommerceModifier} {Symbol} per Specialist in all cities")

    # extra Commerce for State religion buildings
    for CommerceModifier in getStateReligionCommerces(OBuilding): 
        iCommerceModifier = CommerceModifier[0]
        Symbol = getHTMLForFontSymbol(CommerceModifier[1])
        if iCommerceModifier > 0:
            Effects.append(f"+{iCommerceModifier} {Symbol} from all State {getHTMLForFontSymbol('RELIGION_CHAR')} Buildings ")
    
    
    # Space
    iGlobalSpaceProductionModifier = int(OBuilding.get("iGlobalSpaceProductionModifier", 0))
    if iGlobalSpaceProductionModifier > 0:
        Symbol = getHTMLForFontSymbol("YIELD_PRODUCTION_CHAR")
        Effects.append(f"+{iGlobalSpaceProductionModifier}% Spaceship Production in all cities")
        
        
    return {
        "title": "Effects",
        "content": addBulletpoints(Effects)
    }
    
    
    

def placeHistory(OBuilding):
    History = []
    # Stratgey
    Strategy = get_text(OBuilding.get("Strategy", ""))
    History.append(Strategy)
    
    History.append("") # line break
    
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