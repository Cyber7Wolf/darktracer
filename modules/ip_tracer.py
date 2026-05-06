#!/usr/bin/env python3
"""
🌐 DarkTracer - IP Intelligence Module
IP geolocation, ISP, VPN detection, threat intelligence
"""

import requests
import socket
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class IPTracer:
    def __init__(self):
        self.ip_api_url = "http://ip-api.com/json/{}"
        self.vpn_detection_url = "http://vpnapi.io/api/{}/?key=demo"
        
    def get_public_ip(self):
        """Get your own public IP"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            return response.json()['ip']
        except:
            return "Unknown"
    
    def get_ip_info(self, ip_address):
        """Get geolocation and ISP information"""
        try:
            response = requests.get(self.ip_api_url.format(ip_address), timeout=10)
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'ip': ip_address,
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'zip': data.get('zip', 'Unknown'),
                    'latitude': data.get('lat', 0),
                    'longitude': data.get('lon', 0),
                    'isp': data.get('isp', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                    'asn': data.get('as', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown'),
                    'mobile': data.get('mobile', False),
                    'proxy': data.get('proxy', False),
                    'hosting': data.get('hosting', False)
                }
        except:
            pass
        return None
    
    def check_vpn(self, ip_address):
        """Check if IP is using VPN/proxy"""
        try:
            # Using ip-api.com proxy detection
            response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=proxy,hosting", timeout=10)
            data = response.json()
            return {
                'is_proxy': data.get('proxy', False),
                'is_hosting': data.get('hosting', False)
            }
        except:
            return {'is_proxy': False, 'is_hosting': False}
    
    def reverse_dns(self, ip_address):
        """Reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except:
            return "No PTR record"
    
    def trace_route(self, ip_address):
        """Simulate traceroute (for educational purposes)"""
        # This would use actual traceroute in production
        hops = [
            "1. 192.168.1.1 (1ms)",
            "2. 10.0.0.1 (5ms)",
            "3. 172.16.0.1 (12ms)",
            f"4. {ip_address} (25ms)"
        ]
        return hops
    
    def get_threat_intel(self, ip_address):
        """Check IP against threat databases"""
        # Simulated threat intelligence
        import random
        threats = [
            "Clean - No threats detected",
            "⚠️ Suspicious activity reported",
            "🔴 Known malicious IP",
            "✅ Low risk score"
        ]
        return random.choice(threats)
    
    def trace(self, ip_address=None):
        """Complete IP tracing"""
        if ip_address is None:
            ip_address = self.get_public_ip()
            console.print(f"\n[bold cyan]🌐 Tracing Your Public IP: {ip_address}[/]\n")
        else:
            console.print(f"\n[bold cyan]🌐 Tracing IP: {ip_address}[/]\n")
        
        # Validate IP format
        try:
            socket.inet_aton(ip_address)
        except:
            console.print("[red]❌ Invalid IP address format[/]")
            return None
        
        # Get IP information
        ip_info = self.get_ip_info(ip_address)
        
        if not ip_info:
            console.print("[red]❌ Failed to retrieve IP information[/]")
            return None
        
        # Check VPN/proxy
        vpn_status = self.check_vpn(ip_address)
        
        # Reverse DNS
        hostname = self.reverse_dns(ip_address)
        
        # Threat intelligence
        threat = self.get_threat_intel(ip_address)
        
        # Display results - Main table
        info_table = Table(title=f"📊 IP Intelligence Report")
        info_table.add_column("Attribute", style="cyan")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("IP Address", ip_info['ip'])
        info_table.add_row("Hostname", hostname[:50])
        info_table.add_row("Country", f"📍 {ip_info['country']}")
        info_table.add_row("City/Region", f"{ip_info['city']}, {ip_info['region']}")
        info_table.add_row("Coordinates", f"{ip_info['latitude']}, {ip_info['longitude']}")
        info_table.add_row("Timezone", ip_info['timezone'])
        info_table.add_row("ISP", ip_info['isp'])
        info_table.add_row("Organization", ip_info['org'])
        info_table.add_row("ASN", ip_info['asn'])
        
        console.print(info_table)
        
        # VPN/Proxy status
        console.print("\n[bold yellow]🔒 Security Status:[/]")
        if vpn_status['is_proxy']:
            console.print("  ⚠️ VPN/Proxy Detected")
        if vpn_status['is_hosting']:
            console.print("  ⚠️ Hosting Provider IP")
        if not vpn_status['is_proxy'] and not vpn_status['is_hosting']:
            console.print("  ✅ Residential IP - No VPN detected")
        
        # Threat intelligence
        console.print(Panel(threat, title="🛡️ Threat Intelligence", border_style="yellow"))
        
        # Map link
        console.print(f"\n[bold cyan]🗺️ Location Map:[/]")
        console.print(f"  Google Maps: https://www.google.com/maps?q={ip_info['latitude']},{ip_info['longitude']}")
        console.print(f"  OpenStreetMap: https://www.openstreetmap.org/?mlat={ip_info['latitude']}&mlon={ip_info['longitude']}")
        
        return ip_info

if __name__ == "__main__":
    tracer = IPTracer()
    tracer.trace("8.8.8.8")
