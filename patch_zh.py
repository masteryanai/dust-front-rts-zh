#!/usr/bin/env python3
"""
Patch Dust Front RTS resources.assets — add Chinese column to localization CSVs.
Uses UnityPy to read/write the binary asset file correctly.
"""
import sys
import csv
import io

sys.path.insert(0, '/home/noman/.local/lib/python3.12/site-packages')
import UnityPy

from translations import TRANSLATIONS

import argparse
_parser = argparse.ArgumentParser()
_parser.add_argument("--asset", default="Dust Front RTS Demo/Dust Front RTS_Data/resources.assets")
_args, _ = _parser.parse_known_args()
ASSET_PATH = _args.asset
LOC_ASSETS = {
    "Localization_DUST_FRONT - Main",
    "Localization_DUST_FRONT - Tutorial-locals",
}


def add_chinese_column(csv_text: str) -> str:
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    if not rows:
        return csv_text

    header = rows[0]
    if "Chinese" in header:
        print("  Chinese column already present — skipping")
        return csv_text

    out_rows = [header + ["Chinese"]]
    missing = []
    for row in rows[1:]:
        if not row:
            out_rows.append(row)
            continue
        key = row[0] if row else ""
        zh = TRANSLATIONS.get(key, "")
        if not zh and key:
            missing.append(key)
        out_rows.append(row + [zh])

    if missing:
        print(f"  ⚠  {len(missing)} keys not in TRANSLATIONS dict:")
        for k in missing[:10]:
            print(f"     {k}")
        if len(missing) > 10:
            print(f"     ... and {len(missing) - 10} more")

    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerows(out_rows)
    return buf.getvalue()


def main():
    print(f"Loading {ASSET_PATH} ...")
    env = UnityPy.load(ASSET_PATH)

    patched = 0
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        data = obj.read()
        if data.m_Name not in LOC_ASSETS:
            continue

        print(f"\nPatching: {data.m_Name}")
        raw = data.m_Script
        if isinstance(raw, bytes):
            csv_text = raw.decode("utf-8")
        else:
            csv_text = raw

        new_csv = add_chinese_column(csv_text)
        data.m_Script = new_csv
        data.save()
        patched += 1
        print(f"  Done — {len(new_csv)} chars written")

    if patched == 0:
        print("No TextAssets matched — nothing changed")
        sys.exit(1)

    import os, shutil, tempfile

    env.file.mark_changed()
    tmp_dir = tempfile.mkdtemp()
    try:
        env.save(out_path=tmp_dir)
        out_file = os.path.join(tmp_dir, os.path.basename(ASSET_PATH))
        if not os.path.exists(out_file):
            # fallback: find any file in tmp_dir
            files = os.listdir(tmp_dir)
            if not files:
                print("ERROR: env.save() wrote nothing")
                sys.exit(1)
            out_file = os.path.join(tmp_dir, files[0])
        shutil.move(out_file, ASSET_PATH)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    size = os.path.getsize(ASSET_PATH)
    print(f"\nSaved to {ASSET_PATH}")
    print(f"File size: {size:,} bytes")


if __name__ == "__main__":
    main()
