import json
import sqlite3
import os
import glob

def catalog_ondemand_assets():
    manifest_path = r"E:\REA\workspace\nikke-maiden\meta\manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assets = manifest.setdefault("assets", {})
    initial_count = len(assets)

    # 1. SAUS JA Story and Lobby Dialogue Packages
    cat_ja = os.path.expandvars("%USERPROFILE%/AppData/LocalLow/com_proximabeta/NIKKE/saus/ja/asset-catalog-2480009861.cat")
    conn = sqlite3.connect(cat_ja)
    cur = conn.cursor()

    target_story_lines = [
        ("d_main_13_08_e_181", "Main Scenario Ch 13 Ep 8"),
        ("d_main_24af_06_181", "Main Scenario Ch 24 After Ep 6"),
        ("d_main_26af_01_181", "Main Scenario Ch 26 After Ep 1"),
        ("d_main_27_07_181", "Main Scenario Ch 27 Ep 7"),
        ("d_main_31_06_181", "Main Scenario Ch 31 Ep 6"),
        ("d_main_31_08_181", "Main Scenario Ch 31 Ep 8"),
        ("event_beautyfullshot1_02_s_181", "Beauty Full Shot Part 1 Ep 2"),
        ("event_goldencoinrush1_03_s_181", "Golden Coin Rush Part 1 Ep 3"),
        ("event_redash1_06_e_181", "Red Ash Part 1 Ep 6"),
        ("event_redash2_06_e_181", "Red Ash Part 2 Ep 6"),
        ("event_seayouagain1_intermission_01_181", "Sea, You, Again Part 1 Intermission 1"),
        ("event_seayouagain2_06_e_181", "Sea, You, Again Part 2 Ep 6")
    ]

    for key, ctx in target_story_lines:
        cur.execute(
            "SELECT a.Key, f.Id, f.RelativePath, hex(f.Hash), f.Size, f.IsLocal "
            "FROM AssetEntity a JOIN FileInfoEntity f ON a.FileId = f.Id WHERE a.Key = ?",
            (key,)
        )
        row = cur.fetchone()
        if row:
            k = f"{row[2]}:{row[0]}"
            assets[k] = {
                "category": "Remote Story Dialogue Audio (JA)",
                "type": "standalone",
                "scope": "in_scope",
                "script_key": row[0],
                "file_id": row[1],
                "container_path": row[2],
                "internal_id": "{NK.Addressable.HostConst.HostSoundLoadURL}/" + row[2],
                "sha256": row[3],
                "size_bytes": row[4],
                "is_local": row[5],
                "context": ctx,
                "status": "cataloged_on_demand_cdn"
            }

    # High-affinity lobby touch lines
    cur.execute(
        "SELECT a.Key, f.Id, f.RelativePath, hex(f.Hash), f.Size, f.IsLocal "
        "FROM AssetEntity a JOIN FileInfoEntity f ON a.FileId = f.Id WHERE f.Id = 939596904"
    )
    for row in cur.fetchall():
        k = f"{row[2]}:{row[0]}"
        assets[k] = {
            "category": "Character Voiceline (Japanese - Remote)",
            "type": "standalone",
            "scope": "in_scope",
            "script_key": row[0],
            "file_id": row[1],
            "container_path": row[2],
            "internal_id": "{NK.Addressable.HostConst.HostSoundLoadURL}/" + row[2],
            "sha256": row[3],
            "size_bytes": row[4],
            "is_local": row[5],
            "context": "Maiden high-affinity lobby touch",
            "status": "cataloged_on_demand_cdn"
        }

    # 2. Addressables Remote Asset Packages
    addr_dir = os.path.expandvars("%USERPROFILE%/AppData/LocalLow/com_proximabeta/NIKKE/com.unity.addressables")
    cat_files = glob.glob(os.path.join(addr_dir, "*.json"))

    hd_bgs = []
    spine_scenes = []
    live_wallpapers = []

    for cf in cat_files:
        try:
            with open(cf, "r", encoding="utf-8") as f:
                data = json.load(f)
            internal_ids = data.get("m_InternalIds", [])
            for path in internal_ids:
                p_lower = path.lower()
                if "scenariobackground(hd)" in p_lower:
                    for ev in ["acpu", "phantomthief", "beautyfullshot", "bluewater", "darkhero", "goldencoinrush", "miraclesnow", "neverland", "seayouagain"]:
                        if ev in p_lower:
                            hd_bgs.append((ev, path))
                            break
                elif "spineeventscenesgroup(hd)" in p_lower:
                    for ev in ["beautyfullshot_03", "bluewaterisland_01", "goldencoinrush_02", "neverland_02", "seayouagain_04", "acpufreeze_01"]:
                        if ev in p_lower:
                            spine_scenes.append((ev, path))
                            break
                elif "livewallpaperprefabs" in p_lower:
                    for ev in ["beautyfullshot_03", "bluewaterisland_01", "goldencoinrush_02", "neverland_01", "neverland_02", "seayouagain_04", "acpufreeze_01", "c181_cutscene", "c183_cutscene"]:
                        if ev in p_lower:
                            live_wallpapers.append((ev, path))
                            break
        except Exception:
            pass

    for ev, p in sorted(list(set(hd_bgs))):
        fname = os.path.basename(p)
        assets[fname] = {
            "category": "Environment & Scenario Background (HD)",
            "type": "compound",
            "scope": "in_scope",
            "internal_id": p,
            "event": ev,
            "status": "cataloged_on_demand_cdn"
        }

    for ev, p in sorted(list(set(spine_scenes))):
        fname = os.path.basename(p)
        assets[fname] = {
            "category": "Animated Event Card (Spine Live2D - Remote)",
            "type": "compound",
            "scope": "in_scope",
            "internal_id": p,
            "event": ev,
            "status": "cataloged_on_demand_cdn"
        }

    for ev, p in sorted(list(set(live_wallpapers))):
        fname = os.path.basename(p)
        assets[fname] = {
            "category": "Live Wallpaper Prefab (Remote)",
            "type": "compound",
            "scope": "in_scope",
            "internal_id": p,
            "event": ev,
            "status": "cataloged_on_demand_cdn"
        }

    # Update summary totals
    in_scope_assets = [k for k, v in assets.items() if v.get("scope") == "in_scope"]
    out_of_scope_assets = [k for k, v in assets.items() if v.get("scope") == "out_of_scope"]

    manifest["total_cataloged"] = len(assets)
    manifest["in_scope_total"] = len(in_scope_assets)
    manifest["out_of_scope_total"] = len(out_of_scope_assets)

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Cataloged on-demand CDN assets successfully:")
    print(f"  Previous asset count: {initial_count}")
    print(f"  Updated total cataloged: {len(assets)}")
    print(f"  In-scope total: {len(in_scope_assets)}")
    print(f"  Out-of-scope total: {len(out_of_scope_assets)}")

if __name__ == "__main__":
    catalog_ondemand_assets()
