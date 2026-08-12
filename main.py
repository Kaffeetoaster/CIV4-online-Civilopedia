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

def renderUpgradeTrees(Civilopedia):
	for UpgradeTree in Civilopedia.UpgradeTrees:
		print(f"Rendering UpgradeTree {UpgradeTree.title}...")
		result_file = OUTPUT_PATH/ "Categories" / f"{UpgradeTree.title.replace(' ', '-')}.md"
		
		renderCategory(UpgradeTree, result_file, template_name= "template_UpgradeTree.jinja")
		print(f"Finished rendering UpgradeTree {UpgradeTree.title}. Result saved to {result_file}")

def renderCategories(Civilopedia):
	for category in Civilopedia.Categories:
		print(f"Rendering category {category.title}...")
		result_file = OUTPUT_PATH/ "Categories" / f"{category.title.replace(' ', '-')}.md"
		
		renderCategory(category, result_file)
		print(f"Finished rendering category {category.title}. Result saved to {result_file}")



def renderTechChooser(TechTree, result_file = OUTPUT_PATH / "Categories" / "Tech-Tree.md", template_name= "template_TechChooser.jinja"):
	print(f"Rendering TechChooser {TechTree.title}...")
	environment = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
 
	template = environment.get_template(template_name)
	rendered_html = template.render(TechTree = TechTree)
	result_file.write_text(rendered_html, encoding="utf-8")
	print(f"Finished rendering TechChooser {TechTree.title}. Result saved to {result_file}")
	
	
