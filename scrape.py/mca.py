import os
import requests
import base64
from datetime import datetime

BASE_URL = "https://www.mca.gov.in"
METADATA_URL = BASE_URL + "/bin/ebook/service/documentMetadata"
PDF_URL = BASE_URL + "/bin/ebook/dms/getdocument"

session = requests.Session()

# Cookies copied from browser
session.cookies.update({
    "JSESSIONID": "node0ugt4lz6fgxkw1g60277a8w9fn221.node0",
    "__UUID-HASH": "b4b6a0a8c11e082fd62e142efeaf9954$",
    "bm_sv": "D07A3C501A8CBDDA63400719A93C588A~YAAQb88uF+ANiUKfAQAAOo50UADZycHSCy02dFH0JeBIEvY10K+Kfhr1Fibc8Pyx4EZmNUGJ63pfUIVVlvm2SbvOUl2c394FvVDBZTcaZKQ+GieB1m4m1Xmii2lLirNvB0KcFPm+JZFNNCfE1/BJcxyItXm2oD1JFSHfMirpXNq3xrBwLZ36yfj0eJr1iDndZf8PF3wkWXxxi43JbXexKu0dmBbG/kT4KahJfVDWszLYhhMGa/PX+GnNNCqXEmAjxyQ=~1",
    "ak_bm sc": "38BD5835856290F307744A95B473EB89~000000000000000000000000000000~YAAQf88uF/XvZEGfAQAAyTQtUAAFByUcK+OclaRRXFI66NPCtHDhcBBkFZoxOpEKCl5ouHH54FD53hqgYtPZ+WpU+Ngn/cTARhI8cCqFFneHrV3bNXTmaWCU3WEOFYx0C7HjoaKId/fS87uwPafXCuarZqHJOSJZPJTe4C2qJkXObObJz/GqQpYKonnMxrDS9yo977bBdCbv3bTI35y016j6SLqFzPlwU5kaI3vdeL1qrtwp69lWrO7JES1DAdiNP01QT4wy3FkgPaty/YofetFQC0sq8TusD3cyVO2r8vlKWIZDBSQzwcwZ+HKbFsyQV21y+K18rjo0pMT8AQw/IEfjG6AU9BejiuY6A2OJ45zg8RnExBZgm3zJ+cqu6EKgZqVTvL+PwlFSoEgCVhsqAp08b0/MxEPOHvJsBsFmkte14ct64w=="
})

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Referer": "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/circulars.html",
    "Origin": "https://www.mca.gov.in",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_metadata():
    params = {
        "docCategory": "Circulars",
        "flag": "initial",
        "status": "Current"
    }

    response = session.get(
        METADATA_URL,
        params=params,
        headers=headers,
        timeout=30
    )

    print("Metadata Status:", response.status_code)
    response.raise_for_status()

    return response.json()


docs = fetch_metadata()

print(f"Found {len(docs['data'])} total circulars")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

START_DATE = datetime(2026, 1, 1)

for doc in reversed(docs["data"]):
    encodeddoc=base64.b64encode(doc["link"].encode()).decode()
    date = datetime.strptime(doc["notificationdate"], "%m/%d/%Y")

    if date < START_DATE:
        break

    print("\n------------------------------------")
    print(doc["docName"])
    print(doc["notificationdate"])

    response = session.get(
        PDF_URL,
        params={
            "doc": encodeddoc,
            "docCategory": "Circulars",
           
        },
        headers=headers,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Size:", len(response.content))

    if response.status_code != 200:
        print(response.text[:500])
        continue

    if "application/pdf" not in response.headers.get("Content-Type", ""):
        print("Not a PDF!")
        print(response.text[:500])
        continue

    filename = f"{doc['docName']}.pdf"

    for ch in '\\/:*?"<>|':
        filename = filename.replace(ch, "_")

    filepath = os.path.join(DOWNLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"Saved -> {filepath}")

print("\nDone!")