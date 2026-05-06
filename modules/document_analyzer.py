#!/usr/bin/env python3
"""
📄 DarkTracer - Document Metadata Intelligence
Extract hidden data from PDF, DOCX, XLSX files
"""

import os
import hashlib
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class DocumentAnalyzer:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.xlsx', '.pptx', '.txt']
    
    def analyze_pdf(self, filepath):
        """Extract metadata from PDF"""
        try:
            import PyPDF2
            
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                info = reader.metadata
                
                metadata = {
                    'Title': info.get('/Title', 'Unknown'),
                    'Author': info.get('/Author', 'Unknown'),
                    'Subject': info.get('/Subject', 'Unknown'),
                    'Creator': info.get('/Creator', 'Unknown'),
                    'Producer': info.get('/Producer', 'Unknown'),
                    'Pages': len(reader.pages),
                }
                return metadata
        except:
            return None
    
    def analyze_docx(self, filepath):
        """Extract metadata from DOCX"""
        try:
            import docx
            
            doc = docx.Document(filepath)
            core_props = doc.core_properties
            
            metadata = {
                'Author': core_props.author or 'Unknown',
                'Title': core_props.title or 'Unknown',
                'Subject': core_props.subject or 'Unknown',
                'Created': str(core_props.created) if core_props.created else 'Unknown',
                'Modified': str(core_props.modified) if core_props.modified else 'Unknown',
                'Last Modified By': core_props.last_modified_by or 'Unknown',
                'Paragraphs': len(doc.paragraphs),
            }
            return metadata
        except:
            return None
    
    def get_file_hash(self, filepath):
        """Calculate file hash for tracking"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def analyze(self, filepath):
        """Complete document analysis"""
        console.print(f"\n[bold cyan]📄 Analyzing Document: {filepath}[/]\n")
        
        if not os.path.exists(filepath):
            console.print("[red]❌ File not found[/]")
            return None
        
        # Basic file info
        file_size = os.path.getsize(filepath) / 1024
        file_hash = self.get_file_hash(filepath)
        
        basic_table = Table(title="File Information")
        basic_table.add_column("Property", style="cyan")
        basic_table.add_column("Value", style="white")
        
        basic_table.add_row("Filename", os.path.basename(filepath))
        basic_table.add_row("Size", f"{file_size:.2f} KB")
        basic_table.add_row("SHA256", file_hash[:32] + "...")
        
        console.print(basic_table)
        
        # Extract metadata based on file type
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.pdf':
            metadata = self.analyze_pdf(filepath)
        elif ext == '.docx':
            metadata = self.analyze_docx(filepath)
        else:
            metadata = None
            console.print("[yellow]⚠️ Advanced metadata extraction only for PDF/DOCX[/]")
        
        if metadata:
            meta_table = Table(title="Document Metadata")
            meta_table.add_column("Property", style="cyan")
            meta_table.add_column("Value", style="white")
            
            for key, value in metadata.items():
                meta_table.add_row(key, str(value)[:50])
            
            console.print(meta_table)
            
            # Privacy analysis
            if metadata.get('Author') and metadata['Author'] != 'Unknown':
                console.print(Panel(
                    f"⚠️ Document contains author information: {metadata['Author']}\n"
                    f"This could reveal the document creator's identity.",
                    title="🛡️ Privacy Note",
                    border_style="yellow"
                ))
        
        return metadata

if __name__ == "__main__":
    analyzer = DocumentAnalyzer()
    analyzer.analyze("document.pdf")
