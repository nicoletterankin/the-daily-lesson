#!/usr/bin/env python3
"""Machine-verify pet deck QRs with zbar (print-gate quality decoder), 100% + 50% scale."""
import cv2, json, sys, pathlib
from pyzbar import pyzbar

SUITS = {"ground": "g", "feel": "f", "remember": "r", "tend": "t"}

def decode(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for cand in (g, cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]):
        for sym in pyzbar.decode(cand, symbols=[pyzbar.ZBarSymbol.QRCODE]):
            return sym.data.decode()
    return None

results, bad = {}, 0
base = pathlib.Path(sys.argv[1])
for suit, letter in SUITS.items():
    for n in range(1, 14):
        cid = f"pet-{suit}{n}"
        expected = f"https://held.press/p/p{letter}{n}"
        img = cv2.imread(str(base / f"{cid}-back.jpg"))
        full = decode(img)
        half = decode(cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
        ok = (full and full.rstrip("/") == expected) and (half and half.rstrip("/") == expected)
        if not ok:
            bad += 1
        results[cid] = {"status": "OK" if ok else "FAIL", "expected": expected,
                        "decoded_100": full, "decoded_50": half}

print(json.dumps({"total": len(results), "failures": bad}))
json.dump(results, open(base.parent / "qr_verify_zbar.json", "w"), indent=1)
for cid, r in results.items():
    if r["status"] != "OK":
        print(cid, r)
