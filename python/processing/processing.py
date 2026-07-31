
from pathlib import Path
from unicodedata import category
from PIL import Image
import os 
import re

import config 

## Button processing functions


def buildButtonLookup():
    """
    Build a lookup table for button locations. Start with the basegame, then add Warlords and BTS and then the mod.
    
    Result should be a mapping of relative button path to exact file path.
    """
    paths = [
            config.INPUT_PATH.parent.parent.parent / "Assets" , # basegame
            config.INPUT_PATH.parent.parent.parent.parent / "Art Assets", # basegame archives i extracted them once into an Art Assets folder.
            config.INPUT_PATH.parent.parent.parent / "Warlords/Assets", # Warlords
            config.INPUT_PATH.parent.parent / "Assets", # BTS
            config.INPUT_PATH / "Assets", # Mod
        ]
    dict_buttonLookup = {}
    for path in paths:
        for file in path.rglob("*.dds"):
            relative_path = file.relative_to(path)
            dict_buttonLookup[str(relative_path).lower()] = str(file)
    
    return dict_buttonLookup


def loadButtonFromAtlas(atlas_info, buttonLookup):
    """
    Given an atlas info, load the button image from the atlas.
    """
    atlas_path = buttonLookup.get(atlas_info[0].lower(), "")
    if atlas_path == "":
        print(f"Atlas path not found for {atlas_info[0]}.")
        return None
    
    img = Image.open(atlas_path)
    return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))
    

def convertButtonImage(button, buttonLookup):
    """
    Given button info convert the button image to png and save it to the output path.
    
    Returns the new path to the button image.
    """
    
    source = button.get("source", "").split(",")
    
    if len(source)==5: # atlas info with leading comma   
        button_info = source[2:]
        file_path = f"Art/Interface/Atlas/{Path(source[2]).stem}_{source[3]}_{source[4]}.png"
    elif len(source)==4: # atlas info
        button_info = source[1:]
        file_path = f"Art/Interface/Atlas/{Path(source[1]).stem}_{source[2]}_{source[3]}.png"    
    elif len(source)==2: # weird path 
        button_info = source[1]
        file_path = Path(source[1]).with_suffix(".png")
    else: # normal path
        button_info = source[0]
        file_path = Path(source[0]).with_suffix(".png")
        
    if button_info == "" or button_info is None:
        return None
    
    if type(button_info) is list:
        # load button from atlas
        img = loadButtonFromAtlas(button_info, buttonLookup)
        if img is None:
            print(f"Could not load button from atlas {button_info}.")
            return None
    else:
        absolute_button_path = buttonLookup.get(button_info.lower(), "")
        if absolute_button_path == "":
            print(f"Button path not found for {button_info}.")
            return None
        img = Image.open(absolute_button_path)
    
    if button.get("link", "") != "":
        file_path = f"Art/Interface/{button['link'].replace('#', '/').replace(' ', '-')}.png"
    
    output_path = config.OUTPUT_PATH / "Assets" / file_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return file_path
    

## Button link processing functions

def buildHTMLLinkForButton(button):
    """
    Given a button, return HTML code to display the button. This includes a link to the entry.
    """
    categoryName,entryName = button["link"].split("#")
    link = f"../../Categories/{categoryName.replace(' ', '-')}/#{entryName.replace(' ', '-').lower()}"
    text = entryName.replace('-', ' ')
    return f'<a href="{link}" title="{text}"><img src="../../Assets/{button["source"]}" alt="{text}">  </a>'

def buildHTMLForButton(button):   
    """
    Given a button, return HTML code to display the button. This does not include a link to the entry.
    """
    text = Path(button["source"]).stem
    return f'<img src="../../Assets/{button["source"]}" alt="{text}"> '

## text link processing functions

def buildLinkLookup(CivilopediaData):
    """
    Build a lookup table for links. Mapping is from a Entry name like "The Americans" to the link.
    Walks over each Category in the raw Civilopedia data and mapps each entry name to the link "Category/#Entry-Name"
    """
    dict_linkLookup = {}
    for category in CivilopediaData["Categories"]:
        for entry in category["Entries"]:
            link = f"{category['Category'].replace(' ', '-')}/#{entry['title'].replace(' ', '-')}"
            dict_linkLookup[entry["title"]] = link
    return dict_linkLookup
    

def buildHTMLLinkForText(text, linkLookup):
    
    link = f"../../Categories/{linkLookup.get(text)}" 
    return f'<a class="text-link" href="{link}" title="{text}">{text}</a>'


## text formatting functions

