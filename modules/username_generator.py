#!/usr/bin/env python3
"""
🔗 DarkTracer - Username Generator & Availability Checker
Generate possible usernames from real names and check availability
"""

import requests
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table

console = Console()

class UsernameGenerator:
    def __init__(self):
        self.platforms = {
            'GitHub': 'https://github.com/{}',
            'Twitter': 'https://twitter.com/{}',
            'Instagram': 'https://instagram.com/{}/',
            'Reddit': 'https://reddit.com/user/{}',
        }
    
    def generate_from_name(self, first_name, last_name):
        """Generate possible usernames from real name"""
        first = first_name.lower()
        last = last_name.lower()
        
        usernames = [
            f"{first}{last}",
            f"{first}.{last}",
            f"{first}_{last}",
            f"{first}-{last}",
            f"{first}{last[0]}",
            f"{first[0]}{last}",
            f"{first}{last}{random.randint(1,99)}",
            f"{first}{last}_{random.randint(1,9)}",
        ]
        return usernames
    
    def check_availability(self, username):
        """Check if username is available on platforms"""
        results = []
        for platform, url in self.platforms.items():
            try:
                response = requests.get(url.format(username), timeout=3)
                if response.status_code == 200:
                    results.append({'platform': platform, 'status': 'TAKEN', 'url': url.format(username)})
                else:
                    results.append({'platform': platform, 'status': 'AVAILABLE', 'url': None})
            except:
                results.append({'platform': platform, 'status': 'ERROR', 'url': None})
        return results
