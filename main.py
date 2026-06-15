from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from InitGameInfo import initGameInfos
from config import INPUT_PATH, OUTPUT_PATH
from python.helper.measure_duration import measure, start_new_log

from python.Pedia.PediaCultureLevel import build_CultureLevel_Page
from python.Pedia.PediaBuildings import build_Building_Page, build_ReligiousBuilding_Page, build_UniqueBuilding_Page, build_GreatPeopleBuilding_Page, build_NationalWonder_Page, build_GreatWonder_Page

start_new_log()

PediaCategories = {
	"CultureLevels": build_CultureLevel_Page(),
	"Buildings": build_Building_Page(),
	"ReligiousBuildings": build_ReligiousBuilding_Page(),
	"UniqueBuildings": build_UniqueBuilding_Page(),
	"GreatPeopleBuildings": build_GreatPeopleBuilding_Page(),
	"NationalWonders": build_NationalWonder_Page(),
	"GreatWonders": build_GreatWonder_Page()
}


TEMPLATE_DIR = Path(__file__).resolve().parent / "jinja_templates"



def renderCategory(PageInfos, result_file, template_name= "template_page.jinja"):
	environment = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
 
	template = environment.get_template(template_name)
	rendered_html = template.render(page = PageInfos)
	result_file.write_text(rendered_html, encoding="utf-8")


def renderCategories():
	for category, page in PediaCategories.items():
		print(f"Rendering category {category}...")
		result_file = OUTPUT_PATH/ "Categories" / f"{category}.md"
		
		renderCategory(page, result_file)
		print(f"Finished rendering category {category}. Result saved to {result_file}")


if __name__ == "__main__":
	
	measure(initGameInfos)
	#print(PediaCategories["Buildings"]) 
	measure(renderCategories)
