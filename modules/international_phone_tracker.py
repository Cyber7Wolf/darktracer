#!/usr/bin/env python3
"""
🌍 DarkTracer - International Phone Number Intelligence
Supports 200+ countries worldwide
"""

import phonenumbers
from phonenumbers import carrier, geocoder, timezone, region_code_for_number
import pycountry
import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class InternationalPhoneTracker:
    
    # Country codes with their formats
    country_formats = {
        'US': {'name': 'United States', 'example': '+1 212-555-1234', 'carrier': True},
        'GB': {'name': 'United Kingdom', 'example': '+44 20 7946 0123', 'carrier': True},
        'IN': {'name': 'India', 'example': '+91 98765 43210', 'carrier': True},
        'DE': {'name': 'Germany', 'example': '+49 30 1234567', 'carrier': True},
        'FR': {'name': 'France', 'example': '+33 1 23 45 67 89', 'carrier': True},
        'JP': {'name': 'Japan', 'example': '+81 3 1234 5678', 'carrier': True},
        'CN': {'name': 'China', 'example': '+86 10 1234 5678', 'carrier': False},
        'BR': {'name': 'Brazil', 'example': '+55 11 91234 5678', 'carrier': True},
        'RU': {'name': 'Russia', 'example': '+7 495 123-45-67', 'carrier': True},
        'AU': {'name': 'Australia', 'example': '+61 2 1234 5678', 'carrier': True},
        'CA': {'name': 'Canada', 'example': '+1 416-555-1234', 'carrier': True},
        'MX': {'name': 'Mexico', 'example': '+52 55 1234 5678', 'carrier': True},
        'ES': {'name': 'Spain', 'example': '+34 91 123 45 67', 'carrier': True},
        'IT': {'name': 'Italy', 'example': '+39 06 1234 5678', 'carrier': True},
        'NL': {'name': 'Netherlands', 'example': '+31 20 123 4567', 'carrier': True},
        'SE': {'name': 'Sweden', 'example': '+46 8 123 4567', 'carrier': True},
        'NO': {'name': 'Norway', 'example': '+47 21 23 45 67', 'carrier': True},
        'DK': {'name': 'Denmark', 'example': '+45 32 12 34 56', 'carrier': True},
        'FI': {'name': 'Finland', 'example': '+358 9 123 4567', 'carrier': True},
        'BE': {'name': 'Belgium', 'example': '+32 2 123 45 67', 'carrier': True},
        'CH': {'name': 'Switzerland', 'example': '+41 44 123 45 67', 'carrier': True},
        'AT': {'name': 'Austria', 'example': '+43 1 234 5678', 'carrier': True},
        'PL': {'name': 'Poland', 'example': '+48 22 123 45 67', 'carrier': True},
        'CZ': {'name': 'Czech Republic', 'example': '+420 2 12 34 56', 'carrier': True},
        'PT': {'name': 'Portugal', 'example': '+351 21 123 4567', 'carrier': True},
        'GR': {'name': 'Greece', 'example': '+30 21 1234 5678', 'carrier': True},
        'IE': {'name': 'Ireland', 'example': '+353 1 234 5678', 'carrier': True},
        'TR': {'name': 'Turkey', 'example': '+90 212 123 45 67', 'carrier': True},
        'SA': {'name': 'Saudi Arabia', 'example': '+966 11 123 4567', 'carrier': True},
        'AE': {'name': 'UAE', 'example': '+971 4 123 4567', 'carrier': True},
        'IL': {'name': 'Israel', 'example': '+972 2 123 4567', 'carrier': True},
        'ZA': {'name': 'South Africa', 'example': '+27 11 123 4567', 'carrier': True},
        'NG': {'name': 'Nigeria', 'example': '+234 802 123 4567', 'carrier': True},
        'EG': {'name': 'Egypt', 'example': '+20 2 1234 5678', 'carrier': True},
        'PK': {'name': 'Pakistan', 'example': '+92 21 123 4567', 'carrier': True},
        'BD': {'name': 'Bangladesh', 'example': '+880 2 123 4567', 'carrier': True},
        'ID': {'name': 'Indonesia', 'example': '+62 21 123 4567', 'carrier': True},
        'MY': {'name': 'Malaysia', 'example': '+60 3 1234 5678', 'carrier': True},
        'SG': {'name': 'Singapore', 'example': '+65 6123 4567', 'carrier': True},
        'PH': {'name': 'Philippines', 'example': '+63 2 123 4567', 'carrier': True},
        'VN': {'name': 'Vietnam', 'example': '+84 24 1234 5678', 'carrier': True},
        'TH': {'name': 'Thailand', 'example': '+66 2 123 4567', 'carrier': True},
        'KR': {'name': 'South Korea', 'example': '+82 2 1234 5678', 'carrier': True},
        'NZ': {'name': 'New Zealand', 'example': '+64 4 123 4567', 'carrier': True},
        'AR': {'name': 'Argentina', 'example': '+54 11 1234 5678', 'carrier': True},
        'CL': {'name': 'Chile', 'example': '+56 2 1234 5678', 'carrier': True},
        'CO': {'name': 'Colombia', 'example': '+57 1 123 4567', 'carrier': True},
        'PE': {'name': 'Peru', 'example': '+51 1 123 4567', 'carrier': True},
        'VE': {'name': 'Venezuela', 'example': '+58 212 123 4567', 'carrier': True},
        'EG': {'name': 'Egypt', 'example': '+20 2 1234 5678', 'carrier': True},
        'MA': {'name': 'Morocco', 'example': '+212 5 12 34 56 78', 'carrier': True},
        'KE': {'name': 'Kenya', 'example': '+254 20 123 4567', 'carrier': True},
    }
    
    def get_country_info(self, number):
        """Extract country code and info"""
        for code, info in self.country_formats.items():
            region = phonenumbers.region_code_for_country_code(int(code))
            return {'code': code, 'info': info}
        return None
    
    def trace_international(self, phone_number):
        """Trace any international phone number"""
        console.print(f"\n[bold cyan]🌍 International Phone Trace: {phone_number}[/]\n")
        
        try:
            # Parse the number
            parsed = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed):
                console.print("[red]❌ Invalid phone number[/]")
                return None
            
            # Get country code
            country_code = f"+{parsed.country_code}"
            
            # Get region
            region = region_code_for_number(parsed)
            
            # Get country name
            country_name = geocoder.description_for_number(parsed, "en")
            
            # Get carrier (if available)
            carrier_name = carrier.name_for_number(parsed, "en")
            if not carrier_name:
                carrier_name = "Information not available for this region"
            
            # Get timezone
            tz = timezone.time_zones_for_number(parsed)
            timezone_str = list(tz)[0] if tz else "Unknown"
            
            # Get number type
            num_type = self.get_number_type(parsed)
            
            # Format numbers
            international_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            national_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            e164_format = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            # Display results
            table = Table(title=f"📊 International Phone Intelligence Report")
            table.add_column("Attribute", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Country", f"{country_name} ({country_code})")
            table.add_row("Region Code", region if region else "N/A")
            table.add_row("Carrier", carrier_name)
            table.add_row("Number Type", num_type)
            table.add_row("Timezone", timezone_str)
            table.add_row("International Format", international_format)
            table.add_row("National Format", national_format)
            table.add_row("E.164 Format", e164_format)
            
            console.print(table)
            
            # Area code info for US numbers only
            if country_code == "+1" and len(phone_number) >= 11:
                area_code = phone_number[2:5]
                if area_code.isdigit():
                    console.print(f"\n[bold yellow]📍 Area Code: {area_code} - {self.get_us_area_location(area_code)}[/]")
            
            # Google Maps link (country level)
            console.print(f"\n[bold cyan]🗺️ Country Map:[/]")
            console.print(f"  https://www.google.com/maps/search/{country_name.replace(' ', '+')}")
            
            # Additional info
            console.print(Panel(
                f"📡 This number is registered in {country_name}\n"
                f"📞 Carrier: {carrier_name}\n"
                f"📱 Type: {num_type}",
                title="🌍 Location Intelligence",
                border_style="cyan"
            ))
            
            return parsed
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            return None
    
    def get_number_type(self, parsed):
        """Get number type"""
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
        return types.get(phonenumbers.number_type(parsed), "Unknown")
    
    def get_us_area_location(self, area_code):
        """Get US area code location"""
        area_locations = {
            '212': 'New York, NY', '310': 'Los Angeles, CA', '312': 'Chicago, IL',
            '305': 'Miami, FL', '702': 'Las Vegas, NV', '404': 'Atlanta, GA',
            '206': 'Seattle, WA', '617': 'Boston, MA', '214': 'Dallas, TX',
            '713': 'Houston, TX', '215': 'Philadelphia, PA', '303': 'Denver, CO',
            '602': 'Phoenix, AZ', '619': 'San Diego, CA', '415': 'San Francisco, CA',
        }
        return area_locations.get(area_code, 'Unknown')

if __name__ == "__main__":
    tracker = InternationalPhoneTracker()
    
    # Test international numbers
    test_numbers = [
        "+14155552671",  # USA
        "+447911123456", # UK
        "+919876543210", # India
        "+49301234567",  # Germany
        "+81312345678",  # Japan
    ]
    
    for num in test_numbers:
        tracker.trace_international(num)
        print("\n" + "-"*50 + "\n")
