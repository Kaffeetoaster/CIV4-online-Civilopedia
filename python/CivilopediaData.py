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








