import os
BASIS_PFAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notizen") 

def find_txt_and_md_files(ordner):
    """Gibt die .txt- und .md-Dateien eines Ordners zurück, alphabetisch sortiert.

    Ergebnis immer ein Dictionary mit "erfolg":
      Erfolg: {"erfolg": True,  "dateien": [...]}
      Fehler: {"erfolg": False, "fehler": "Text, den das Modell lesen kann"}

    Ein leerer Ordner (oder einer ohne .txt/.md-Dateien) ist ein ERFOLG mit
    leerer Liste: Der Aufruf hat geklappt, es gibt nur nichts zu finden. Ein
    Fehler bedeutet "ich konnte nicht nachsehen".
    """

    BASIS_PFAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notizen")                             

    basis = os.path.realpath(BASIS_PFAD)
    voll = os.path.realpath(os.path.join(basis, ordner))

    try:
        erlaubt = os.path.commonpath([basis, voll]) == basis
    except ValueError:                             
        erlaubt = False

    if not erlaubt:                                     
        return {"erfolg": False,
        "fehler": f"Zugriff verweigert: '{ordner}' liegt außerhalb des erlaubten Ordners."}


    try:
        eintraege = os.listdir(voll)
    except FileNotFoundError:
        return {"erfolg": False, "fehler": f"Ordner '{ordner}' existiert nicht."}
    except OSError as e:
        return {"erfolg": False, "fehler": f"Ordner '{ordner}' nicht lesbar: {e}"}

    dateien = []
    for name in eintraege:
        pfad = os.path.join(voll, name)
        if name.endswith((".txt", ".md")) and os.path.isfile(pfad):
            dateien.append(name)

    return {"erfolg": True, "dateien": sorted(dateien)}
