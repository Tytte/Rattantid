import os
import json
from datetime import datetime, timezone
import urllib.request
import xml.etree.ElementTree as ET

api_key = os.environ.get("TRAFIKVERKET_API_KEY")

print("Rattantid startar")

if not api_key:
    print("API-nyckel saknas")
    raise SystemExit(1)

print("API-nyckel hittad")

query = f"""<REQUEST>
<LOGIN authenticationkey="{api_key}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.9">
<INCLUDE>AdvertisedTrainIdent</INCLUDE>
<INCLUDE>LocationSignature</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>EstimatedTimeAtLocation</INCLUDE>
</QUERY>
</REQUEST>"""

request = urllib.request.Request(
    "https://api.trafikinfo.trafikverket.se/v2/data.xml",
    data=query.encode("utf-8"),
    headers={"Content-Type": "application/xml"},
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()

    root = ET.fromstring(data)
    trains = root.findall(".//TrainAnnouncement")
    print("Kontakt med Trafikverket lyckades")
    print("Antal tågannonseringar:", len(trains))

    print("Första tågannonseringen:", ET.tostring(trains[0], encoding="unicode") if trains else "Inga annonseringar")
except Exception as error:
    print("Fel vid hämtning:", error)
    raise SystemExit(1)
output = []
for train in trains:
    output.append(ET.tostring(train, encoding="unicode"))
with open("trafikdata.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False)
