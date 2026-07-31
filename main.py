from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import json

from config import INPUT_PATH, OUTPUT_PATH
from python.measure_duration import measure, start_new_log
import python.CivilopediaData as CivilopediaData
from python.processing.processing import *


start_new_log()



TEMPLATE_DIR = Path(__file__).resolve().parent / "jinja_templates"



def renderCategory(PageInfos, result_file, template_name= "template_page.jinja"):
	environment = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
 
	template = environment.get_template(template_name)
	rendered_html = template.render(page = PageInfos)
	result_file.write_text(rendered_html, encoding="utf-8")


def renderCategories(Civilopedia):
	for category in Civilopedia.Categories:
		print(f"Rendering category {category.title}...")
		result_file = OUTPUT_PATH/ "Categories" / f"{category.title.replace(' ', '-')}.md"
		
		renderCategory(category, result_file)
		print(f"Finished rendering category {category.title}. Result saved to {result_file}")


def loadCivilopediaData():
    
    with open("data/CivilopediaData_raw.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def buildCivilopediaData():
    raw_CivilopediaData = loadCivilopediaData()
    # print("Civlopediadata:")
    # print(raw_CivilopediaData["Categories"][0].get("Entries", [])[:1])
    buttonLookup = buildButtonLookup()
    linkLookup = buildLinkLookup(raw_CivilopediaData)
    extractGlyphsFromFontAtlas()
    
    civilopedia = CivilopediaData.Civilopedia(title=raw_CivilopediaData["title"])
    
    for category_data in raw_CivilopediaData["Categories"]:
        if category_data.get("Entries", []) == []:
            continue
        category = CivilopediaData.Category(title=category_data["Category"])
        
        for entry_data in category_data["Entries"]:
            entry = CivilopediaData.Entry(title=entry_data["title"])
            
            
            for i, panel_data in enumerate(entry_data["PageContent"]):
                
                Panelcontent = ""
                
                # if there is another panel before the listbox, attach the infos to the panel.
                # if there is no panel before, like for the Culture Levels, attach the infos to the listbox panel.
                if panel_data.get("type", "") == "listbox":
                    panel_data["content"].pop(0) # remove the first element, since it should contain the title too.
                    texts = [content.get("text", "") for content in panel_data["content"] if content.get("text", "") not in ["", "<font=3></font>"]]
                    text = resolveTextFormatting(", ".join(texts), linkLookup)
                    if entry.PageContent != []:
                        entry.PageContent[0].PanelContent += text
                    else:
                        Panelcontent += text
                else:
                    for datapoint in panel_data["content"]:
                        
                        contentType = datapoint.get("type", "")
                        
                        if contentType == "text":
                            Panelcontent += resolveTextFormatting(datapoint.get("text", ""), linkLookup)
                        elif contentType == "button":
                            
                            datapoint["source"] = convertButtonImage(datapoint, buttonLookup)
                            if panel_data["title"] == "":
                                panel_data["title"] = buildHTMLForButton(datapoint)  # add button to title for the info panel
                                panel_data["title"] += " "
                            else:
                                Panelcontent += buildHTMLForButton(datapoint)
                            
                        elif contentType == "buttonlink":
                            datapoint["source"] = convertButtonImage(datapoint, buttonLookup)
                            Panelcontent += buildHTMLLinkForButton(datapoint)
                        elif contentType == "listboxstring":
                            Panelcontent += resolveTextFormatting(datapoint.get("text", ""), linkLookup)
                
                if Panelcontent != "" or panel_data["title"] != "":
                    panel = CivilopediaData.Panel(title=panel_data["title"], PanelContent=Panelcontent)
                    entry.PageContent.append(panel)
            entry.PageContent[0].title += entry_data["title"]  # set the title of the first panel to the title of the entry
            category.entries.append(entry)
        
        civilopedia.Categories.append(category)
    
    return civilopedia



if __name__ == "__main__":
	CivilopediaData_processed = measure(buildCivilopediaData)
    
	measure(renderCategories, CivilopediaData_processed)
