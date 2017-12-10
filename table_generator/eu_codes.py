#!/usr/bin/env python
import pycountry

# http://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes
raw_text = """Belgium
(BE)
Greece
(EL)
Lithuania
(LT)
Portugal
(PT)
Bulgaria
(BG)
Spain
(ES)
Luxembourg
(LU)
Romania
(RO)
Czech
Republic
(CZ)
France
(FR)
Hungary
(HU)
Slovenia
(SI)
Denmark
(DK)
Croatia
(HR)
Malta
(MT)
Slovakia
(SK)
Germany
(DE)
Italy
(IT)
Netherlands
(NL)
Finland
(FI)
Estonia
(EE)
Cyprus
(CY)
Austria
(AT)
Sweden
(SE)
Ireland
(IE)
Latvia
(LV)
Poland
(PL)
United
Kingdom
(UK)
Iceland
(IS)
Norway
(NO)
Liechtenstein
(LI)
Switzerland
(CH)
Montenegro
(ME)
The
former
Yugoslav
Republic
of
Macedonia
(MK)
Albania
(AL)
Serbia
(RS)
Turkey
(TR)
Kosovo
(XK)
Bosnia and Herzegovina
(BA)
Armenia
(AM)
Belarus
(BY)
Georgia
(GE)
Azerbaijan
(AZ)
Moldova
(MD)
Ukraine
(UA)
Algeria
(DZ)
Lebanon
(LB)
Syria
(SY)
Egypt
(EG)
Libya
(LY)
Tunisia
(TN)
Israel
(IL)
Morocco
(MA)
Jordan
(JO)
Palestine
(PS)
Russia
(RU)
Argentina
(AR)
China(except Hong
Kong)
(CN_X_HK)
Mexico
(MX)
South
Africa
(ZA)
Australia
(AU)
Hong
Kong
(HK)
Nigeria
(NG)
South
Korea
(KR)
Brazil
(BR)
India
(IN)
New
Zealand
(NZ)
Taiwan
(TW)
Canada
(CA)
Japan
(JP)
Singapore
(SG)
United
States
(US)"""

eu_to_alpha_2 = {}

name_collector = []
for line in raw_text.split('\n'):
    line = line.strip()
    if line.startswith('(') and line.endswith(')'):
        country_name = ' '.join(name_collector)
        try:
            country_code = pycountry.countries.lookup(country_name).alpha_2
            eu_code = line.strip('()')
            if eu_code != country_code:
                eu_to_alpha_2[eu_code] = country_code
        except LookupError:
            pass
        name_collector = []
    else:
        name_collector.append(line)