def resolveTextFormatting(text, linkLookup):
    """
    Given a textstring, resolve the formatting and return the formatted text.
    Result should be a string with HTML formatting.
    This includes: 
    font tags, \n, color tags, and hexedecimal symbold IDs like \u01c6, <tab>, <b> etc.
    """
    
    
    # ignore font tags for now:
    
    
    text = re.sub(
        r"<font=4b>(.*?)</font>",
        lambda match: f"<strong>{match.group(1)}</strong>",
        text
    )
    text = text.replace("<font=2>", "").replace("<font=3>", "").replace("</font>", "")
    
    
    # replace new lines with <br> tags
    text = text.replace("\\n", "<br>")
    
    # replace <tab> with &nbsp;*4
    text = text.replace("<tab>", "&nbsp;"*4)
    
    # replace <b> and </b> with <strong> and </strong>
    text = text.replace("<b>", "<strong>").replace("</b>", "</strong>")
    
    # replace color tags with <span> tags
    def replace_color(match):
        r, g, b, a = map(int, match.groups())

        if not all(0 <= value <= 255 for value in (r, g, b, a)):
            return match.group(0)

        alpha = a / 255

        if a == 255:
            return f'<span style="color: rgb({r} {g} {b});">'

        return f'<span style="color: rgb({r} {g} {b} / {alpha:.3f});">'

    text = re.sub(
        r"<color=(\d+),(\d+),(\d+),(\d+)>",
        replace_color,
        text
    )
    text = text.replace("</color>", "</span>")
    
    # replace hexadecimal symbol IDs like \u01c6 with the corresponding HTML code for the symbol
    
    text = re.sub(
        r"\\u([0-9a-fA-F]{4})",
        lambda match: buildHTMLForSymbol(match.group(1)),
        text
    )
    SymbolIDs = re.findall(r"\\u([0-9a-fA-F]{4})", text)
    
    # replace links in the text like <link=literal>Artist</link>
    
    text = re.sub(
        r"<link=literal>(.*?)</link>",
        lambda match: buildHTMLLinkForText(match.group(1), linkLookup),
        text
    )
    text = re.sub(
            r"<link='literal'>(.*?)</link>",
            lambda match: buildHTMLLinkForText(match.group(1), linkLookup),
            text
        )
    
    return text



## Symbol proccessing functions

def extractGlyphsFromFontAtlas():
    """
    Load the font atlas and split it into individual symbols.
    Save them with the correct ids. Beginnend mit 0100,0101,0102 für die yields und dann 0113 für die commerce types und dann mit 25 elementen pro Zeile gerechnet. (Auch leere Zeilen zählen!).
    """
    # load the font atlas
    font_img = Image.open(config.INPUT_PATH / "Assets/res/Fonts/GameFont.tga")
    GAME_FONT_ROW_BLOCKS = [
    {"count": 4, "height": 17, "vertical_spacing": 1},
    {"count": 10, "height": 21, "width": 21, "vertical_spacing": 0, "horizontal_spacing": 1},
    ]
    
    offset_top = 71# offset for the frirst 4 rows, since the contain only letters.
    offset_left = 0 # offset for the bullet point, since its only 12px wide instead of 21px.
    # yields are extra, because in the first row are only 14 or so elements instead of 25.
    for num in range(0x0100, 0x0103):
        
        i = num-0x0100
        glyph_img = font_img.crop((i*21,offset_top,i*22+21,offset_top+21))
        output_path = config.OUTPUT_PATH / f"Assets/Symbols/{num:04x}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        glyph_img.save(output_path)
    
    # others glyhs starting with the commerce types
    for num in range(0x0113, 0x0113+25*9):
        i = num-0x0113
        row = i//25
        col = i%25
        
        glyph_img = font_img.crop((offset_left+col*22,offset_top+row*21 + 21,offset_left+col*22+21,offset_top+row*21+21 +21))
        
        if row == 7:
            if col == 4: # the bulltet point is a special case, since its not 21x21 px.
                glyph_img = font_img.crop((col*22,offset_top+row*21 + 21,col*22+12,offset_top+row*21+21 +21))
                offset_left = 12-21
            if col == 24:
                offset_left = 0
        
        # dont save empty glyphs!
        if glyph_img.getbbox() is not None:
            output_path = config.OUTPUT_PATH / f"Assets/Symbols/{num:04x}.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            glyph_img.save(output_path)         
        



def buildHTMLForSymbol(SymbolID):
    """
    Given a symbol ID, return HTML code to display the symbol.
    """
    source = f"{SymbolID}.png"
    if not (config.OUTPUT_PATH / f"Assets/Symbols/{source}").exists():
        return f"&#x{SymbolID};"
    
    return f'<img src="../../Assets/Symbols/{source}" alt="{SymbolID}" class="Symbol">'
    
    pass


## toc generation functions

def generateTOC(gamedata):
    """
    Given the (raw or processed)gamedata, generate a table of contents for use in mkdocs.yml.
    """
    
    pass