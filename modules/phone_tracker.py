#!/usr/bin/env python3
"""
📞 DarkTracer - Advanced Phone Number Tracking
"""

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from modules.area_codes import AREA_CODES

console = Console()

class PhoneTracker:
    def get_basic_info(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed):
                return {
                    'valid': True,
                    'country': geocoder.description_for_number(parsed, "en"),
                    'carrier': carrier.name_for_number(parsed, "en"),
                    'timezone': list(timezone.time_zones_for_number(parsed))[0] if timezone.time_zones_for_number(parsed) else "Unknown",
                    'number_type': self.get_number_type(parsed),
                    'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                }
        except:
            pass
        return {'valid': False}
    
    def get_number_type(self, parsed):
        types = {
            0: "Fixed Line", 1: "Mobile", 2: "Fixed Line or Mobile",
            3: "Toll Free", 4: "Premium Rate", 5: "Shared Cost",
            6: "VoIP", 7: "Personal Number", 8: "Pager",
            9: "Universal Access", 10: "Voice Mail", 11: "Unknown"
        }
        return types.get(phonenumbers.number_type(parsed), "Unknown")
    
    def get_area_code_location(self, phone_number):
        match = re.search(r'\+1(\d{3})', phone_number)
        if match:
            area = match.group(1)
            if area in AREA_CODES:
                return AREA_CODES[area]
        return None
    
    def trace(self, phone_number):
        console.print(f"\n[bold cyan]📞 Advanced Phone Trace: {phone_number}[/]\n")
        
        basic = self.get_basic_info(phone_number)
        if not basic['valid']:
            console.print("[red]❌ Invalid phone number[/]")
            return None
        
        table = Table(title="Phone Intelligence Report")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Phone", basic.get('international', phone_number))
        table.add_row("Country", basic.get('country', 'Unknown'))
        table.add_row("Carrier", basic.get('carrier', 'Unknown'))
        table.add_row("Type", basic.get('number_type', 'Unknown'))
        table.add_row("Timezone", basic.get('timezone', 'Unknown'))
        console.print(table)
        
        location = self.get_area_code_location(phone_number)
        if location:
            console.print(f"\n[bold yellow]📍 Location: {location['city']}, {location['state']}[/]")
            map_url = f"https://www.google.com/maps?q={location['lat']},{location['lon']}"
            console.print(f"[bold cyan]🗺️ Google Maps: {map_url}[/]")
        else:
            console.print(f"\n[yellow]📍 Country: {basic.get('country', 'Unknown')}[/]")
        
        return basic

if __name__ == "__main__":
    tracker = PhoneTracker()
    tracker.trace("+14155552671")
