import klembord  # pip install klembord

import markdown
import pyperclip

def convert_markdown_to_enriched():

    # Leer el contenido del portapapeles
    md_text = pyperclip.paste()

    # Convertir el texto Markdown a HTML
    html_text = markdown.markdown(md_text)
    klembord.init()
    # Reemplazar el contenido del portapapeles con el texto enriquecido (HTML)
    klembord.set_with_rich_text("html_text", html_text)




convert_markdown_to_enriched()