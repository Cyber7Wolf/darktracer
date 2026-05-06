#!/usr/bin/env python3
"""
🔗 DarkTracer - Social Media Intelligence Module
Trace usernames across platforms
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class SocialTracer:
    def __init__(self):
        self.platforms = {
            "Twitter": "https://twitter.com/{}",
            "Instagram": "https://instagram.com/{}/",
            "Facebook": "https://facebook.com/{}",
            "LinkedIn": "https://linkedin.com/in/{}",
            "GitHub": "https://github.com/{}",
            "Reddit": "https://reddit.com/user/{}",
            "TikTok": "https://tiktok.com/@{}",
            "YouTube": "https://youtube.com/@{}",
            "Pinterest": "https://pinterest.com/{}/",
            "Tumblr": "https://{}.tumblr.com",
            "Medium": "https://medium.com/@{}",
            "Twitch": "https://twitch.tv/{}",
            "Snapchat": "https://snapchat.com/add/{}",
            "Telegram": "https://t.me/{}",
            "Discord": "https://discord.com/users/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "GitLab": "https://gitlab.com/{}",
            "Bitbucket": "https://bitbucket.org/{}",
            "Keybase": "https://keybase.io/{}",
        }
    
    def check_profile(self, platform, url_template, username):
        """Check if profile exists"""
        url = url_template.format(username.replace(' ', ''))
        try:
            response = requests.get(url, timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            if response.status_code == 200:
                return {'platform': platform, 'url': url, 'status': 'found'}
        except:
            pass
        return None
    
    def trace(self, username):
        """Trace username across platforms"""
        console.print(f"\n[bold cyan]🔍 Tracing Username: {username}[/]\n")
        
        found_profiles = []
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("[yellow]Scanning platforms...", total=len(self.platforms))
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = []
                for platform, url_template in self.platforms.items():
                    future = executor.submit(self.check_profile, platform, url_template, username)
                    futures.append(future)
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        found_profiles.append(result)
                    progress.update(task, advance=1)
        
        if found_profiles:
            table = Table(title=f"📊 Profiles Found for: {username}")
            table.add_column("Platform", style="cyan")
            table.add_column("URL", style="green")
            
            for result in found_profiles:
                table.add_row(result['platform'], result['url'])
            
            console.print(table)
            console.print(f"\n[green]✅ Found on {len(found_profiles)} platforms[/]")
        else:
            console.print("[red]❌ No profiles found[/]")
        
        return found_profiles

if __name__ == "__main__":
    tracer = SocialTracer()
    tracer.trace("johndoe")
