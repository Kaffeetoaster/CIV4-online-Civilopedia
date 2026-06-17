
import xml.etree.ElementTree as ET

import config
from python.helper.measure_duration import measure, start_new_log

from PIL import Image
from pathlib import Path
import json
import os

def strip_namespace(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag

def xml_to_dict(element):
    result = {}
    children = list(element)

    if children:
        child_dict = {}
        for child in children:
            tag = strip_namespace(child.tag)
            child_result = xml_to_dict(child)

            if tag not in child_dict:
                child_dict[tag] = child_result
            else:
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_result)

        return child_dict
    else:
        return element.text.strip() if element.text else ""


def parse_xml_file(file_path):
    # takes an xml file and returns a parsed representation depending on the root tag
    # trying to fix some encoding problems:
    text = Path(file_path).read_text(encoding="latin-1")
    root = ET.fromstring(text)
    # tree = ET.parse(file_path)
    # root = tree.getroot()
    root_tag = strip_namespace(root.tag)
    
    # Case 1: Civ4GameText -> dict keyed by <Tag>
    if root_tag == "Civ4GameText":
        result = {}
        for text_entry in root:
            entry_dict = xml_to_dict(text_entry)
            key = entry_dict.get("Tag")
            if key:
                result[key] = entry_dict
        return result

    # Case 2: two levels of nesting, dict keyed by <Type> of the second level
    result = {}
    for sub_root in root:
        for entry in sub_root:
            entry_dict = xml_to_dict(entry)
            key = entry_dict.get("Type")
            if key:
                result[key] = entry_dict
    return result




## build file index for loading with unknown capitalization
def build_case_index():
    index = {}
    paths = [
        config.INPUT_PATH / "Assets", # Mod
        config.INPUT_PATH.parent.parent / "Assets", # BTS
        config.INPUT_PATH.parent.parent.parent / "Warlords/Assets", # Warlords
        config.INPUT_PATH.parent.parent.parent / "Assets" , # basegame
        config.INPUT_PATH.parent.parent.parent.parent / "Art Assets", # basegame archives
    ]
    for root in paths:
        for path in root.rglob("*"):
            if path.is_file():
                index[str(path).lower()] = path
        
    return index

print("Built file index for case-insensitive loading of files.")
file_index = measure(build_case_index)
print(f"file index built with {len(file_index)} entries.")


def stringify_dict(dict):
    return {str(key): str(value) for key, value in dict.items()}

with open("data.json", "w") as f:
    json.dump(stringify_dict(file_index), f, indent=2)
    

def get_external_path(path):
    return file_index.get(str(path).lower(), "")

### Resolving XML tags ###


def load_from_path(input_path_part):
    paths = [
        config.INPUT_PATH / "Assets", # Mod
        config.INPUT_PATH.parent.parent / "Assets", # BTS
        config.INPUT_PATH.parent.parent.parent / "Warlords/Assets", # Warlords
        config.INPUT_PATH.parent.parent.parent / "Assets" , # basegame
        config.INPUT_PATH.parent.parent.parent.parent / "Art Assets", # basegame archives
    ]
    for path in paths:
        path = path / input_path_part
        path = get_external_path(path)
        if path != "":
            try:
                img = Image.open(path)
                break
            except:
                print(f"could not open image at path {path} with {input_path_part}")
                
    else:
        return None
    img.load()
    return img


def load_from_atlas(atlas_info):
    try:
        input_path_part = atlas_info[0]
    except:
        print(f"invalid atlas info {atlas_info}. Returning None.")
        return None
    img = load_from_path(input_path_part)
    return img.crop(((int(atlas_info[1])-1)*64, (int(atlas_info[2])-1)*64, int(atlas_info[1])*64, int(atlas_info[2])*64))


def convert_button_image(button_info, file_name):
    # fix file path, save it on config.OUTPUT_PATH and return the new path
    if button_info == "" or button_info is None:
        return None
    if type(button_info) is list:
            img = load_from_atlas(button_info)
            
    else:
        img = load_from_path(button_info)
                
    output_path = config.OUTPUT_PATH / f"Assets/Art/Interface/Buttons/{file_name}.png"
    os.makedirs(output_path.parent, exist_ok=True)
    img.save(output_path)
    return output_path

def resolve_button_path(ObjectValues, new_file_name):
    if "Button" not in ObjectValues:
        return ""
    path = ObjectValues.get("Button", "").split(',')
        
    if len(path)==5: # atlas info with leading comma   
        button_info = path[2:]
    elif len(path)==4: # atlas info
        button_info = path[1:]    
    
    elif len(path)==2: # weird path 
        button_info = path[1]
    else: # normal path
        button_info = path[0]
        
    if button_info == "" or button_info is None:
        return ""
    try:    
        new_path = convert_button_image(button_info, new_file_name)
    except Exception as e:
        return ""
    ObjectValues["Button"] = new_path
    return new_path