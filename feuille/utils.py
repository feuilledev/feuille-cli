"""
FEUILLE-CLI
(2024 FeuilleDev team)
"""

import os
import re
import json
#import zipfile
import tarfile
import requests

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
class Secrets_Handlers:
    def __init__(self):  
        self.home_dir = os.path.expanduser("~")
        self.file_path = os.path.join(self.home_dir, "feuille_key.json")     
        if os.path.exists(self.file_path):
            self.keys = json.loads(open(self.file_path,"r").read())
            #raise ValueError(self.keys)
        else:
            self.init() 
            self.keys = {"keys": {}}
            
    def modify_key(self, key_name, value):
        if key_name not in self.keys["keys"]:
            raise ValueError("No keys found")
        self.keys["keys"][key_name] = value
        self.save()

    def get_key(self, key_name):
        return self.keys.get("keys", {}).get(key_name, None)
    
    def delete_key(self, key_name):
        if "keys" in self.keys and key_name in self.keys["keys"]:
            self.keys["keys"].pop(key_name, None)
    
    def save(self):
        with open(self.file_path,"w") as f:
            f.write(json.dumps(self.keys))
    
    def init(self):
        if "FEUILLE_KEYS" not in os.environ:
            TEMP_JSON = """
            {
                "WARNING": "DO NOT SHARE THIS FILE WITH ANYONE",
                "feuille": "true",
                "keys": {"DJAPPSTORE": "MYKEY", "FEUILLESTORE": "MYKEY", "PAXOSTORE": "MYKEY"}
            }
            """
            with open(self.file_path,"w") as f:
                f.write(TEMP_JSON)


class Stores_Handlers():
    print("[+] : Loading...")
    # ik this code is very ugly...
    def dj_appstore():
        SCRET = Secrets_Handlers()
        data = json.load(open("feuille.json","r"))
        print("[+] : Getting token from DB")
        if SCRET.get_key("DJAPPSTORE") is  None or SCRET.get_key("DJAPPSTORE") == "MYKEY":
            print("[?] : Enter your DJAppStoreKey")
            SCRET.modify_key("DJAPPSTORE",input("Key : "))
            print("[+] : Done")
            Stores_Handlers.dj_appstore()
        else:
            print("[+] : Checking for recent build...")
            if os.path.exists("dist/app.lua"):
                print("[+] : Build found")
                print("[+] : Zipping...")
                with tarfile.open("export.tar", "w") as tar:
                    tar.add("dist/app.lua")
                    tar.add("dist/assets")
                    for i in os.listdir("dist/assets"):
                        tar.add(f"dist/assets/{i}")
                    tar.add("feuille.json")
                print("[+] : Uploading...")
                ICON_PATH = f'dist/{data["assets_folder"]}/{data["icon"]}'
                x = requests.get(url="https://45.90.12.31:6517/add_app/paxo/",verify=False,cookies={"id_creator":SCRET.get_key("DJAPPSTORE")},data={"name":data["name"],"description":data["description"]},files={"icon":open(ICON_PATH,"rb"),"appfile":open("export.tar","rb")})
                print(x.status_code)
                print(x.text)
                print("[+] : Done")
                input("pres enter to exit")
            else:
                print("[-] : No build found")
                print("[TIPS] : Use feuille -l to link all files and distribute your app !")

    def feuillestore():
        print("[+] : Todo")
    def paxostore():
        print("[+] : Todo")

#print(minify_(compile_("test")))
