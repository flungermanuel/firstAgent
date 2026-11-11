import json
import anthropic
from dotenv import load_dotenv
load_dotenv()
from find_txt_and_md_files import find_txt_and_md_files

MODEL = "claude-haiku-5-5"
client = anthropic.Anthropic()
tools = [
    {
        "name" : "find_txt_and_md_files",
        "description" : "gibt alle dateien die eine .txt oder md endung haben in einem dictonary mit erfolg : boolean , dateien : liste oder fehler : fehler mit namen von .txt oder .md dateien von einem ordner ist nicht geiegnet wenn nutzer nach bearbeitung von dateien fragt. nicht geiegnet wenn der nutzer nach aktionen wie zählen von zeilen fragt. nicht wenn der nutzer eine auflistung von anderen dateiendungen wie .png etc haben will. nicht geiegnet wenn der Nutzer den inhalt einer datei ausgeben will. Bei einem der ordner existiert niccht fehlerfall soll dem nutzer dieser fehler mitgeteilt werden und nochmal nach dem korrekten namen des ordners nachgefragt werden.Wenn der orndername fehlt frag nach wie der zu durchsuchende ordner heißt "
        "",
        "input_schema" : {
            "type": "object",
            "properties" : {
                "ordner" :{
                    "type" : "string",
                    "description" : "name des zu durchsuchenden ordners zB notizen"
                } 
            },

            "required" : ["ordner"]
        }
    }   
    ]  

TOOL_FUNKTIONEN = {"find_txt_and_md_files": find_txt_and_md_files}

SYSTEM_PROMPT = "Du hilfst bei Fragen zu Textdateien in Ordnern. Antworte auf Deutsch, kurz und gut lesbar."


def frage_agent(messages,frage, max_runden=5):
    messages.append({"role": "user", "content": frage})

    for runde in range(max_runden):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":  
            liste=[]
            for block in response.content:
                if block.type == "text":
                    liste.append(block.text) 

            
            final= "\n".join(liste)
            messages.append({"role": "assistant", "content": response.content})
            return final

        messages.append({"role": "assistant", "content": response.content})

        ergebnisse = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  [Runde {runde + 1}] Tool: {block.name}({block.input})")
                funktion = TOOL_FUNKTIONEN[block.name]            
                ergebnis = funktion(**block.input)
                ergebnisse.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(ergebnis, ensure_ascii=False),
                })

        if ergebnisse:
            messages.append({"role" : "user" , "content" : ergebnisse})     

    return "Abbruch: zu viele Runden."


if __name__ == "__main__":

    gedächtnis = []

    while True :

        user_input = input("Du: ")

        if user_input.lower() in ["exit" , "quit" , "schließen"] : 
            print("Claude : Tschüss")
            break

        if not user_input.strip():
            continue


        print("Claude denkt nach ...")
        antwort = frage_agent(gedächtnis,user_input)

        print (f"\nClaude:{antwort}\n")

