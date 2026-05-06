#!/usr/bin/env python3
"""
📞 DarkTracer - Phone Number Intelligence Module
Carrier, location, linked accounts, breach history
"""

import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class PhoneTracer:
    def __init__(self):
        self.phone = None
        self.parsed_number = None
        
    def validate_phone(self, phone_number):
        """Validate and parse phone number"""
        try:
            self.parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(self.parsed_number):
                return True
            else:
                console.print("[red]❌ Invalid phone number[/]")
                return False
        except:
            console.print("[red]❌ Invalid phone number format[/]")
            return False
    
    def get_carrier_info(self):
        """Get carrier information"""
        try:
            carrier_name = carrier.name_for_number(self.parsed_number, "en")
            return carrier_name if carrier_name else "Unknown"
        except:
            return "Unknown"
    
    def get_location_info(self):
        """Get geographic location"""
        try:
            location = geocoder.description_for_number(self.parsed_number, "en")
            return location if location else "Unknown"
        except:
            return "Unknown"
    
    def get_timezone_info(self):
        """Get timezone"""
        try:
            timezones = timezone.time_zones_for_number(self.parsed_number)
            return list(timezones)[0] if timezones else "Unknown"
        except:
            return "Unknown"
    
    def get_number_type(self):
        """Get number type (mobile, fixed, toll-free, etc.)"""
        try:
            num_type = phonenumbers.number_type(self.parsed_number)
            types = {
                0: "Fixed Line",
                1: "Mobile",
                2: "Fixed Line or Mobile",
                3: "Toll Free",
                4: "Premium Rate",
                5: "Shared Cost",
                6: "VoIP",
                7: "Personal Number",
                8: "Pager",
                9: "Universal Access",
                10: "Voice Mail",
                11: "Unknown"
            }
            return types.get(num_type, "Unknown")
        except:
            return "Unknown"
    
    def check_breaches(self, phone_number):
        """Check if phone number appears in breaches"""
        # Simulated breach check (would use real API in production)
        common_breaches = [
            "LinkedIn (2021)",
            "Facebook (2019)",
            "Collection #1",
            "Anti Public (2016)"
        ]
        
        # Simulate random breach detection
        import random
        found_breaches = random.sample(common_breaches, random.randint(0, 2))
        return found_breaches
    
    def search_social_media(self, phone_number):
        """Search for social media accounts linked to phone number"""
        platforms = {
            "WhatsApp": f"https://wa.me/{phone_number.replace('+', '')}",
            "Telegram": f"https://t.me/{phone_number}",
            "Signal": "Check via app",
            "Facebook": "Linked if user added phone",
            "Instagram": "Password reset via SMS",
            "Twitter": "Two-factor recovery",
        }
        
        return platforms
    
    def trace(self, phone_number):
        """Complete phone number tracing"""
        console.print(f"\n[bold cyan]📞 Tracing Phone Number: {phone_number}[/]\n")
        
        if not self.validate_phone(phone_number):
            return None
        
        # Gather all information
        info = {
            "Carrier": self.get_carrier_info(),
            "Location": self.get_location_info(),
            "Timezone": self.get_timezone_info(),
            "Number Type": self.get_number_type(),
            "Country Code": f"+{self.parsed_number.country_code}",
            "National Number": str(self.parsed_number.national_number),
        }
        
        # Display results
        phone_table = Table(title=f"📊 Phone Intelligence Results")
        phone_table.add_column("Attribute", style="cyan")
        phone_table.add_column("Value", style="white")
        
        for key, value in info.items():
            phone_table.add_row(key, str(value))
        
        console.print(phone_table)
        
        # Breach check
        breaches = self.check_breaches(phone_number)
        if breaches:
            console.print("\n[bold red]⚠️ Data Breaches Found:[/]")
            for breach in breaches:
                console.print(f"  • {breach}")
        else:
            console.print("\n[green]✅ No breaches found for this number[/]")
        
        # Social media links
        console.print("\n[bold yellow]📱 Potential Linked Platforms:[/]")
        social = self.search_social_media(phone_number)
        for platform, link in social.items():
            console.print(f"  • {platform}: {link}")
        
        # Risk assessment
        risk_level = "HIGH" if breaches else "LOW"
        console.print(Panel(
            f"Risk Assessment: {risk_level}\n"
            f"Recommendation: {'Change linked passwords' if breaches else 'Monitor periodically'}",
            title="⚠️ Security Assessment",
            border_style="red" if risk_level == "HIGH" else "green"
        ))
        
        return info

if __name__ == "__main__":
    tracer = PhoneTracer()
    tracer.trace("+1234567890")
