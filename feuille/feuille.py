
'''
🌿 FEUILLE-CLI
(2024 FeuilleDev team)
'''

import argparse
import json
from .utils import *
import base64
import shutil
import subprocess
import threading
import zipfile

TEMPLATE_JSON = """
{
    "name":"App_Name",
    "src_folder":"src",
    "app_main": "main.lua",
    "app_version": "1.0.0",
    "app_author": "Author",
    "files_order_actived": "false",
    "icon": "icon.png",
    "description": "Description",
    "files_order": [
        "function_test.lua",
        "function_test_hello.lua"
    ],
    "assets_folder":"assets",
    "permissions": {"storage": "true", "internet": "true"},
    "feuille_version":"1.0.0"
}

"""
VERSION = "1.0.0"


def main():
    secretshad = Secrets_Handlers()
    terminal_utils.clear()
    print(f"== Feuille CLI (V {VERSION}) ==")
    print("[?] : Need help ? Use -h")
    argparser = argparse.ArgumentParser(description='Feuille CLI')
    argparser.add_argument('-v', '--version', help='Show the version of the program', action='store_true')
    argparser.add_argument('-n', '--new', help='Create a new feuille project', action='store_true')
    argparser.add_argument('-l', '--link', help='Link all files from a folder', action='store_true')
    argparser.add_argument('-c', '--config', help='Configuration of the feuille project', action='store_true')
    argparser.add_argument('-u', '--upload', help='Upload the app to DJAppStore/FeuilleStore/PaxoStore', action='store_true')
    argparser.add_argument('-r', '--run', help='Launch the emulator', action='store_true')
    argparser.add_argument('-t', '--tar', help='Exporting to a tar.gz', action='store_true')
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
        temp_demojson = json.loads(TEMPLATE_JSON)
        #_APP_MAIN = input("[?] : Main file : ")
        _APP_VERSION = input("[?] : Version : ")
        _APP_AUTHOR = input("[?] : Author : ")
        temp_demojson["icon"] = "icon.png"
        temp_demojson["description"] = input("[?] : Description : ")
        print("[+] Creating a new feuille project")
        
        temp_demojson["name"] = _NAME
        temp_demojson["app_main"] = "app.lua"
        temp_demojson["app_version"] = _APP_VERSION
        temp_demojson["app_author"] = _APP_AUTHOR
        temp_demojson["feuille_version"] = VERSION
        
        with open("feuille.json", "w") as f:
            json.dump(temp_demojson, f, indent=4)
        os.makedirs("src")
        with open("src/app.lua", "w") as f:
            f.write(f"print(\"My first lua file\")") 
        os.makedirs("assets")
        with open("assets/icon.png","wb") as f:
            f.write(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHqSURBVGhD7ZaxSgQxEIZ9ETs7OztfxJfwCex8BsGXsLMQQURbOwvBRjvhPA9EjkO8RiP/3c75O06yWTeLg+SDKTJJZvdLcrldC/+EKuKNKuKNKuKNKuKNLJHR23G4mx00LZ9kiUDiZLTetHxSfyPecCcymV+Gi6ftRTy8HjXZJei7et75kQfuRM7HW4vfI+L0caPJLpE+nQeuRLDiIiHBxPIgSyS1pSkwHkdEHm4dF4Z3Q4LHc16TJZLaUo2ccX4oB2rEZGLjBc5rskRSBRhInI03v423wloQ61hJCFZOKCpiHY3rl93w/jEP97PDVe5mutfM+MKaKyFYOaGYiF5R62VT6LncFqyc0Fkkdr71inZFz9VtYOWELBGcaSkQ+8HzQ7ruBuD5VhtYOSFLhM+3VQS09beh5/Pi4flAj2GyRECqCGjrb0PPv53ur9pyCvQYxq0IbjrO6ctEM4hI6t87Bs8XONd2mRQTybkQUlj1OcdhXSbFRPSF0HVXeK7AOQ6LYiKgz65Y9bme1c8UFemzKzxP0PV0P1NUBMRWkcP6nOd+RteL/dkWF4mtog599PiFGa6X+mIoLgJyZPRLyZzffN6AQUT+girijSrijWyR2PXohWyRvtfj0GSLeKeKeKOKeKOKeKOK+CKET7D7L+5+3zraAAAAAElFTkSuQmCC"))
        
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
                print("[+] : Copying assets")
                if os.path.exists("dist/assets"):
                    shutil.rmtree("dist/assets")
                    os.makedirs("dist/assets")
                else:
                    os.makedirs("dist/assets")
                for i in os.listdir("assets"):
                    print(i)
                    shutil.copy(f"assets/{i}",f"dist/assets/{i}");shutil.copy(f"assets/{i}",f"dist/{i}")
                #adding all files under /dist folder to a tar.gz
                with tarfile.open("dist/dist.tar", "w:gz") as tar:
                    tar.add("dist", arcname=os.path.basename("dist"))
                    tar.add("feuille.json")
                print("[+] : Linking done, saved in /dist/app.lua / or for sending to a appstore saved to /dist/dist.tar")
        else:
            print("[-] Not found")
            print("Please create a new project.")
    elif args.config:
        print("Searhing for a feuille.json")
        if os.path.exists("feuille.json"):
            print("[+] Found")
            terminal_utils.clear()
            with open("feuille.json", "r") as f:
                data = json.load(f)
                _LIST_ORDERS_FILE = data["files_order"]
                _LIST_ORDERS_ACTIVED = data["files_order_actived"]
                print("ACTUAL CONFIG :")
                print(f"[+] Name : {data['name']}")
                print(f"[+] Main file : {data['app_main']}")
                print(f"[+] Version : {data['app_version']}")
                print(f"[+] Author : {data['app_author']}")
                if _LIST_ORDERS_ACTIVED == "true":
                    print(f"[+] Files order actived")
                    for i in _LIST_ORDERS_FILE:
                        print(f" - {i}")
                else:
                    print(f"[+] Files order inactived")

        else:
            print("[-] Not found")
            print("Please create a new project.")
    elif args.upload:
        if os.path.exists("feuille.json"):
            store_select = ""
            while store_select not in ["exit","EXIT","2"]:
                terminal_utils.clear()
                print("🌿 FEUILLE-CLI")
                print("====================================================")
                print(" [1] : FeuilleStore \n [2] : DJAppStore \n [IN-DEV] : PaxoStore")
                print("[TIPS] : Type exit, EXIT to leave.")
                store_select = input("[?] : Select a store to upload to : ")
                if store_select == "2":
                    Stores_Handlers.dj_appstore()
    elif args.tar:
        if os.path.exists("feuille.json"):
            # adding folder /src and assets to a tar.gz (creating)
            if not os.path.exists("dist"):
                os.mkdir("dist")
            with tarfile.open("dist/dist.tar", "w:gz") as tar:
                tar.add("src", arcname=os.path.basename("src"))
                tar.add("assets", arcname=os.path.basename("assets"))
                tar.add("feuille.json")
            print("[+] : Export done, saved in /dist/dist.tar")
        else:
            print("[-] : No feuille project found")
    elif args.run:
        if os.path.exists("feuille.json"):
            print("[+] : Checking for emulator")
            if os.path.exists("paxoemu/program.exe"):
                print("[+] : Emulator found")
                process_sub =subprocess.Popen("paxoemu/program.exe")
                # monitoring ram usage (if depass > 4mo closing and warning)
                def monitor_emulator():
                    while True:
                        if process_sub.poll() is not None:
                            print("[+] : Emulator closed")
                            break
                        # check exit code
                        if process_sub.returncode is not None:
                            if process_sub.returncode == 0:
                                print("[+] : Emulator closed")
                                break
                            else:
                                print("[!] : Emulator closed with error code")
                                break
                        else:
                            terminal_utils.clear()
                            print("====================================================")
                            print("MONITORING IN PROCESS")
                            print("> FeuilleCLI is actually monitoring the emulator")
                            import psutil
                            process = psutil.Process(process_sub.pid)
                            ram = process.memory_info().rss
                            if ram > 4*1024*1024*1024:
                                print("[!] : RAM usage is too high, closing")
                                process_sub.kill()
                                break     
                            print(F"RAM usage : {ram/1024/1024/1024} Mo/4 Mo")
                            print("====================================================")

                            time.sleep(1)
                thread = threading.Thread(target=monitor_emulator)
                thread.start()
            else:
                print("[-] : Emulator not found")
                print("Downloading PaxoEmulator")
                x = requests.get("https://github.com/paxo-phone/PaxOS-9/releases/download/stable/windows-build.zip")
                with open("paxoemu.zip","wb") as f:
                    f.write(x.content)
                print("[+] : Unzipping")
                with zipfile.ZipFile("paxoemu.zip", "r") as zip_ref:
                    zip_ref.extractall("paxoemu")
                print("[+] : Copying storage folder to project root")
                # copying everthing froom the root folder
                os.makedirs("storage")
                xstorage = requests.get("https://github.com/feuilledev/files/raw/refs/heads/main/emu-storage.zip")
                with open("storage.zip","wb") as f:
                    f.write(xstorage.content)
                with zipfile.ZipFile("storage.zip", "r") as zip_ref:
                    zip_ref.extractall("storage")
                    
                print("[+] : Cleaning")
                os.remove("paxoemu.zip")
                os.remove("storage.zip")
                print("[+] : Please relaunch the command")
        else:
            print("[-] : No feuille.json found")
        
if __name__ == "__main__":
    main()