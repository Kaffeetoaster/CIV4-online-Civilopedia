This is the backend script for creating an online version of a Civ4 Civilopedia. It parses the XML files for the game infos and recreates the Civilopedia look using mkdocs with the readyourdocs theme.
To use it one must define an *INPUT_PATH* variable, that points to the (mod) folder, whose information one wants to display and an *OUTPUT_PATH* variable, that should point to a /docs folder. 
Both these variables must set in a config.py file.
The last thing needed is a mkdocs style mkdocs.yml, wherre among other things the toc will be defined.
For both files a template file is included.
