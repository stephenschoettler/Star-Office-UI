#!/usr/bin/env python3
"""
Anglicize Star Office UI — Phase 2 Translation Script
Uses OpenAI API since ANTHROPIC_API_KEY not set in this shell.
"""

import os, re, json, sys, time
from openai import OpenAI

BASE = os.path.dirname(os.path.abspath(__file__))
MAP_FILE = os.path.join(BASE, "translation-map.json")

CJK_RE = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\u3040-\u309f\u30a0-\u30ff]+')

TARGET_FILES = [
    "frontend/index.html",
    "frontend/game.js",
    "frontend/layout.js",
    "frontend/invite.html",
    "frontend/join.html",
    "frontend/join-office-skill.md",
    "backend/app.py",
    "agent-invite-template.txt",
    "office-agent-push.py",
    "convert_to_webp.py",
    "set_state.py",
    "state.json",
    "agents-state.json",
    "join-keys.json",
    "docs/FEATURES_NEW_2026-03-01.md",
    "docs/OPEN_SOURCE_RELEASE_CHECKLIST.md",
    "docs/PROJECT_SUMMARY_2026-03-01.md",
    "docs/STAR_OFFICE_UI_OVERVIEW.md",
]

def extract_strings(filepath):
    strings = set()
    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for m in CJK_RE.finditer(content):
            strings.add(m.group())
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
    return strings

def batch_translate(strings, client):
    if not strings:
        return {}
    strings_list = sorted(strings)
    numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(strings_list))
    prompt = f"""You are translating UI strings for a pixel-art office dashboard used by AI agents. Translate each Chinese string to natural, concise English.

Context: Pixel office dashboard for AI agents. States: idle (break room), writing/working, researching, executing, syncing, error (bug zone). There is a "Yesterday's Notes" memo panel. Office owner = "Star". Guests are other AI agents.

Key mappings:
- "海辛" = "Star"
- "海辛小龙虾" = "Star"
- "龙虾" = "agent" (UI) or "lobster" (flavor)
- "昨日小记" = "Yesterday's Notes"
- "像素办公室" = "Pixel Office"
- "看板" = "dashboard"
- "待命" = "Standby"
- "工作中" = "Working"
- "同步中" = "Syncing"
- "报警" = "Alert"
- "访客" = "Guest"
- "主人" = "you" or "user"
- "牌匾" = "sign"
- "团队成员" = "Team Member"
- Chinese quotes in 「」 = translate the meaning as natural English flavor text
- Code comments/error messages = developer-friendly English

Return ONLY a JSON object: {{"1": "...", "2": "...", ...}}

Strings:
{numbered}"""

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4096,
    )
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = re.sub(r'^```\w*\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)
    result_map = json.loads(raw)
    translations = {}
    for i, s in enumerate(strings_list):
        key = str(i + 1)
        translations[s] = result_map.get(key, s)
    return translations

def apply_translations(filepath, translation_map):
    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            content = f.read()
        original = content
        sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
        for zh in sorted_keys:
            en = translation_map[zh]
            if zh != en and zh in content:
                content = content.replace(zh, en)
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  Error applying to {filepath}: {e}")
        return False

def main():
    client = OpenAI()  # uses OPENAI_API_KEY from env
    print("=== Phase 1: Collecting Chinese strings ===")
    all_strings = set()
    for rel_path in TARGET_FILES:
        fp = os.path.join(BASE, rel_path)
        if os.path.exists(fp):
            strings = extract_strings(fp)
            if strings:
                print(f"  {rel_path}: {len(strings)} CJK strings")
                all_strings.update(strings)
        else:
            print(f"  SKIP (not found): {rel_path}")
    print(f"\nTotal unique CJK strings: {len(all_strings)}")
    print("\n=== Phase 2: Translating via OpenAI API ===")
    translation_map = {}
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE) as f:
            translation_map = json.load(f)
        print(f"  Loaded {len(translation_map)} existing translations")
    untranslated = [s for s in all_strings if s not in translation_map]
    print(f"  Need to translate: {len(untranslated)} strings")
    BATCH_SIZE = 80
    for i in range(0, len(untranslated), BATCH_SIZE):
        batch = untranslated[i:i+BATCH_SIZE]
        print(f"  Translating batch {i//BATCH_SIZE + 1} ({len(batch)} strings)...")
        try:
            new_translations = batch_translate(set(batch), client)
            translation_map.update(new_translations)
            with open(MAP_FILE, 'w', encoding='utf-8') as f:
                json.dump(translation_map, f, ensure_ascii=False, indent=2)
            print(f"    OK - {len(new_translations)} translations saved")
        except Exception as e:
            print(f"    ERROR: {e}")
            sys.exit(1)
        time.sleep(0.3)
    print(f"\nTranslation map saved to {MAP_FILE}")
    print("\n=== Phase 3: Applying translations ===")
    for rel_path in TARGET_FILES:
        fp = os.path.join(BASE, rel_path)
        if os.path.exists(fp):
            changed = apply_translations(fp, translation_map)
            status = "updated" if changed else "no changes"
            print(f"  {rel_path}: {status}")
    print("\n=== Done! ===")

if __name__ == "__main__":
    main()
