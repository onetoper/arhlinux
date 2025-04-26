import os
import re
import colorama
import ipinfo
import requests
import subprocess
from colorama import Fore, init
from bs4 import BeautifulSoup
from apiverve_phonenumbervalidator.apiClient import PhonenumbervalidatorAPIClient


script_dir = os.path.dirname(os.path.abspath(__file__))


api = PhonenumbervalidatorAPIClient("4ae37b34-e5b8-405c-ae0f-4c39f8b7bc52")

access_token = "1a9fac0a2e4c0c"
handler = ipinfo.getHandler(access_token)

def get_ip_details(ip_address):
    try:
        details = handler.getDetails(ip_address)
        data = details.all
        print(f"\n{Fore.YELLOW}=== IP Address Details ===")
        print(f"{Fore.CYAN}IP Address:{Fore.WHITE} {data.get('ip', ip_address)}")
        print(f"{Fore.CYAN}Hostname:{Fore.WHITE} {data.get('hostname', 'N/A')}")
        print(f"{Fore.CYAN}City:{Fore.WHITE} {data.get('city', 'N/A')}")
        print(f"{Fore.CYAN}Region:{Fore.WHITE} {data.get('region', 'N/A')}")
        print(f"{Fore.CYAN}Country:{Fore.WHITE} {data.get('country_name', 'N/A')} ({data.get('country', 'N/A')})")
        print(f"{Fore.CYAN}Location:{Fore.WHITE} {data.get('loc', 'N/A')}")
        print(f"{Fore.CYAN}Postal Code:{Fore.WHITE} {data.get('postal', 'N/A')}")
        print(f"{Fore.CYAN}Timezone:{Fore.WHITE} {data.get('timezone', 'N/A')}")
        print(f"{Fore.CYAN}Organization:{Fore.WHITE} {data.get('org', 'N/A')}")

        asn = data.get('asn', {})
        if isinstance(asn, dict):
            print(f"{Fore.CYAN}ASN:{Fore.WHITE} {asn.get('asn', 'N/A')}")
        else:
            print(f"{Fore.CYAN}ASN:{Fore.WHITE} {asn}")

    except Exception as e:
        print(f"\n{Fore.RED}Error getting IP info: {str(e)}")
        print(f"{Fore.YELLOW}Note: Free ipinfo.io accounts have limited requests per day")
def search_ip_in_database(ip_address):
    found_lines = []
    try:
        with open(database_path, "r", encoding="utf-8") as file:
            for line in file:
                if re.search(rf"\b{re.escape(ip_address)}\b", line):
                    found_lines.append(line.strip())
        
        if found_lines:
            print(f"\n{Fore.GREEN}Found matches in database:")
            for i, found_line in enumerate(found_lines, 1):
                print(f"{Fore.YELLOW}{i}. {found_line}")
        else:
            print(f"\n{Fore.RED}No matches found in database")
            
    except FileNotFoundError:
        print(f"\n{Fore.RED}Error: database file not found!")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}")


os.system("cls")

init()
print(" ")
print(colorama.Fore.RED + "        ██          ████        ██     ██")
print("       ████         ██  ██      ██     ██")
print("      ██  ██        ██  ██      █████████")
print("     ██    ██       ████        ██     ██")
print("    ██████████      ██  ██      ██     ██")
print("   ██        ██     ██   ██     ██     ██")
print(" ")