def loadTechTreeData():
	with open("data/TechChooserData_raw.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	return data    

def loadCivilopediaData():
	with open("data/CivilopediaData_raw.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	return data

def loadPreviewData():
	with open("data/PreviewData_raw.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	return data


def buildTechTreeData(raw_TechTreeData=None, buttonLookup=None, linkLookup=None, previewLookup=None):

	TechTree = CivilopediaData.TechChooser(title=raw_TechTreeData["title"])
	for tech_data in raw_TechTreeData["Techs"]:
		TechBox = CivilopediaData.TechBox(
			title=tech_data["title"],
			x=tech_data["x"],
			y=tech_data["y"],
			width=tech_data["width"],
			height=tech_data["height"],
		)
		previewstyle = ""
		if int(TechBox.x) < 200:
			previewstyle += f"left: 100%;"
		else:
			previewstyle += f"right: 100%;"
		if int(TechBox.y) < 200:
			previewstyle += f"top: 0;"
		else:
			previewstyle += f"bottom: 0;" 
		TechTree.width = max(TechTree.width, TechBox.x + TechBox.width)
		TechTree.height = max(TechTree.height, TechBox.y + TechBox.height)
  
		for datapoint in tech_data["content"]:
			contentType = datapoint.get("type", "")
			if contentType == "buttonlinkAt":
				datapoint["source"] = convertButtonImage(datapoint, buttonLookup)
				TechBox.TechBoxContent += buildHTMLLinkForButton(datapoint,isTree = True, previewstyle = previewstyle)
			elif contentType == "TechBoxLabel":
				# since TechBoxLabel coordinates are not relative to the TechBox, we need to adjust them.
				datapoint["x"] -= TechBox.x
				datapoint["x"] += 2 # padding so the Label is aligned with the TechBox content
				datapoint["y"] -= TechBox.y
				TechBox.TechBoxContent += buildHTMLForTechBoxLabel(datapoint)
		TechTree.techs.append(TechBox)
			
	for arrow in raw_TechTreeData.get("Arrows", []):
		arrow["source"] = convertButtonImage(arrow, buttonLookup)
		TechTree.arrows.append(buildHTMLForButton(arrow))
			
			
	return TechTree



def buildCivilopediaData(raw_CivilopediaData=None, buttonLookup=None, linkLookup=None, previewLookup=None):
	
	civilopedia = CivilopediaData.Civilopedia(title=raw_CivilopediaData["title"])
	
	for category_data in raw_CivilopediaData["Categories"]:
		if category_data.get("Entries", []) == []:
			continue
		# handle UpgradeTree category separately, since it has a different structure than the other categories
		if category_data.get("CategoryType", "") == "UpgradeTree":
			UpgradeTree = CivilopediaData.UpgradeTree(title=category_data["Category"])
			TreeContent = ""
			for element in category_data["Entries"][0]["PageContent"][0]["content"]:
				UpgradeTree.width = max(UpgradeTree.width, element["x"] + element["width"])
				UpgradeTree.height = max(UpgradeTree.height, element["y"] + element["height"])
				previewstyle = ""
				if int(element["x"]) < 200:
					previewstyle += f"left: 100%;"
				else:
					previewstyle += f"right: 100%;"
				if int(element["y"]) < 200:
					previewstyle += f"top: 0;"
				else:
					previewstyle += f"bottom: 0;" 
				if element.get("type", "") == "buttonlinkAt":
					element["source"] = convertButtonImage(element, buttonLookup)
					TreeContent += buildHTMLLinkForButton(element, isTree=True, previewstyle=previewstyle)
			UpgradeTree.content = TreeContent
			civilopedia.UpgradeTrees.append(UpgradeTree)
			continue
	 
		category = CivilopediaData.Category(title=category_data["Category"])
		for entry_data in category_data["Entries"]:
			entry = CivilopediaData.Entry(title=entry_data["title"])
			
			
			for i, panel_data in enumerate(entry_data.get("PageContent", [])):
				
				Panelcontent = ""
				
				# if there is another panel before the listbox, attach the infos to the panel.
				# if there is no panel before, like for the Culture Levels, attach the infos to the listbox panel.
				
				if panel_data.get("type", "") == "listbox":
					panel_data["content"].pop(0) # remove the first element, since it should contain the title too.
					texts = [content.get("text", "") for content in panel_data["content"] if content.get("text", "") not in ["", "<font=3></font>"]]
					text = resolveTextFormatting(", ".join(texts), linkLookup, previewLookup)
					if entry.PageContent != []:
						entry.PageContent[0].PanelContent += text
					else:
						Panelcontent += text
				else:
					for datapoint in panel_data.get("content", []):
						
						contentType = datapoint.get("type", "")
						
						if contentType == "text":
							Panelcontent += resolveTextFormatting(datapoint.get("text", ""), linkLookup, previewLookup)
							
						elif contentType == "button":
							datapoint["source"] = convertButtonImage(datapoint, buttonLookup)
							if panel_data["title"] == "":
								panel_data["title"] = buildHTMLForButton(datapoint)  # add button to title for the info panel
								panel_data["title"] += " "
							else:
								Panelcontent += buildHTMLForButton(datapoint)
							
						elif contentType == "buttonlink" or contentType == "buttonlinkAt":
							datapoint["source"] = convertButtonImage(datapoint, buttonLookup)
							Panelcontent += buildHTMLLinkForButton(datapoint)
							
						elif contentType == "listboxstring":
							Panelcontent += resolveTextFormatting(datapoint.get("text", ""), linkLookup, previewLookup)
							Panelcontent += "<br>"

				
				if Panelcontent != "" or panel_data["title"] != "":
					panel = CivilopediaData.Panel(title=panel_data["title"], PanelContent=Panelcontent)
					entry.PageContent.append(panel)
				
			if entry.PageContent != []:
				entry.PageContent[0].title += entry_data["title"]  # set the title of the first panel to the title of the entry
			category.entries.append(entry)
		
		civilopedia.Categories.append(category)
	
	return civilopedia



if __name__ == "__main__":
	start_new_log()
	# loading all data and preparing lookups
	print("Loading raw data and preparing lookups...")
	raw_CivilopediaData = loadCivilopediaData()
	raw_TechTreeData = loadTechTreeData()
	buttonLookup = buildButtonLookup()
	linkLookup = buildLinkLookup(raw_CivilopediaData)
	previewLookup = buildPreviewLookup(raw_CivilopediaData)
	extractGlyphsFromFontAtlas()
	print("Finished loading raw data and preparing lookups.")
	
	
	# building CivilopediaData ...
	CivilopediaData_processed = measure(buildCivilopediaData, raw_CivilopediaData, buttonLookup, linkLookup, previewLookup)
	
 
	measure(renderCategories, CivilopediaData_processed)
	measure(renderUpgradeTrees, CivilopediaData_processed)
	
	# building TechTreeData ...
	TechTreeData_processed = measure(buildTechTreeData, raw_TechTreeData, buttonLookup,linkLookup, previewLookup)
	print(f"TechTree contains {len(TechTreeData_processed.techs)} techs and {len(TechTreeData_processed.arrows)} arrows.")
	measure(renderTechChooser, TechTreeData_processed)