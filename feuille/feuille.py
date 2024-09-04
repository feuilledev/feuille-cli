'''
🌿 FEUILLE-CLI
(2024 FeuilleDev team)
'''

import argparse
import json
from .utils import *
TEMPLATE_JSON = """
{
    "name":"App_Name",
    "src_folder":"src",
    "app_main": "main.lua",
    "app_version": "1.0.0",
    "app_author": "Author",
    "files_order_actived": "false",
    "files_order": [
        "function_test.lua",
        "function_test_hello.lua"
    ],

    "feuille_version":"1.0.0"
}

"""
VERSION = "1.0.0"
def main():
    print(f"== Feuille CLI (V {VERSION}) ==")
    print("[?] : Need help ? Use -h")
    argparser = argparse.ArgumentParser(description='Feuille CLI')
    argparser.add_argument('-v', '--version', help='Show the version of the program', action='store_true')
    argparser.add_argument('-n', '--new', help='Create a new feuille project', action='store_true')
    argparser.add_argument('-l', '--link', help='Link all files from a folder', action='store_true')
    argparser.add_argument('-c', '--config', help='Configuration of the feuille project', action='store_true')
    argparser.add_argument('-u', '--upload', help='Upload the app to DJAppStore/FeuilleStore/PaxoStore', action='store_true')
    args = argparser.parse_args()

    if args.version:
        print("Version : 1.0.0")
    elif args.new:
        print("Creating a new feuille's project")
        print("[TIPS] : Use this code when creating functions")
        print("""
        local my_function = function()
                print("Hello")
        end
    """)
        print("If you do want to mess with the files order + bugs")
        _NAME = input("[?] : Name of the app : ")
        _APP_MAIN = input("[?] : Main file : ")
        _APP_VERSION = input("[?] : Version : ")
        _APP_AUTHOR = input("[?] : Author : ")
        print("[+] Creating a new feuille project")
        temp_demojson = json.loads(TEMPLATE_JSON)
        temp_demojson["name"] = _NAME
        temp_demojson["app_main"] = _APP_MAIN
        temp_demojson["app_version"] = _APP_VERSION
        temp_demojson["app_author"] = _APP_AUTHOR
        temp_demojson["feuille_version"] = VERSION
        with open("feuille.json", "w") as f:
            json.dump(temp_demojson, f, indent=4)
        os.makedirs("src")
        with open("src/main.lua", "w") as f:
            f.write(f"print(\"My first lua file\")") 
        print("[+] Done, Happy coding !")
        print("[TIPS] : Use feuille -l to link all files and distribute your app !")

    elif args.link:
        print("Searching for a feuille.json")
        if os.path.exists("feuille.json"):
            print("[+] Found")
            with open("feuille.json", "r") as f:
                data = json.load(f)
                x=link_(data["src_folder"],main_file=data["app_main"],config_file=data)
                print("[?] Do you want to minify it ? (y/n)")
                e = input()
                if e.lower() == "y":
                    print("[+] Minifying")
                    x=minify_(x)
                else:
                    print("[+] Skipping minify")
            
                if os.path.exists("dist"):
                    pass
                else:
                    os.mkdir("dist")
                with open("dist/app.lua", "w") as f:
                    f.write(x)
                print("[+] Done, saved in /dist/app.lua")
        else:
            print("[-] Not found")
            print("Please create a new project.")
    elif args.config:
        print("Searhing for a feuille.json")
        if os.path.exists("feuille.json"):
            print("[+] Found")
            with open("feuille.json", "r") as f:
                data = json.load(f)
                print("TODO")
        else:
            print("[-] Not found")
            print("Please create a new project.")
    elif args.upload:
        print("TODO")
if __name__ == "__main__":
    main()