while True:
    print("> [1] - searcher")
    print("> [2] - IP info")
    print("> [3] - number info")
    print("> [4] - DoS")
    print("> [5] - osint manuals")
    print("> [6] - swat manuals")
    try:
        choise = int(input("> enter the number of what you need: "))
    except ValueError:
        print("[!] Please enter a valid number!")
        continue
    
    if choise == 1:
        keyword = input("> enter name/sname and etc to search in format Alexander;Alexandrov: ")
        found_lines = []
        found_results = {}
        script_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            txt_files = [f for f in os.listdir(script_dir) if f.endswith('.txt')]
            
            if not txt_files:
                print("\n> No .txt files found in directory!")
                input("> enter some text here to go to main screen...")
            print(f"\n> Searching in files: {', '.join(txt_files)}")

            for txt_file in txt_files:
                file_path = os.path.join(script_dir, txt_file)
                found_lines = []

                print(f"\n> Scanning file: {txt_file}")
            
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        if re.search(keyword, line, re.IGNORECASE):
                            found_lines.append(line.strip())
                            print(f"> Found match: {line.strip()}")
            
            if found_lines:
                found_results[txt_file] = found_lines
        
            if found_results:
                print("\n> Found matches:")
                for file_name, lines in found_results.items():
                    print(f"\n> In file '{file_name}':")
                    for i, line in enumerate(lines, 1):
                        print(f"{i}. {line}")
            else:
                print("\n> No matches found in any .txt files")
            
        except Exception as e:
            print(f"\n[!] An error occurred: {str(e)}")
    
        input("> enter some text here to go to main screen...")
    elif choise == 2:
        ip_address = input("> enter target IP address: ")
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_address):
            get_ip_details(ip_address)
            print(f"\n{Fore.YELLOW}=== Database Search ===")
            search_ip_in_database(ip_address)
        else:
            print(f"{Fore.RED}[!] Invalid IP address format!")
            
    elif choise == 3:
        try:
            if os.path.isfile('last.txt'):
                os.remove('last.txt')
        
            phone = input("> phone number: ")
            if not phone.strip():
                print("[!] Phone number cannot be empty")
                continue
        
            service = "http://phoneradar.ru/phone/"
            link = service + phone

            def get_html(link):
                try:
                    r = requests.get(link, timeout=10)
                    r.raise_for_status()
                    return r
                except requests.RequestException as e:
                    print(f"[!] Error fetching data: {str(e)}")
                    return None

            def parse():
                html = get_html(link)
                if html is None:
                    return
            
                soup = BeautifulSoup(html.text, 'html.parser')
                result = soup.find('tbody')
            
                if result is None:
                    print("[!] No information found for this number")
                    return
                
                try:
                    with open("last.txt", 'w', encoding='utf-8') as out:
                        out.write(result.get_text(separator='\n', strip=True))
                        print(f"\n> Information saved to last.txt\n")
                
                    print("Number:", phone)
                    print("\n> Result:\n")
                    with open("last.txt", 'r', encoding='utf-8') as file:
                        for line in file:
                            if line.strip():
                                print(line.strip())
                except IOError as e:
                    print(f"[!] File error: {str(e)}")

            parse()
        except Exception as e:
            print(f"[!] An unexpected error occurred: {str(e)}")
    elif choise == 4:
        target = input("enter target IP(example: https://8.8.8.8): ")
        with open("target.txt", "w", encoding="utf-8") as file:
            file.write(target)
        subprocess.run(["python", "botnet\\1.py"])
        subprocess.run(["python", "botnet\\2.py"])
        subprocess.run(["python", "botnet\\3.py"])
        subprocess.run(["python", "botnet\\4.py"])
        subprocess.run(["python", "botnet\\5.py"])
        subprocess.run(["python", "botnet\\6.py"])
        subprocess.run(["python", "botnet\\7.py"])
        subprocess.run(["python", "botnet\\8.py"])
        subprocess.run(["python", "botnet\\9.py"])
        subprocess.run(["python", "botnet\\10.py"])
    elif choise == 5:
        try:
            file_path = os.path.join(script_dir, 'manualosint.txt')
            with open(file_path, 'r', encoding='utf-8') as f:
             for line in f:
                 print(line, end='')
        except FileNotFoundError:
            print(f"{Fore.RED}Файл manualosint.txt не найден в папке: {script_dir}")
        except UnicodeDecodeError:
            print(f"{Fore.RED}Ошибка кодировки! Попробуйте сохранить файл в UTF-8.")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при чтении файла: {e}")

    elif choise == 6:
        try:
            file_path = os.path.join(script_dir, 'manualswat.txt')
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    print(line, end='')
        except FileNotFoundError:
         print(f"{Fore.RED}Файл manualswat.txt не найден в папке: {script_dir}")
        except UnicodeDecodeError:
            print(f"{Fore.RED}Ошибка кодировки! Попробуйте сохранить файл в UTF-8.")
        except Exception as e:
            print(f"{Fore.RED}Ошибка при чтении файла: {e}")
    else:
        print("\n[!] Invalid choice. Please try again.")   
