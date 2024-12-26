import asyncio
import random
import ssl
import json
import time
import uuid
import base64
import aiohttp
from datetime import datetime
from colorama import init, Fore, Style
from websockets_proxy import Proxy, proxy_connect

init(autoreset=True)

def gradient_text(text, colors):
    gradient = ""
    for i, char in enumerate(text):
        gradient += f"\033[38;2;{colors[i % len(colors)][0]};{colors[i % len(colors)][1]};{colors[i % len(colors)][2]}m{char}"
    return gradient + Style.RESET_ALL

# Gradient banner with RGB colors
BANNER_TEXT = """
 -================= ≫ ──── ≪•◦ ❈ ◦•≫ ──── ≪=================-
 │                                                          │
 │  ██████╗  █████╗ ██████╗ ██╗  ██╗                        │
 │  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝                        │
 │  ██║  ██║███████║██████╔╝█████╔╝                         │
 │  ██║  ██║██╔══██║██╔══██╗██╔═██╗                         │
 │  ██████╔╝██║  ██║██║  ██║██║  ██╗                        │
 │  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝                        │
 │                                                          │
 │                                                          │
 ╰─━━━━━━━━━━━━━━━━━━━━━━━━Termux-os━━━━━━━━━━━━━━━━━━━━━━━─╯
"""
GRADIENT_COLORS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 127, 255), (0, 0, 255), (139, 0, 255)]
BANNER = gradient_text(BANNER_TEXT, GRADIENT_COLORS)

EDGE_USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.57",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.46",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.128",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.112",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.98",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.83",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.133",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.121",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91"
]

HTTP_STATUS_CODES = {
    200: "OK",
    201: "Created", 
    202: "Accepted",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden", 
    404: "Not Found",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

def colorful_log(proxy, device_id, message_type, message_content, is_sent=False, mode=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    color = Fore.GREEN if is_sent else Fore.BLUE
    action_color = Fore.YELLOW
    mode_color = Fore.LIGHTYELLOW_EX
    
    log_message = (
        f"{Fore.WHITE}[{timestamp}] "
        f"{Fore.MAGENTA}[Proxy: {proxy}] "
        f"{Fore.CYAN}[Device ID: {device_id}] "
        f"{action_color}[{message_type}] "
        f"{color}{message_content} "
        f"{mode_color}[{mode}]"
    )
    
    print(log_message)

async def connect_to_wss(socks5_proxy, user_id, mode):
    # As before (unchanged)

async def main():
    print(BANNER)
    print(f"{Fore.CYAN}dark life 🧬| GetGrass Crooter V2{Style.RESET_ALL}")
    
    # Add password protection
    password = input(f"{Fore.YELLOW}Enter password to proceed: {Style.RESET_ALL}").strip()
    if password != "darkwithX":
        print(f"{Fore.RED}Invalid password. Exiting.{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Password verified successfully.{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}Select Mode:{Style.RESET_ALL}")
    print("1. Extension Mode")
    print("2. Desktop Mode")
    
    while True:
        mode_choice = input("Enter your choice (1/2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
    
    mode = "extension" if mode_choice == "1" else "desktop"
    print(f"{Fore.GREEN}Selected mode: {mode}{Style.RESET_ALL}")
    
    _user_id = input('Please Enter your user ID: ')
    
    with open('proxy.txt', 'r') as file:
        local_proxies = file.read().splitlines()
    
    print(f"{Fore.YELLOW}Total Proxies: {len(local_proxies)}{Style.RESET_ALL}")
    
    tasks = [asyncio.ensure_future(connect_to_wss(i, _user_id, mode)) for i in local_proxies]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
