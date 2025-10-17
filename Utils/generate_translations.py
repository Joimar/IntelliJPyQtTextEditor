import xml.etree.ElementTree as ET
from Utils.AppStrings import AppStrings

# This script creates .ts files without strings line number dependency

def generate_translation_template():
    # Cria a estrutura XML manualmente
    ts_root = ET.Element("TS", version="2.1", language="en")

    # Agrupa strings por contexto
    contexts = {}

    # Coleta todas as strings do AppStrings
    for attr_name in dir(AppStrings):
        if not attr_name.startswith('_'):
            attr_value = getattr(AppStrings, attr_name)
            if isinstance(attr_value, tuple) and len(attr_value) >= 3:
                context, source, text_id = attr_value[0], attr_value[1], attr_value[2]

                if context not in contexts:
                    contexts[context] = []

                contexts[context].append({
                    'source': source,
                    'id': text_id,
                    'attr_name': attr_name
                })

    # Cria os contextos no XML
    for context_name, messages in contexts.items():
        context_elem = ET.SubElement(ts_root, "context")
        name_elem = ET.SubElement(context_elem, "name")
        name_elem.text = context_name

        for msg in messages:
            message_elem = ET.SubElement(context_elem, "message")

            # Usa o ID único como localização, não o número da linha
            location_elem = ET.SubElement(message_elem, "location")
            location_elem.set("filename", "Utils/AppStrings.py")
            location_elem.set("line", f"id:{msg['id']}")  # ID único aqui!

            source_elem = ET.SubElement(message_elem, "source")
            source_elem.text = msg['source']

            translation_elem = ET.SubElement(message_elem, "translation")
            translation_elem.set("type", "unfinished")

            # Salva o arquivo
            tree = ET.ElementTree(ts_root)
            tree.write("Translations/template.ts", encoding="utf-8", xml_declaration=True)

            print("✓ Template de tradução gerado sem dependência de linhas!")

            if __name__ == "__main__":
                generate_translation_template()
