***

**Create: `scripts/generate_workflow_pdf.py`**
```python
#!/usr/bin/env python3
"""
BingeBear Visual Schema Generator
Extracts Mermaid flowcharts from Claude's markdown and generates a high-res HTML/PDF visual map.
"""
import sys
import re
import os

def generate_visual_map(md_file):
    try:
        with open(md_file, 'r') as f:
            content = f.read()
            
        # Extract Mermaid code block
        match = re.search(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
        if not match:
            print("❌ No visual schema (Mermaid code) found in the markdown file.")
            return
            
        mermaid_code = match.group(1)
        
        # Create an HTML file that renders the beautiful visual map
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>BingeBear GHL Schema</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #F5F7FA; padding: 40px; text-align: center; }}
                .schema-container {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: inline-block; text-align: left; min-width: 80%; }}
                h1 {{ color: #1B2A4A; }}
                .print-btn {{ background: #2D5BFF; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; margin-bottom: 20px; font-weight: bold; }}
                .print-btn:hover {{ background: #1B2A4A; }}
                @media print {{ .print-btn {{ display: none; }} body {{ background: white; padding: 0; }} .schema-container {{ box-shadow: none; width: 100%; }} }}
            </style>
        </head>
        <body>
            <button class="print-btn" onclick="window.print()">🖨️ Save as PDF</button>
            <div class="schema-container">
                <h1>⚙️ BingeBear Workflow Schema</h1>
                <div class="mermaid">
                    {mermaid_code}
                </div>
            </div>
            <script>mermaid.initialize({{startOnLoad:true, theme: 'default'}});</script>
        </body>
        </html>
        """
        
        output_file = md_file.replace('.md', '_SCHEMA.html')
        with open(output_file, 'w') as f:
            f.write(html_content)
            
        print(f"✅ SUCCESS! Visual Schema generated: {output_file}")
        print(f"👉 Open {output_file} in your web browser, then click 'Save as PDF'!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate_workflow_pdf.py <markdown_file>")
    else:
        generate_visual_map(sys.argv[1])
