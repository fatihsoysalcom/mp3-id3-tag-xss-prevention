import http.server
import socketserver
import html

PORT = 8000

# Simulate extracted ID3 tags, one of which contains a malicious XSS payload.
# In a real scenario, this data would come from parsing an uploaded MP3 file's ID3 tags.
malicious_id3_metadata = {
    "title": "My Awesome Song",
    "artist": "Evil Hacker",
    "album": "Malicious Album",
    "comment": "<script>alert('XSS Vulnerability Detected from MP3 ID3 Tag!');</script>This comment looks innocent."
}

# HTML template for the vulnerable page
# The 'comment' field is directly inserted without sanitization, leading to XSS.
VULNERABLE_HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MP3 ID3 XSS Demo (Vulnerable)</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        h1 {{ color: #d9534f; }}
        pre {{ background-color: #eee; padding: 1em; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Vulnerable MP3 ID3 Tag Display</h1>
    <p>This page demonstrates an XSS vulnerability when displaying unsanitized ID3 tags from an MP3 file.</p>
    <p>Visit <a href="/secure">/secure</a> for the safe version.</p>
    <h2>Song Details:</h2>
    <ul>
        <li><strong>Title:</strong> {malicious_id3_metadata['title']}</li>
        <li><strong>Artist:</strong> {malicious_id3_metadata['artist']}</li>
        <li><strong>Album:</strong> {malicious_id3_metadata['album']}</li>
        <li><strong>Comment:</strong> <!-- Vulnerable point: Direct insertion of user-controlled data -->
            {malicious_id3_metadata['comment']}
        </li>
    </ul>
    <p>The alert box indicates successful XSS execution.</p>
</body>
</html>
"""

# HTML template for the secure page
# The 'comment' field is HTML-escaped before insertion, preventing XSS.
SECURE_HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MP3 ID3 XSS Demo (Secure)</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        h1 {{ color: #5cb85c; }}
        pre {{ background-color: #eee; padding: 1em; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Secure MP3 ID3 Tag Display</h1>
    <p>This page demonstrates how to prevent XSS by properly sanitizing (HTML escaping) ID3 tags from an MP3 file.</p>
    <p>Visit <a href="/vulnerable">/vulnerable</a> for the unsafe version.</p>
    <h2>Song Details:</h2>
    <ul>
        <li><strong>Title:</strong> {html.escape(malicious_id3_metadata['title'])}</li>
        <li><strong>Artist:</strong> {html.escape(malicious_id3_metadata['artist'])}</li>
        <li><strong>Album:</strong> {html.escape(malicious_id3_metadata['album'])}</li>
        <li><strong>Comment:</strong> <!-- Secure point: Using html.escape() to prevent XSS -->
            {html.escape(malicious_id3_metadata['comment'])}
        </li>
    </ul>
    <p>Notice the script tag is displayed as text, not executed.</p>
</body>
</html>
"""

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/vulnerable':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(VULNERABLE_HTML_TEMPLATE.encode("utf-8"))
        elif self.path == '/secure':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(SECURE_HTML_TEMPLATE.encode("utf-8"))
        else:
            # Redirect root to vulnerable page for easier access
            self.send_response(302)
            self.send_header("Location", "/vulnerable")
            self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(('', PORT), MyHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Vulnerable page: http://localhost:{PORT}/vulnerable")
        print(f"Secure page: http://localhost:{PORT}/secure")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()
