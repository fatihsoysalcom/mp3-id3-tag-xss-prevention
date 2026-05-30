# MP3 ID3 Tag XSS Prevention

This example demonstrates how Cross-Site Scripting (XSS) vulnerabilities can arise from displaying unsanitized ID3 metadata extracted from MP3 files in a web application. It simulates a malicious ID3 comment tag containing an XSS payload and shows both a vulnerable page that executes the script and a secure page that prevents it using proper HTML escaping.

## Language

`python`

## How to Run

1. Save the code as `main.py`.
2. Run `python main.py` in your terminal.
3. Open `http://localhost:8000/vulnerable` in your browser to see the XSS attack.
4. Open `http://localhost:8000/secure` to see the same data displayed securely.

## Original Article

This example accompanies the Turkish article: [MP3 Dosyaları ve Siber Güvenlik Riskleri: SQLi, XSS, CSRF Tehditleri Nasıl Önlenir?](https://fatihsoysal.com/blog/mp3-dosyalari-ve-siber-guvenlik-riskleri-sqli-xss-csrf-tehditleri-nasil-onlenir/).

## License

MIT — see [LICENSE](LICENSE).
