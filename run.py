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

# Function to create gradient text
def gradient_text(text, colors):
    gradient = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        gradient += f"\033[38;2;{color[0]};{color[1]};{color[2]}m{char}"
    return gradient + Style.RESET_ALL

# Gradient banner with colors
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
GRADIENT_COLORS = [
    (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0),
    (0, 0, 255), (75, 0, 130), (238, 130, 238)
]
BANNER = gradient_text(BANNER_TEXT, GRADIENT_COLORS)

EDGE_USERAGENTS = [
    # Add user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.57",
]

HTTP_STATUS_CODES = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
}

def colorful_log(proxy, device_id, message_type, message_content, is_sent=False, mode=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = Fore.GREEN if is_sent else Fore.BLUE
    log_message = (
        f"{Fore.WHITE}[{timestamp}] "
        f"{Fore.MAGENTA}[Proxy: {proxy}] "
        f"{Fore.CYAN}[Device ID: {device_id}] "
        f"{Fore.YELLOW}[{message_type}] "
        f"{color}{message_content} "
        f"{Fore.LIGHTYELLOW_EX}[{mode}]"
    )
    print(log_message)

async def connect_to_wss(socks5_proxy, user_id, mode):
    device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, socks5_proxy))
    random_user_agent = random.choice(EDGE_USERAGENTS)

    colorful_log(proxy=socks5_proxy, device_id=device_id, message_type="INITIALIZATION",
                 message_content=f"User Agent: {random_user_agent}", mode=mode)

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    uri = random.choice(["wss://proxy2.wynd.network:4444/", "wss://proxy2.wynd.network:4650/"])
    proxy = Proxy.from_url(socks5_proxy)

    try:
        async with proxy_connect(uri, proxy=proxy, ssl=ssl_context) as websocket:
            # Connection logic
            async def send_ping():
                while True:
                    await websocket.send(json.dumps({"action": "PING"}))
                    await asyncio.sleep(5)
            asyncio.create_task(send_ping())
            
            while True:
                response = await websocket.recv()
                message = json.loads(response)
                colorful_log(proxy, device_id, "RECEIVED", json.dumps(message), mode=mode)
                # Handle different message actions (AUTH, HTTP_REQUEST, etc.)
                
    except Exception as e:
        colorful_log(proxy, device_id, "ERROR", str(e), mode=mode)

async def main():
    print(BANNER)
    password = input(f"{Fore.YELLOW}Enter password to proceed: {Style.RESET_ALL}").strip()
    if password != "darkwithX":
        print(f"{Fore.RED}Invalid password. Exiting...{Style.RESET_ALL}")
        return

    mode_choice = input("Select Mode (1: Extension, 2: Desktop): ").strip()
    mode = "extension" if mode_choice == "1" else "desktop"
    user_id = input("Enter User ID: ")

    with open('proxy.txt', 'r') as file:
        local_proxies = file.read().splitlines()

    tasks = [connect_to_wss(proxy, user_id, mode) for proxy in local_proxies]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
