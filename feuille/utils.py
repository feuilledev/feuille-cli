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
#print(minify_(compile_("test")))