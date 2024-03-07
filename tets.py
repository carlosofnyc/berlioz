import wikipedia
import mwparserfromhell

def get_infobox(page_name):
    page = wikipedia.page(page_name)
    raw = page.html()
    wikicode = mwparserfromhell.parse(raw)
    infoboxes = [template for template in wikicode.filter_templates() 
                 if template.name.strip().lower().startswith("infobox")]
    return infoboxes[0] if infoboxes else None

infobox = get_infobox("Japan")
print(infobox)