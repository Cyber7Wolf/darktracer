#!/usr/bin/env python3
"""
🔔 DarkTracer - Real-time Breach Monitoring System
Monitor email/phone for data breaches and dark web exposure
"""

import requests
import hashlib
import json
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

console = Console()

class BreachMonitor:
    def __init__(self):
        self.breach_api = "https://haveibeenpwned.com/api/v3/breachedaccount/"
        self.monitoring_active = False
        self.monitored_emails = []
    
    def check_breaches(self, email):
        """Check email against known breaches"""
        console.print(f"\n[bold cyan]🔍 Checking breaches for: {email}[/]\n")
        
        try:
            response = requests.get(
                f"{self.breach_api}{email}",
                headers={'User-Agent': 'DarkTracer-OSINT'}
            )
            
            if response.status_code == 200:
                breaches = response.json()
                
                if breaches:
                    table = Table(title=f"⚠️ Data Breaches Found for {email}")
                    table.add_column("Breach Name", style="red")
                    table.add_column("Date", style="yellow")
                    table.add_column("Data Types", style="white")
                    
                    for breach in breaches[:10]:
                        table.add_row(
                            breach.get('Name', 'Unknown'),
                            breach.get('BreachDate', 'Unknown'),
                            ', '.join(breach.get('DataClasses', [])[:3])
                        )
                    
                    console.print(table)
                    
                    # Risk assessment
                    risk_score = len(breaches) * 10
                    risk_level = "HIGH" if risk_score > 50 else "MEDIUM" if risk_score > 20 else "LOW"
                    
                    console.print(Panel(
                        f"Risk Score: {risk_score}/100\n"
                        f"Risk Level: {risk_level}\n"
                        f"Breaches Found: {len(breaches)}\n\n"
                        f"⚠️ Action Required: Change passwords immediately!",
                        title="🔴 Security Alert",
                        border_style="red"
                    ))
                    
                    return breaches
                else:
                    console.print("[green]✅ No breaches found for this email[/]")
                    return []
            
            elif response.status_code == 404:
                console.print("[green]✅ No breaches found for this email[/]")
                return []
            else:
                console.print("[yellow]⚠️ Rate limited. Please try again later.[/]")
                return []
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            return []
    
    def monitor_continuously(self, email, interval=3600):
        """Continuously monitor for new breaches"""
        console.print(f"\n[bold yellow]🔔 Starting continuous monitoring for: {email}[/]")
        console.print(f"Checking every {interval} seconds. Press Ctrl+C to stop.\n")
        
        self.monitored_emails.append(email)
        self.monitoring_active = True
        
        try:
            while self.monitoring_active:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                console.print(f"[dim]{timestamp} - Checking {email}...[/]")
                
                breaches = self.check_breaches(email)
                
                if breaches:
                    console.print(f"[red]🚨 NEW BREACH DETECTED for {email}![/]")
                    # Could send notification here
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Monitoring stopped[/]")
            self.monitoring_active = False
    
    def batch_check(self, email_file):
        """Check multiple emails from file"""
        console.print(f"\n[bold cyan]📋 Batch checking emails from: {email_file}[/]\n")
        
        try:
            with open(email_file, 'r') as f:
                emails = [line.strip() for line in f if line.strip()]
            
            results = []
            for email in emails:
                breaches = self.check_breaches(email)
                results.append({'email': email, 'breaches': len(breaches)})
                time.sleep(1.5)  # Rate limiting
            
            # Summary table
            summary_table = Table(title="Batch Breach Check Summary")
            summary_table.add_column("Email", style="cyan")
            summary_table.add_column("Breaches Found", style="red")
            summary_table.add_column("Status", style="white")
            
            for result in results:
                status = "⚠️ COMPROMISED" if result['breaches'] > 0 else "✅ SECURE"
                summary_table.add_row(result['email'], str(result['breaches']), status)
            
            console.print(summary_table)
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

if __name__ == "__main__":
    monitor = BreachMonitor()
    monitor.check_breaches("test@example.com")
