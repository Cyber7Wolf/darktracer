#!/usr/bin/env python3
"""
🌐 DarkTracer - Domain WHOIS History Intelligence
Track domain ownership, registration changes, and DNS history
"""

import whois
import dns.resolver
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree

console = Console()

class DomainHistory:
    def __init__(self):
        self.history_api = "https://api.securitytrails.com/v1/history/"
    
    def get_whois_info(self, domain):
        """Get current WHOIS information"""
        try:
            domain_info = whois.whois(domain)
            
            info = {
                'Domain': domain,
                'Registrar': domain_info.registrar or 'Unknown',
                'Creation Date': str(domain_info.creation_date[0]) if isinstance(domain_info.creation_date, list) else str(domain_info.creation_date),
                'Expiration Date': str(domain_info.expiration_date[0]) if isinstance(domain_info.expiration_date, list) else str(domain_info.expiration_date),
                'Name Servers': ', '.join(domain_info.name_servers[:3]) if domain_info.name_servers else 'Unknown',
                'Status': ', '.join(domain_info.status[:3]) if domain_info.status else 'Unknown',
            }
            return info
        except Exception as e:
            return None
    
    def get_dns_records(self, domain):
        """Get DNS records"""
        records = {}
        record_types = ['A', 'MX', 'TXT', 'NS', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(r) for r in answers[:3]]
            except:
                records[record_type] = []
        
        return records
    
    def get_subdomains(self, domain):
        """Find subdomains (simulated)"""
        common_subdomains = ['www', 'mail', 'admin', 'dev', 'api', 'blog', 'shop']
        found = []
        
        for sub in common_subdomains:
            full = f"{sub}.{domain}"
            try:
                dns.resolver.resolve(full, 'A')
                found.append(full)
            except:
                pass
        
        return found
    
    def track_changes(self, domain):
        """Track domain changes over time"""
        console.print(f"\n[bold cyan]🌐 Domain Intelligence: {domain}[/]\n")
        
        # Current WHOIS
        whois_info = self.get_whois_info(domain)
        
        if whois_info:
            whois_table = Table(title="WHOIS Information")
            whois_table.add_column("Attribute", style="cyan")
            whois_table.add_column("Value", style="white")
            
            for key, value in whois_info.items():
                whois_table.add_row(key, str(value)[:60])
            
            console.print(whois_table)
        
        # DNS Records
        dns_records = self.get_dns_records(domain)
        if any(dns_records.values()):
            dns_table = Table(title="DNS Records")
            dns_table.add_column("Record Type", style="cyan")
            dns_table.add_column("Values", style="white")
            
            for record_type, values in dns_records.items():
                if values:
                    dns_table.add_row(record_type, '\n'.join(values))
            
            console.print(dns_table)
        
        # Subdomains
        subdomains = self.get_subdomains(domain)
        if subdomains:
            console.print("\n[bold yellow]🔗 Discovered Subdomains:[/]")
            for sub in subdomains:
                console.print(f"  • {sub}")
        
        # Risk assessment
        console.print(Panel(
            f"Domain: {domain}\n"
            f"Registrar: {whois_info.get('Registrar', 'Unknown') if whois_info else 'Unknown'}\n"
            f"Subdomains Found: {len(subdomains)}\n\n"
            f"📌 Monitor this domain for changes regularly.",
            title="📊 Domain Intelligence Summary",
            border_style="cyan"
        ))
        
        return whois_info

if __name__ == "__main__":
    tracker = DomainHistory()
    tracker.track_changes("example.com")
