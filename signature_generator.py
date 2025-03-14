# Email Signature Generator

import urllib.parse

def get_position_translation(position):
    position_lookup = {
        "Vorsitzender": ("Chairman", "Elnök"),
        "Stellv. Vorsitzender": ("Vice Chairman", "Alelnök"),
        "Schriftführer": ("Secretary", "Titkár"),
        # Insert further positions here
    }
    return position_lookup.get(position, (position, position))

def generate_signature(first_name, last_name, position, phone):
    pos_en, pos_hu = get_position_translation(position)
    name_hu = f"{last_name} {first_name}"
    name_default = f"{first_name} {last_name}"
    
    signatures = {}
    for lang, (name, pos, univ, rep, country) in {
        "de": (name_default, position, "Semmelweis Universität", "Deutschsprachige Studentenvertretung", ", HUNGARY"),
        "en": (name_default, pos_en, "Semmelweis University", "German Speaking Student Union", ", HUNGARY"),
        "hu": (name_hu, pos_hu, "Semmelweis Egyetem", "Német Nyelvű Hallgatói Képviselet", "")
    }.items():
        phone_line = f'<div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: \"Trebuchet MS\";"> <a href="tel:{phone}">{phone}</a></div>' if phone else ""
        
        signatures[lang] = f'''
<tbody><tr>
<td id="left" style="padding-right: 20px;border-right: 3px solid #b3a16e;"><img src="https://semmelweis.hu/img/kekcimer_180.png" name="logo" id="logo" width="120" height="120"></td> 
<td id="dataFrame" style="padding-left:30px;"><b style="font-size: 16pt; text-transform: uppercase; color: rgb(35, 47, 97); font-family: \"Trebuchet MS\";">{name}</b>
<div style="font-size: 10.5pt; text-transform: uppercase; color: rgb(35, 47, 97); padding-bottom: 15px; font-family: \"Trebuchet MS\";">{pos}</div>
<div style="color: rgb(179, 161, 110); text-transform: uppercase; font-size: 13px; letter-spacing: 1px; margin-bottom: -1px; font-family: \"Trebuchet MS\"; font-weight: bold;">{univ}</div>
<div style="text-transform: uppercase; font-size: 11px; letter-spacing: 1px; margin-bottom: -1px; color: rgb(35, 47, 97); font-family: \"Trebuchet MS\"; font-weight: bold;">DSVS - {rep}</div>
<div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: \"Trebuchet MS\";">Tűzoltó u. 37-47, 1094 Budapest{country}</div>
{phone_line}
<div style="font-size: 11px; color: rgb(35, 47, 97); margin-bottom: -1px; font-family: \"Trebuchet MS\";"> <a href="mailto:dsvs@semmelweis.hu">dsvs@semmelweis.hu</a></div>
</td></tr></tbody>
'''
    return signatures

def create_mailto_link(first_name, last_name, position, phone):
    signatures = generate_signature(first_name, last_name, position, phone)
    body = f"""
Hejj {first_name} {last_name},

hier findest du alle drei Versionen (Deutsch, Englisch, Ungarisch) deiner Emailsignatur zum copy and pasten.
Here you can find all three versions (German, English, Hungarian) of your email signature to copy and paste.
Itt megtalálod az e-mail aláírásod mindhárom változatát (német, angol, magyar) másolásra és beillesztésre.

Deutsch:

{signatures['de']}

----------------------------

Englisch:

{signatures['en']}

----------------------------

Ungarisch:

{signatures['hu']}


*Dies ist eine automatisch generierte Email*
    """
    mailto_link = f"mailto:?cc=dsvs@semmelweis.hu&subject=Email Signatur {position}&body={urllib.parse.quote(body)}"
    return mailto_link

if __name__ == "__main__":
    first_name = input("Vorname: ")
    last_name = input("Nachname: ")
    position = input("Position: ")
    phone = input("Telefonnummer (optional): ").strip() or None
    
    mailto_link = create_mailto_link(first_name, last_name, position, phone)
    print("Öffne folgenden Link in deinem Browser:")
    print(mailto_link)
