import pdfplumber, re, json, sys
pdf = pdfplumber.open(sys.argv[1])
tables = {"A":[], "B":[]}  # A: to Kpb (CKR..JAKK), B: to Bks/Ckr
for pi, page in enumerate(pdf.pages):
    text = page.extract_text() or ""
    if "Bekasi" not in text.split("\n")[0] and "Commuter Lin Bekasi" not in text: continue
    key = "A" if "Kampung Bandan-Bekasi" in text else "B"
    words = page.extract_words(keep_blank_chars=False)
    # header row: find word 'CUK' and 'SUD'
    hdr_names = ["CKR","TLM","CIT","TB","BKST","BKS","KRI","CUK","KLDB","BUA","KLD","JNG","POK","KMT","GST","PSE","KMO","RJW","MTR","MRI","SUD","SUDB","KAT","THB","DU","AK","KPB","JAKK"]
    hdr = [w for w in words if w["text"] in hdr_names]
    top = min(w["top"] for w in hdr if w["text"]=="CUK")
    hdr = {w["text"]:(w["x0"]+w["x1"])/2 for w in hdr if abs(w["top"]-top)<3}
    # group rows
    rows = {}
    for w in words:
        if w["top"] <= top+3: continue
        rows.setdefault(round(w["top"]), []).append(w)
    # merge close tops
    keys = sorted(rows); merged=[]
    for k in keys:
        if merged and k-merged[-1][0] <= 2: merged[-1][1].extend(rows[k])
        else: merged.append([k, list(rows[k])])
    for _, ws in merged:
        ws.sort(key=lambda w:w["x0"])
        if not re.fullmatch(r"\d+", ws[0]["text"]): continue
        times = {}
        left = []
        for w in ws[1:]:
            if re.fullmatch(r"\d\d:\d\d|Ls", w["text"]):
                c=(w["x0"]+w["x1"])/2
                st=min(hdr, key=lambda s:abs(hdr[s]-c))
                if abs(hdr[st]-c) > 12: print("WARN far", w["text"], st, file=sys.stderr)
                if w["text"]!="Ls": times[st]=w["text"]
            elif not times:
                left.append(w["text"])
        s=" ".join(left)
        m=re.match(r"(\d+F?)(?:\s*-\s*(\d+F?))?\s+(.*)", s)
        tables[key].append({"no":m.group(1),"no2":m.group(2),"rel":m.group(3),"t":times,"page":pi+1})
for k in tables: print(k, len(tables[k]), file=sys.stderr)
json.dump(tables, open("parsed.json","w"))
