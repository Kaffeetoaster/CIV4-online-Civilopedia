from dataclasses import dataclass, field




@dataclass
class Panel:
	title: str
	PanelContent: str = ""

@dataclass
class Entry:
	title: str
	PageContent: list[Panel] = field(default_factory=list)

@dataclass
class Category:
	title: str
	entries: list[Entry] = field(default_factory=list)
 
@dataclass
class Civilopedia:
	title: str
	Categories: list[Category] = field(default_factory=list)



@dataclass
class TechBox:
	title: str
	x: int
	y: int
	width: int
	height: int
	TechBoxContent: str = ""  # contains the tech name, tech icon and tech effects



@dataclass
class TechChooser:
	title: str
	width: int = 0
	height: int = 0
	techs: list[TechBox] = field(default_factory=list)
	arrows: str = ""  # contains the arrows between the techs as html elements





