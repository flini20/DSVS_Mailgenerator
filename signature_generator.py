import urllib.parse
import webbrowser

class EmailSignatureGenerator:
    def __init__(self):
        self.position_lookup = {
            "Vorsitzender": {"de": "Vorsitzender", "en": "Chairperson", "hu": "Elnök"},
            "Stellvertretender Vorsitzender": {"de": "Stellvertretender Vorsitzender", "en": "Vice Chairperson", "hu": "Alelnök"},
            "Generalsekretär": {"de": "Generalsekretär", "en": "Secretary General", "hu": "Főtitkár"},
            "Pressesprecher": {"de": "Pressesprecher", "en": "Press Officer", "hu": "Sajtószóvivő"},
            "Abgeordneter": {"de": "Abgeordneter", "en": "Delegate", "hu": "Küldött"},
        }
    
    def check_position(self, position):
        if position not in self.position_lookup:
            raise ValueError("Non existing position!")
    
    def generate_email_signature(self, first_name, last_name, position, phone_number):
        self.check_position(position)
        translations = self.position_lookup[position]
        
        uni_translations = {"de": "Semmelweis Universität", "en": "Semmelweis University", "hu": "Semmelweis Egyetem"}
        student_union_translations = {"de": "Deutschsprachige Studentenvertretung", "en": "German Speaking Student Union", "hu": "Német Nyelvű Hallgatói Képviselet"}
        address_suffix = {"de": ", HUNGARY", "en": ", HUNGARY", "hu": ""}
        
        names = {
            "de": f"{first_name} {last_name}",
            "en": f"{first_name} {last_name}",
            "hu": f"{last_name} {first_name}"
        }
        
        signatures = {}
        for lang in ["de", "en", "hu"]:
            phone_html = f'<div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: \"Trebuchet MS\";"><a href="tel:{phone_number}">{phone_number}</a></div>' if phone_number else ""
            
            signatures[lang] = f"""
            <table id="tableFrame">
                <tbody><tr>
                    <td id=\"left\" style=\"padding-right: 20px;border-right: 3px solid #b3a16e;\"><img src=\"https://semmelweis.hu/img/kekcimer_180.png\" name=\"logo\" id=\"logo\" width=\"120\" height=\"120\"></td> 
                    <td id=\"dataFrame\" style=\"padding-left:30px;\">
                        <b style=\"font-size: 16pt; text-transform: uppercase; color: rgb(35, 47, 97); font-family: 'Trebuchet MS';\">{names[lang]}</b>
                        <div style=\"font-size: 10.5pt; text-transform: uppercase; color: rgb(35, 47, 97); padding-bottom: 15px; font-family: 'Trebuchet MS';\">{translations[lang]}</div>
                        <div style=\"color: rgb(179, 161, 110); text-transform: uppercase; font-size: 13px; letter-spacing: 1px; margin-bottom: -1px; font-family: 'Trebuchet MS'; font-weight: bold;\">{uni_translations[lang]}</div>
                        <div style=\"text-transform: uppercase; font-size: 11px; letter-spacing: 1px; margin-bottom: -1px; color: rgb(35, 47, 97); font-family: 'Trebuchet MS'; font-weight: bold;\">DSVS - {student_union_translations[lang]}</div>
                        <div style=\"font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: 'Trebuchet MS';\">Tűzoltó u. 37-47, 1094 Budapest{address_suffix[lang]}</div>
                        {phone_html}
                        <div style=\"font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: 'Trebuchet MS';\"><a href=\"mailto:dsvs@semmelweis.hu\">dsvs@semmelweis.hu</a></div>
                        <div style=\"font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: 'Trebuchet MS';\"><a href=\"mailto:{position.lower().replace(' ', '')}@semmelweis.hu\">{position.lower().replace(' ', '')}@semmelweis.hu</a></div>
                    </td>
                </tr></tbody>
            </table>
            """
        
        body = f"""
        Hejj {first_name} {last_name},
        
        hier findest du alle drei Versionen (Deutsch, Englisch, Ungarisch) deiner Emailsignatur zum copy and pasten.
        
        Deutsch:
        
        {signatures['de']}
        
        --------------------------------------------
        
        Englisch:
        
        {signatures['en']}
        
        --------------------------------------------
        
        Ungarisch:
        
        {signatures['hu']}
        
        
        *Dies ist eine automatisch generierte Email*
        """
        
        mailto_link = f"mailto:?cc=dsvs@semmelweis.hu&subject=Email Signatur {position}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto_link)

def main():
    generator = EmailSignatureGenerator()
    first_name = input("Vorname: ")
    last_name = input("Nachname: ")
    position = input("Position: ")
    
    generator.check_position(position)
    
    phone_number = input("Telefonnummer (optional): ") or None
    generator.generate_email_signature(first_name, last_name, position, phone_number)

if __name__ == "__main__":
    main()
