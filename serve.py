#!/usr/bin/env python3
"""
Simple static file server for CCHits.net Archive
Just serves HTML files with proper MIME types for local development
"""

import http.server
import socketserver
import os
from pathlib import Path

class SimpleStaticHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Ensure proper MIME types
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def translate_path(self, path):
        """Translate URL paths to handle extensionless URLs"""
        # Get the default translation
        translated_path = super().translate_path(path)
        path_obj = Path(translated_path)
        
        # If path doesn't exist but there's a directory with index.html, serve that
        if not path_obj.exists() and not path.endswith('/'):
            # Try path/index.html
            index_path = path_obj / 'index.html'
            if index_path.exists():
                return str(index_path)
        
        # If path ends with / and directory exists, serve index.html
        if path.endswith('/') and path_obj.is_dir():
            index_path = path_obj / 'index.html'
            if index_path.exists():
                return str(index_path)
        
        return translated_path

def main():
    """Start a simple static file server"""
    PORT = int(os.environ.get('PORT', 5224))
    
    # Change to the target directory (where static files are)
    target_dir = Path(__file__).parent
    os.chdir(target_dir)
    
    with socketserver.TCPServer(("", PORT), SimpleStaticHandler) as httpd:
        print(f"🎵 CCHits.net Archive - Static Server")
        print(f"📁 Serving from: {target_dir}")
        print(f"🌐 http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    main()