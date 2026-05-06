#!/usr/bin/env python3
"""
🧠 DarkTracer - AI-Powered Intelligence Analysis
"""

import subprocess
import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class AIAnalyzer:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
        self.check_ollama()
    
    def check_ollama(self):
        """Check if Ollama is available"""
        try:
            result = subprocess.run(['which', 'ollama'], capture_output=True)
            if result.returncode == 0:
                console.log("[green]✓ Ollama available for AI analysis[/]")
                return True
            else:
                console.log("[yellow]⚠️ Ollama not installed. AI features limited.[/]")
                return False
        except:
            return False
    
    def analyze_phone(self, phone_data):
        """AI analysis of phone number intelligence"""
        prompt = f"""Analyze this phone number intelligence:

Carrier: {phone_data.get('Carrier', 'Unknown')}
Location: {phone_data.get('Location', 'Unknown')}
Number Type: {phone_data.get('Number Type', 'Unknown')}
Breaches: {phone_data.get('breaches', [])}

Provide:
1. Risk assessment of this phone number
2. What this number reveals about the person
3. Privacy recommendations

Keep it concise and educational."""
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip()
        except:
            return "AI analysis unavailable. Install Ollama for insights."
    
    def analyze_social(self, username, found_profiles):
        """AI analysis of social media footprint"""
        platforms = [p['platform'] for p in found_profiles[:10]]
        prompt = f"""Analyze this social media footprint for username '{username}':

Found on: {', '.join(platforms)}
Total platforms: {len(found_profiles)}

Provide:
1. Persona assessment (what platforms suggest about the person)
2. Privacy exposure level (LOW/MEDIUM/HIGH)
3. Recommendations for reducing digital footprint"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip()
        except:
            return "AI analysis unavailable."
    
    def analyze_ip(self, ip_info):
        """AI analysis of IP intelligence"""
        prompt = f"""Analyze this IP address intelligence:

IP: {ip_info.get('ip', 'Unknown')}
Location: {ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')}
ISP: {ip_info.get('isp', 'Unknown')}
VPN/Proxy: {'Yes' if ip_info.get('proxy') else 'No'}

Provide:
1. What this IP reveals about the user
2. Privacy implications
3. Recommendations"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip()
        except:
            return "AI analysis unavailable."
    
    def correlate_intel(self, all_data):
        """Correlate all intelligence sources"""
        prompt = f"""Correlate this intelligence data:

Phone Data: {json.dumps(all_data.get('phone', {}), indent=2)[:500]}
IP Data: {json.dumps(all_data.get('ip', {}), indent=2)[:500]}
Social Data: {len(all_data.get('social', []))} platforms found

Provide:
1. Comprehensive threat assessment
2. Linkages between different data points
3. Actionable intelligence summary"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True, text=True, timeout=45
            )
            return result.stdout.strip()
        except:
            return "AI correlation unavailable."

if __name__ == "__main__":
    ai = AIAnalyzer()
    result = ai.analyze_phone({"Carrier": "Verizon", "Location": "New York"})
    print(result)
