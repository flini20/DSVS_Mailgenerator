import webbrowser
import textwrap
import base64
import requests
import re

class EmailSignatureGenerator:
    def __init__(self):
        self.position_lookup = {
            "Präsident": {"de": "Präsident", "en": "President", "hu": "DSVS Elnöke", "email": "vorsitz@dsvs-semmelweis.de"},
            "Vize Präsident": {"de": "Vize Präsident", "en": "General Vice President", "hu": "DSVS Általános Elnöke", "email": "vorsitz@dsvs-semmelweis.de"},
            "Generalsekretär": {"de": "Generalsekretär", "en": "General Secretary", "hu": "DSVS Főtitkára", "email": "office@dsvs-semmelweis.de"},
            "Leitung Studienangelegenheiten": {"de": "Leitung Studienangelegenheiten", "en": "Head Academic Affairs", "hu": "Tanulmányi Vezető", "email": "akademik@dsvs-semmelweis.de"},
            "Stv. Leitung Studienangelegenheiten": {"de": "Stv. Leitung Studienangelegenheiten", "en": "Deputy Head Academic Affairs", "hu": "Tanulmányi Vezető Helyettes", "email": "akademik@dsvs-semmelweis.de"},
            "Leitung Events": {"de": "Leitung Events", "en": "Head Events", "hu": "Rendezvényszervezési Vezető", "email": "events@dsvs-semmelweis.de"},
            "Stv. Leitung Events": {"de": "Stv. Leitung Events", "en": "Deputy Head Events", "hu": "Rendezvényszervezési Vezető Helyettes", "email": "events@dsvs-semmelweis.de"},
            "Leitung Multimedia": {"de": "Leitung Multimedia", "en": "Head Multimedia", "hu": "Multimedia Vezető", "email": "multimedia@dsvs-semmelweis.de"},
            "Stv. Leitung Multimedia": {"de": "Stv. Leitung Multimedia", "en": "Deputy Head Multimedia", "hu": "Multimedia Vezető Helyettes", "email": "multimedia@dsvs-semmelweis.de"},
            "Leitung IT": {"de": "Leitung IT", "en": "Head IT", "hu": "IT Vezető", "email": "it@dsvs-semmelweis.de"},
            "Stv. Leitung IT": {"de": "Stv. Leitung IT", "en": "Deputy Head IT", "hu": "IT Vezető Helyettes", "email": "it@dsvs-semmelweis.de"},
            "Leitung Finanzen": {"de": "Leitung Finanzen", "en": "Head Finance", "hu": "Pénzügyi Vezető", "email": "finanzen@dsvs-semmelweis.de"},
            "Stv. Leitung Finanzen": {"de": "Stv. Leitung Finanzen", "en": "Deputy Head Finance", "hu": "Pénzügyi Vezető Helyettes", "email": "finanzen@dsvs-semmelweis.de"},
            "Vertretung Zahnmedizin": {"de": "Vertretung Zahnmedizin", "en": "Representative Dentistry", "hu": "Fogászat Kari Képviselő", "email": "zahnmedizin@dsvs-semmelweis.de"},
            "Vertretung Pharmazie": {"de": "Vertretung Pharmazie", "en": "Representative Pharmacy", "hu": "Gyógyszerészet Kari Képviselő", "email": "pharmazie@dsvs-semmelweis.de"},
        }
    
    def get_base64_image_from_url(self, url):
        """Downloads an image from a URL and converts it to Base64."""
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode("utf-8")
        else:
            raise Exception(f"Bild konnte nicht von der URL geladen werden: {url}")
    
    def check_position(self, position):
        if position not in self.position_lookup:
            raise ValueError("Non existing position!")
    
    def sanitize_phone_number(self, phone_number, allow_plus=False):
        """Sanitizes the phone number by removing all non-digit characters."""
        if allow_plus:
            return re.sub(r"[^\d+]", "", phone_number)
        return re.sub(r"[^\d]", "", phone_number)
    
    def get_phone_number(self):
        """
        Handles the input for the phone number in three parts:
        - International prefix
        - Provider prefix
        - Phone number
        """
        create_phone = input("Soll eine Telefonnummer erstellt werden? (y/n): ").strip().lower()
        if create_phone == "n":
            return None  # Skip phone number input

        if create_phone == "y":
            # Input for international prefix
            international_prefix = input("Internationale Vorwahl (z. B. +36): ").strip()
            international_prefix = self.sanitize_phone_number(international_prefix, allow_plus=True)

            # Input for provider prefix
            provider_prefix = input("Anbieter-Vorwahl (z. B. 30): ").strip()
            provider_prefix = self.sanitize_phone_number(provider_prefix)
            # Remove leading zeros from provider prefix
            provider_prefix = provider_prefix.lstrip("0")

            # Input for the rest of the phone number
            phone_number = input("Telefonnummer (z. B. 1234567): ").strip()
            phone_number = self.sanitize_phone_number(phone_number)

            # Combine all parts into a single formatted phone number
            return f"{international_prefix} {provider_prefix} {phone_number}"

        # If input is invalid, return None
        print("Ungültige Eingabe. Telefonnummer wird übersprungen.")
        return None
    
    def generate_email_signature(self, first_name, last_name, position, phone_number):      
        translations = self.position_lookup[position]
        
        uni_translations = {"de": "Semmelweis Universität", "en": "Semmelweis University", "hu": "Semmelweis Egyetem"}
        student_union_translations = {"de": "Deutschsprachige Studentenvertretung", "en": "German Speaking Student Union", "hu": "Német Nyelvű Hallgatói Képviselet"}
        address_suffix = {"de": ", HUNGARY", "en": ", HUNGARY", "hu": ""}
        
        names = {
            "de": f"{first_name} {last_name}",
            "en": f"{first_name} {last_name}",
            "hu": f"{last_name} {first_name}"
        }
        
        # Base64-encoded image from URL
        base64_image = self.get_base64_image_from_url("https://semmelweis.hu/img/kekcimer_180.png")
        image_tag = f'<img src="data:image/png;base64,{base64_image}" name="logo" id="logo" width="120" height="120">'

        
        signatures = {}
        for lang in ["de", "en", "hu"]:
            phone_html = f'<div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: \'Trebuchet MS\';">{phone_number}</div>' if phone_number else ""
            
            # Dynamische zweite E-Mail-Adresse aus position_lookup
            second_email = self.position_lookup[position]["email"]
            
            signatures[lang] = textwrap.dedent(f"""
            <div id="signature-{lang}" style="margin-top:20px;text-indent: initial;">
                <table id="alairasKeret">
                    <tbody><tr>
                        <td id="bal" style="padding-right: 20px;border-right: 3px solid #b3a16e;">
                            {image_tag}
                        </td> 
                        <td id="adatokKeret" style="padding-left:30px;">
                            <b style="font-size: 16pt; text-transform: uppercase; color: rgb(35, 47, 97); font-family: 'Trebuchet MS';">{names[lang]}</b>
                            <div style="font-size: 10.5pt; text-transform: uppercase; color: rgb(35, 47, 97); padding-bottom: 15px; font-family: 'Trebuchet MS';">{translations[lang]}</div>
                            <div style="color: rgb(179, 161, 110); text-transform: uppercase; font-size: 13px; letter-spacing: 1px; margin-bottom: -1px; font-family: 'Trebuchet MS'; font-weight: bold;">{uni_translations[lang]}</div>
                            <div style="text-transform: uppercase; font-size: 11px; letter-spacing: 1px; margin-bottom: -1px; color: rgb(35, 47, 97); font-family: 'Trebuchet MS'; font-weight: bold;">DSVS - {student_union_translations[lang]}</div>
                            <div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: 'Trebuchet MS';">Tűzoltó u. 37-47, 1094 Budapest{address_suffix[lang]}</div>
                            {phone_html}
                            <div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: 'Trebuchet MS';"><a href="mailto:dsvs@semmelweis.hu" style="text-decoration: none; color: rgb(35, 47, 97);">dsvs@semmelweis.hu</a></div>
                            <div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: 'Trebuchet MS';"><a href="mailto:{second_email}" style="text-decoration: none; color: rgb(35, 47, 97);">{second_email}</a></div>
                        </td>
                    </tr></tbody>
                </table>
            </div>
            """)
        
        # HTML-Datei erstellen
        with open("email_signatures.html", "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Email Signatures</title>
                <style>
                    body {{
                        font-family: 'Trebuchet MS', sans-serif;
                        margin: 20px;
                    }}
                    h2 {{
                        color: rgb(35, 47, 97);
                    }}
                    button {{
                        margin-bottom: 10px;
                        padding: 5px 10px;
                        background-color: rgb(35, 47, 97);
                        color: white;
                        border: none;
                        cursor: pointer;
                        font-family: 'Trebuchet MS', sans-serif;
                    }}
                    button:hover {{
                        background-color: rgb(179, 161, 110);
                    }}
                    a {{
                        text-decoration: none; /* Entfernt die Unterstreichung */
                        color: rgb(35, 47, 97); /* Setzt die gewünschte Farbe */
                        font-family: 'Trebuchet MS', sans-serif; /* Beibehaltung der Schriftart */
                        font-size: 11px; /* Gleiche Schriftgröße wie der Rest */
                    }}
                    a:hover {{
                        color: rgb(179, 161, 110); /* Farbe beim Hover ändern */
                    }}
                </style>
                <script>
                    function copyToClipboard(lang) {{
                        const signature = document.getElementById('signature-' + lang);
                        const range = document.createRange();
                        range.selectNode(signature);
                        window.getSelection().removeAllRanges();
                        window.getSelection().addRange(range);
                        document.execCommand('copy');
                        window.getSelection().removeAllRanges();
                        alert('Signatur in die Zwischenablage kopiert: ' + lang);
                    }}
                </script>
            </head>
            <body>
                <h2>Deutsch:</h2>
                <button onclick="copyToClipboard('de')">Kopieren</button>
                {signatures['de']}
                <br>
                <h2>Englisch:</h2>
                <button onclick="copyToClipboard('en')">Kopieren</button>
                {signatures['en']}
                <br>
                <h2>Ungarisch:</h2>
                <button onclick="copyToClipboard('hu')">Kopieren</button>
                {signatures['hu']}
            </body>
            </html>
            """)
        
        # HTML-Datei im Browser öffnen
        webbrowser.open("email_signatures.html")

def main():
    generator = EmailSignatureGenerator()
    first_name = input("Vorname: ")
    last_name = input("Nachname: ")
    position = input("Position: ")
    
    generator.check_position(position)
    
    phone_number = generator.get_phone_number()
    generator.generate_email_signature(first_name, last_name, position, phone_number)

if __name__ == "__main__":
    main()
