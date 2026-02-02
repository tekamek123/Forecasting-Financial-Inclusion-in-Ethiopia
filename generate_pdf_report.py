#!/usr/bin/env python3
"""
Generate PDF version of the Interim Report
"""

import os
import sys
from pathlib import Path

def install_requirements():
    """Install required packages for PDF generation"""
    try:
        import markdown
        import weasyprint
        print("✅ Required packages already installed")
        return True
    except ImportError:
        print("📦 Installing required packages...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "weasyprint"])
            print("✅ Packages installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install packages: {e}")
            return False

def generate_pdf():
    """Generate PDF from markdown report"""
    
    # Check if requirements are available
    if not install_requirements():
        print("❌ Cannot generate PDF without required packages")
        return False
    
    try:
        import markdown
        from weasyprint import HTML, CSS
        
        # Read markdown file
        md_file = Path("reports/interim_report.md")
        if not md_file.exists():
            print(f"❌ Markdown file not found: {md_file}")
            return False
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
        
        # Add CSS styling for better PDF appearance
        css_style = """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2E86AB;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        
        h1 {
            border-bottom: 3px solid #2E86AB;
            padding-bottom: 10px;
        }
        
        h2 {
            border-bottom: 2px solid #A23B72;
            padding-bottom: 8px;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        blockquote {
            border-left: 4px solid #F18F01;
            margin: 20px 0;
            padding-left: 20px;
            font-style: italic;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        @page {
            margin: 2cm;
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
            }
        }
        """
        
        # Create complete HTML document
        html_doc = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Ethiopia Financial Inclusion Interim Report</title>
            <style>{css_style}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        output_file = Path("reports/interim_report.pdf")
        HTML(string=html_doc).write_pdf(output_file)
        
        print(f"✅ PDF generated successfully: {output_file.absolute()}")
        print(f"📄 File size: {output_file.stat().st_size / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def create_simple_html_version():
    """Create a simple HTML version as fallback"""
    try:
        import markdown
        
        # Read markdown file
        md_file = Path("reports/interim_report.md")
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'toc'])
        
        # Create simple HTML
        html_doc = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Ethiopia Financial Inclusion Interim Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1, h2, h3 {{ color: #2E86AB; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Save HTML file
        html_file = Path("reports/interim_report.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        
        print(f"✅ HTML version created: {html_file.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating HTML version: {e}")
        return False

def main():
    """Main function"""
    print("🇪🇹 Ethiopia Financial Inclusion - Interim Report Generation")
    print("="*60)
    
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Try to generate PDF
    if generate_pdf():
        print("\n🎉 PDF report generated successfully!")
        print("📁 Location: reports/interim_report.pdf")
    else:
        print("\n⚠️ PDF generation failed, creating HTML version instead...")
        if create_simple_html_version():
            print("📄 HTML report created: reports/interim_report.html")
            print("💡 You can convert HTML to PDF using your browser or online tools")
        else:
            print("❌ Failed to generate any report format")
    
    print("\n📋 Report Contents:")
    print("   • Data enrichment summary")
    print("   • 5 key insights with supporting evidence")
    print("   • Event-indicator relationship analysis")
    print("   • Data limitations and recommendations")
    print("   • Methodology and quality assurance")

if __name__ == "__main__":
    main()
