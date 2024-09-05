"""
FEUILLE-CLI
(2024 FeuilleDev team)
"""

import os
import re
import json

def link_(folder,main_file,config_file):
    print("[+] Linking all files in /src (this can take some times)")
    TMP = ""
    CONFIG = config_file
    if str(CONFIG["files_order_actived"]) == "true" :
        print("[+] File order actived")
        for i in CONFIG["files_order"]:
            if i.endswith(".lua") and i != main_file:
                print(f"-> Linking : {folder}/{i}")
                file = open(f"{folder}/{i}", "r")
                TTMPTEXT = f"-- === {i} ==="
                TMP += f"{TTMPTEXT}\n{file.read()}\n"
    else:
        for i in os.listdir(folder):
            if i.endswith(".lua") and i != main_file:
                print(f"-> Linking : {folder}/{i}")
                file = open(f"{folder}/{i}", "r")
                TTMPTEXT = f"-- === {i} ==="
                TMP += f"{TTMPTEXT}\n{file.read()}\n"
    print(f"[+] Done")
    TMP += open(f"{folder}/{main_file}","r").read()
    TMP += "\n\n-- Made with Feuille Linker"
    return TMP
def minify_(text):
    print("[WARNING] : Minifying is not stable yet.")
    input("Press enter to continue")
    print("[+] Minifying")
    output = re.sub(r'--\[\[.*?\]\]', '', text, flags=re.DOTALL)
    output = re.sub(r'--.*', '', output)
    output = re.sub(r'^\s+|\s+$', '', output, flags=re.MULTILINE)
    output = re.sub(r'\n+', '\n', output)
    output = re.sub(r'\s*([=+-/*%<>~])\s*', r'\1', output)
    output = re.sub(r'\s*([\(\)])\s*', r'\1', output)
    output = re.sub(r'\s*,\s*', ',', output)

    output = output.replace('\n', '')
    return output
class terminal_utils:
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
class Secrets_Handlers():

    def __init__(self):
        self.init() 
        if "FEUILLE_KEYS" in os.environ:
            self.keys = json.loads(os.environ["FEUILLE_KEYS"])
            
            
    def modify_key(self,key_name,value):
         if self.keys["keys"][key_name] is not None:
             self.keys["keys"][key_name] = value
         else:
             self.keys["keys"][key_name] = value
    def get_key(self,key_name):
        if self.keys["keys"][key_name] is not None:
            return self.keys["keys"][key_name]
        else:
            return None
    def delete_key(self,key_name):
        if self.keys["keys"][key_name] is not None:
            del self.keys["keys"][key_name]
        else:
            return None
    def save(self):
        os.environ["FEUILLE_KEYS"] = json.dumps(self.keys)
    def init(self):
        if "FEUILLE_KEYS" in os.environ:
            pass
        else:
            TEMP_JSON = """
        {
            "WARNING": "DO NOT SHARE THIS FILE WITH ANYONE",
            "feuille":"true",
            "keys":[{"DJAPPSTORE":"MYKEY"},{"FEUILLESTORE":"MYKEY"},{"PAXOSTORE":"MYKEY"}]
        }
        """
            os.environ["FEUILLE_KEYS"] = json.dumps(json.loads(TEMP_JSON))


class Stores_Handlers():
    print("[+] : Loading...")
    def dj_appstore():
        print("[+] : Todo")
    def feuillestore():
        print("[+] : Todo")
    def paxostore():
        print("[+] : Todo")

#print(minify_(compile_("test")))