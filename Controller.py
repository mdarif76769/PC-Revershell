#!/usr/bin/env python3
import socket
import os
import sys

# ANSI কালার কোড (টার্মিনাল সুন্দর করার জন্য)
C_BRIGHT = "\033[96m"
Y_BRIGHT = "\033[93m"
G_BRIGHT = "\033[92m"
R_BRIGHT = "\033[91m"
W_RESET  = "\033[0m"
def print_banner():
    if os.name == 'nt':
        os.system('color')
    banner = f"""{C_BRIGHT}
 ╦═╗╔═╗╦  ╦╔═╗╦═╗╔═╗╔═╗  ╔═╗╦ ╦╔═╗╦  ╦   github.com
 ╠╦╝║╣ ╚╗╔╝║╣ ╠╦╝╚═╗║╣   ╚═╗╠═╣║╣ ║  ║  
 ╩╚═╚═╝ ╚╝ ╚═╝╩╚═╚═╝╚═╝  ╚═╝╩ ╩╚═╝╩═╝╩═╝ mdarif76769
======================================================
        {Y_BRIGHT}[+] CENTRAL CONTROL & PEN-TEST PANEL [+]       {C_BRIGHT}
 -----------------------------------------------------  
        {G_BRIGHT}Authorized Educational/Lab Testing Only{C_BRIGHT}      
======================================================{W_RESET}"""
    print(banner)

def start_controller():
    print_banner()
    
    # ১. টার্গেট/লিসেনিং আইপি ইনপুট নেওয়া
    ip_input = input(f"{R_BRIGHT}[*] Enter Listening IP (e.g., 0.0.0.0 or 127.0.0.1): {W_RESET}").strip()
    if not ip_input:
        ip_input = "0.0.0.0"  # কিছু না দিলে ডিফল্ট সব ইন্টারফেস লিসেন করবে
    
    # ২. লিসেনিং পোর্ট ইনপুট নেওয়া
    try:
        port_input = input(f"{R_BRIGHT}[*] Enter Listening Port (e.g., 4444): {W_RESET}").strip()
        port = int(port_input)
    except ValueError:
        print(f"{R_BRIGHT}[-] Invalid Port. Defaulting to 4444.{W_RESET}")
        port = 4444

    # সকেট সার্ভার তৈরি করা
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((ip_input, port))
        server.listen(1)
        print(f"\n{Y_BRIGHT}[*] Controller is listening on {ip_input}:{port}...{W_RESET}")
        print(f"{Y_BRIGHT}[*] Awaiting connection from the agent...{W_RESET}\n")
        
        # এজেন্টের কানেকশন রিসিভ করা
        conn, addr = server.accept()
        print(f"{G_BRIGHT}[+] Success! Connected to Agent: {addr[0]}:{addr[1]}{W_RESET}\n")
        
        # প্রথম পাথ প্রম্পট রিসিভ করা
        initial_prompt = conn.recv(1024).decode('utf-8', errors='ignore')
        print(initial_prompt, end="")
        
        while True:
            command = input()
            
            # খালি ইনপুট হ্যান্ডল করা
            if not command.strip():
                conn.send(b"\n")
                response = conn.recv(4096).decode('utf-8', errors='ignore')
                print(response, end="")
                continue
                
            # এক্সিট লজিক
            if command.lower() == 'exit':
                conn.send(b'exit')
                break
                
            # কমান্ড পাঠানো এবং রেসপন্স প্রিন্ট করা
            conn.send(command.encode('utf-8'))
            response = conn.recv(4096).decode('utf-8', errors='ignore')
            print(response, end="")
            
    except Exception as e:
        print(f"\n{R_BRIGHT}[-] Error: {e}{W_RESET}")
    finally:
        server.close()

if __name__ == "__main__":
    start_controller()
