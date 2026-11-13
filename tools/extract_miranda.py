import os
import sys
import json
import struct
import zstandard as zstd
from PIL import Image
import texture2ddecoder
import UnityPy
from UnityPy.streams import EndianBinaryReader
from UnityPy.files import BundleFile, File

sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE = r"E:\REA\workspace\nikke-maiden"
ASSETS_DIR = os.path.join(WORKSPACE, "assets")
DP_IDX = r"D:\Games\NIKKE\Unity\com_proximabeta_NIKKE\com.shiftup.patch\dp\chunk\store.cdb.idx"
DP_CDB = r"D:\Games\NIKKE\Unity\com_proximabeta_NIKKE\com.shiftup.patch\dp\chunk\store.cdb"
CORE_IDX = r"D:\Games\NIKKE\Unity\com_proximabeta_NIKKE\com.shiftup.patch\core\chunk\store.cdb.idx"
CORE_CDB = r"D:\Games\NIKKE\Unity\com_proximabeta_NIKKE\com.shiftup.patch\core\chunk\store.cdb"

SAUS_JA_DIR = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\com_proximabeta\NIKKE\saus\ja")
LSS_DIR = r"E:\Games\NIKKE\NIKKE\game\NIKKE_Data\StreamingAssets\lss"

dctx = zstd.ZstdDecompressor()

def read_bundle_range(idx_path, cdb_path, start_chunk, max_chunks=80):
    accum = bytearray()
    curr = start_chunk
    with open(idx_path, "rb") as fi, open(cdb_path, "rb") as fc:
        while True:
            fi.seek(28 + curr * 28)
            rec = fi.read(28)
            if not rec:
                break
            off, clen = struct.unpack("<QI", rec[:12])
            fc.seek(off)
            decomp = dctx.decompress(fc.read(clen))
            if decomp.startswith(b"UnityFS") and curr > start_chunk:
                break
            accum.extend(decomp)
            curr += 1
            if curr > start_chunk + max_chunks:
                break
    return bytes(accum), curr - 1

def save_texture(obj_data, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img = obj_data.image
    img.save(out_path)

def extract_spine_bundle(start_chunk, out_dir, model_name):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting Spine puppet {model_name} from chunk {start_chunk}...")
    bdata, end_c = read_bundle_range(DP_IDX, DP_CDB, start_chunk)
    env = UnityPy.load(bdata)
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            script_bytes = d.m_Script.encode('utf8', 'surrogateescape') if isinstance(d.m_Script, str) else bytes(d.m_Script)
            if name.endswith(".skel") or "skel" in name:
                p = os.path.join(out_dir, f"{model_name}.skel")
                with open(p, "wb") as f:
                    f.write(script_bytes)
                print(f"  Saved {p} ({len(script_bytes)} bytes)")
            elif name.endswith(".atlas") or "atlas" in name:
                p = os.path.join(out_dir, f"{model_name}.atlas")
                with open(p, "wb") as f:
                    f.write(script_bytes)
                print(f"  Saved {p} ({len(script_bytes)} bytes)")
        elif obj.type.name == "Texture2D":
            d = obj.read()
            p = os.path.join(out_dir, f"{model_name}.png")
            d.image.save(p)
            print(f"  Saved {p} ({d.image.size})")

def extract_favoriteitem_scene(start_chunk, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting FavoriteItemScene from chunk {start_chunk}...")
    bdata, end_c = read_bundle_range(DP_IDX, DP_CDB, start_chunk)
    env = UnityPy.load(bdata)
    saved_count = 0
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            script_bytes = d.m_Script.encode('utf8', 'surrogateescape') if isinstance(d.m_Script, str) else bytes(d.m_Script)
            ext = ".skel" if "skel" in name else ".atlas"
            p = os.path.join(out_dir, f"{name}{ext if not name.endswith(ext) else ''}")
            with open(p, "wb") as f:
                f.write(script_bytes)
            saved_count += 1
        elif obj.type.name == "Texture2D":
            try:
                d = obj.read()
                name = getattr(d, 'm_Name', getattr(d, 'name', ''))
                if name:
                    p = os.path.join(out_dir, f"{name}.png")
                    d.image.save(p)
                    saved_count += 1
            except Exception as e:
                print(f"  Warning: skipping texture in FavoriteItemScene due to: {e}")
        elif obj.type.name == "Mesh":
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            if name:
                p = os.path.join(out_dir, f"{name}.obj")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(d.export())
                saved_count += 1
    print(f"  Saved {saved_count} FavoriteItemScene assets to {out_dir}")

def extract_sd_models(start_chunk, out_dir, model_name):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting 3D SD model {model_name} from chunk {start_chunk}...")
    bdata, end_c = read_bundle_range(DP_IDX, DP_CDB, start_chunk, max_chunks=15)
    env = UnityPy.load(bdata)
    for obj in env.objects:
        if obj.type.name == "Mesh":
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            if name:
                p = os.path.join(out_dir, f"{name}.obj")
                with open(p, "w", encoding="utf-8") as f:
                    f.write(d.export())
                print(f"  Saved {p}")
        elif obj.type.name == "Texture2D":
            try:
                d = obj.read()
                name = getattr(d, 'm_Name', getattr(d, 'name', ''))
                if name:
                    p = os.path.join(out_dir, f"{name}.png")
                    d.image.save(p)
                    print(f"  Saved {p}")
            except Exception as e:
                print(f"  Warning: skipping SD texture {name}: {e}")
        elif obj.type.name == "Avatar":
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            p = os.path.join(out_dir, f"{name}.json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"avatar_name": name, "type": "Unity.Avatar", "form": model_name}, f, indent=2)
            print(f"  Saved {p}")

def extract_animations(start_chunk, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting 3D SD animations from chunk {start_chunk}...")
    bdata, end_c = read_bundle_range(DP_IDX, DP_CDB, start_chunk, max_chunks=70)
    env = UnityPy.load(bdata)
    count = 0
    for obj in env.objects:
        if obj.type.name == "AnimationClip":
            d = obj.read()
            name = getattr(d, 'm_Name', getattr(d, 'name', ''))
            if name:
                p = os.path.join(out_dir, f"{name}.anim")
                with open(p, "wb") as f:
                    f.write(obj.get_raw_data())
                count += 1
    print(f"  Saved {count} animation clips to {out_dir}")

def extract_ui_texture(chunk_id, out_dir, forced_name=None):
    os.makedirs(out_dir, exist_ok=True)
    bdata, _ = read_bundle_range(DP_IDX, DP_CDB, chunk_id, max_chunks=8)
    env = UnityPy.load(bdata)
    for obj in env.objects:
        if obj.type.name in ["Texture2D", "Sprite"]:
            d = obj.read()
            name = forced_name or getattr(d, 'm_Name', getattr(d, 'name', 'unknown'))
            if name:
                fname = name if name.endswith(".png") else f"{name}.png"
                p = os.path.join(out_dir, fname)
                try:
                    img = getattr(d, "image", None)
                    if img:
                        img.save(p)
                        print(f"  Saved UI texture {p} ({img.size})")
                        return p
                except Exception as e:
                    print(f"  Warning: failed to save UI texture {p}: {e}")

def extract_cutscene(start_chunk, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting Burst Cutscene Spine rig from core chunk {start_chunk}...")
    accum = bytearray()
    curr = start_chunk
    target_len = 7153760
    with open(CORE_IDX, "rb") as fi, open(CORE_CDB, "rb") as fc:
        while len(accum) < target_len:
            fi.seek(28 + curr * 28)
            rec = fi.read(28)
            off, clen = struct.unpack("<QI", rec[:12])
            fc.seek(off)
            accum.extend(dctx.decompress(fc.read(clen)))
            curr += 1

    data = bytes(accum[:target_len])
    reader = EndianBinaryReader(data)
    sig = reader.read_string_to_null()
    ver = reader.read_u_int()
    p_ver = reader.read_string_to_null()
    e_ver = reader.read_string_to_null()

    bf = BundleFile.__new__(BundleFile)
    File.__init__(bf, parent=None, name="c032_cutscene.bundle")
    bf.signature = sig
    bf.version = ver
    bf.version_player = p_ver
    bf.version_engine = e_ver

    m_DirectoryInfo, blocksReader = bf.read_fs(reader)
    node0 = m_DirectoryInfo[0]
    node1 = m_DirectoryInfo[1]

    blocksReader.Position = node0.offset
    raw_node0 = blocksReader.read(node0.size)

    # 1. Extract skel
    skel_idx = raw_node0.find(b"c032_00_skillcut.skel")
    if skel_idx != -1:
        # 21 bytes string name (aligned to 4 = 24 bytes), then 4 bytes size
        name_end = skel_idx + len("c032_00_skillcut.skel")
        align_pad = (4 - (len("c032_00_skillcut.skel") % 4)) % 4
        sz_pos = name_end + align_pad
        skel_size = struct.unpack("<I", raw_node0[sz_pos : sz_pos + 4])[0]
        skel_data = raw_node0[sz_pos + 4 : sz_pos + 4 + skel_size]
        p = os.path.join(out_dir, "c032_00_skillcut.skel")
        with open(p, "wb") as f:
            f.write(skel_data)
        print(f"  Saved {p} ({len(skel_data)} bytes)")

    # 2. Extract atlas
    atl_idx = raw_node0.find(b"c032_00_skillcut.atlas")
    if atl_idx != -1:
        name_end = atl_idx + len("c032_00_skillcut.atlas")
        align_pad = (4 - (len("c032_00_skillcut.atlas") % 4)) % 4
        sz_pos = name_end + align_pad
        atl_size = struct.unpack("<I", raw_node0[sz_pos : sz_pos + 4])[0]
        atl_data = raw_node0[sz_pos + 4 : sz_pos + 4 + atl_size]
        p = os.path.join(out_dir, "c032_00_skillcut.atlas")
        with open(p, "wb") as f:
            f.write(atl_data)
        print(f"  Saved {p} ({len(atl_data)} bytes)")

    # 3. Extract png from resS
    blocksReader.Position = node1.offset
    resS_bytes = blocksReader.read(node1.size)
    tex_offset = 0x219000
    tex_size = 0x400000
    width = 2048
    height = 2048
    bc7_data = resS_bytes[tex_offset : tex_offset + tex_size]
    raw_rgba = texture2ddecoder.decode_bc7(bc7_data, width, height)
    img = Image.frombytes("RGBA", (width, height), raw_rgba, "raw", "BGRA")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    p = os.path.join(out_dir, "c032_00_skillcut.png")
    img.save(p)
    print(f"  Saved {p} ({img.size})")

def extract_voice_audio(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting Japanese voice audio to {out_dir}...")
    nab1 = os.path.join(SAUS_JA_DIR, r"ab\830c7765ad8e784b146fd93e2a992febcaf56e30e6012c3033fe86571e5a710b.nab")
    if os.path.exists(nab1):
        env = UnityPy.load(nab1)
        cnt = 0
        for obj in env.objects:
            if obj.type.name == "AudioClip":
                d = obj.read()
                for fn, sdata in d.samples.items():
                    p = os.path.join(out_dir, fn)
                    with open(p, "wb") as f:
                        f.write(sdata)
                    cnt += 1
        print(f"  Extracted {cnt} voice clips from primary container")

    # Titlecall
    nab2 = os.path.join(SAUS_JA_DIR, r"ab\813b04cf4c3c97cfdcc8d9d0e699383ee37e8385797ff71a03b1e7e5a890328c.nab")
    if os.path.exists(nab2):
        env = UnityPy.load(nab2)
        for obj in env.objects:
            if obj.type.name == "AudioClip":
                d = obj.read()
                name = getattr(d, 'm_Name', getattr(d, 'name', ''))
                if "c032" in name:
                    for fn, sdata in d.samples.items():
                        p = os.path.join(out_dir, fn)
                        with open(p, "wb") as f:
                            f.write(sdata)
                        print(f"  Extracted titlecall {p}")

def extract_sfx_audio(start_chunk, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Extracting SFX & action audio from chunk {start_chunk} to {out_dir}...")
    bdata, _ = read_bundle_range(DP_IDX, DP_CDB, start_chunk, max_chunks=5)
    env = UnityPy.load(bdata)
    cnt = 0
    for obj in env.objects:
        if obj.type.name == "AudioClip":
            d = obj.read()
            for fn, sdata in d.samples.items():
                p = os.path.join(out_dir, fn)
                with open(p, "wb") as f:
                    f.write(sdata)
                cnt += 1
                print(f"  Saved SFX {p}")
    print(f"  Total SFX extracted: {cnt}")

def extract_dialogue_vault(out_file):
    import sqlite3
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    print(f"Extracting localized dialogue vault to {out_file}...")
    lss_files = [
        "Locale_NikkeEpisode.lss",
        "Locale_Counseling.lss",
        "Locale_SuddenMessage.lss",
        "Locale_SuddenStory.lss",
        "Locale_MainScenario.lss",
        "Locale_SubScenario.lss",
        "Locale_Character.lss",
        "Locale_Skill.lss"
    ]
    records = []
    for lss in lss_files:
        lp = os.path.join(LSS_DIR, lss)
        if not os.path.exists(lp):
            continue
        try:
            conn = sqlite3.connect(lp)
            cur = conn.cursor()
            cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
            tables = [t[0] for t in cur.fetchall()]
            for table in tables:
                cur.execute(f"PRAGMA table_info({table})")
                cols = [c[1] for c in cur.fetchall()]
                key_col = next((c for c in cols if 'key' in c.lower() or 'id' in c.lower()), cols[0])
                val_cols = [c for c in cols if c != key_col]
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                for r in rows:
                    row_dict = dict(zip(cols, r))
                    row_str = " ".join(str(v) for v in r)
                    # Check for Miranda references: c032 or 32 or ミランダ
                    if "c032" in row_str or "ミランダ" in row_str or (str(row_dict.get(key_col, "")).startswith("32_")):
                        records.append({
                            "source_file": lss,
                            "table": table,
                            "data": row_dict
                        })
            conn.close()
        except Exception as e:
            print(f"  Error reading {lss}: {e}")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"  Extracted {len(records)} localized dialogue entries into {out_file}")

def main():
    print("=== STARTING MIRANDA ASSET EXTRACTION (STAGE 2) ===")

    # 1. Spine Standing Puppets
    extract_spine_bundle(229195, os.path.join(ASSETS_DIR, "spine/standing/c032/00"), "c032_00")
    extract_spine_bundle(229245, os.path.join(ASSETS_DIR, "spine/standing/c032/01"), "c032_01")

    # 2. Spine Combat Puppets
    extract_spine_bundle(191079, os.path.join(ASSETS_DIR, "spine/combat/c032/00/aim"), "c032_aim_00")
    extract_spine_bundle(191114, os.path.join(ASSETS_DIR, "spine/combat/c032/00/cover"), "c032_cover_00")
    extract_spine_bundle(191161, os.path.join(ASSETS_DIR, "spine/combat/c032/01/aim"), "c032_aim_01")
    extract_spine_bundle(191210, os.path.join(ASSETS_DIR, "spine/combat/c032/01/cover"), "c032_cover_01")

    # 3. Spine Favorite Item Puppet
    extract_spine_bundle(226221, os.path.join(ASSETS_DIR, "spine/favoriteitem/c032/00"), "favoriteitem_c032_00")

    # 4. Favorite Item Interactive Scene
    extract_favoriteitem_scene(70672, os.path.join(ASSETS_DIR, "spine/favoriteitem_scene/c032"))

    # 5. 3D SD Chibi Models
    extract_sd_models(185211, os.path.join(ASSETS_DIR, "models/sd/c032_00"), "c032_00")
    extract_sd_models(185217, os.path.join(ASSETS_DIR, "models/sd/c032_01"), "c032_01")

    # 6. 3D SD Animations
    extract_animations(176957, os.path.join(ASSETS_DIR, "animations/c032"))

    # 7. Full Card Splash Illustrations
    fc_dir = os.path.join(ASSETS_DIR, "textures/full_cards")
    extract_ui_texture(77068, fc_dir, forced_name="c032_00.png")
    extract_ui_texture(77074, fc_dir, forced_name="c032_01.png")

    # 8. UI Portraits & Badges
    ui_dir = os.path.join(ASSETS_DIR, "textures/c032")
    extract_ui_texture(80908, ui_dir, forced_name="mi_c032_00_s.png")
    extract_ui_texture(80910, ui_dir, forced_name="mi_c032_01_s.png")
    extract_ui_texture(82155, ui_dir, forced_name="si_c032_00_s.png")
    extract_ui_texture(82159, ui_dir, forced_name="si_c032_01_s.png")
    extract_ui_texture(94437, ui_dir, forced_name="icn_skill_c032_ult.png")
    extract_ui_texture(88894, ui_dir, forced_name="fi_c032_00_badge.png")
    extract_ui_texture(91253, ui_dir, forced_name="fi_c032_00_icon.png")
    extract_ui_texture(89458, ui_dir, forced_name="fi_c032_00_subicon.png")

    # 9. Burst Cutscene
    extract_cutscene(232231, os.path.join(ASSETS_DIR, "cutscenes/c032"))

    # 10. Japanese Voice Bank
    extract_voice_audio(os.path.join(ASSETS_DIR, "audio/ja/c032"))

    # 11. Combat & Action AudioClips
    extract_sfx_audio(188178, os.path.join(ASSETS_DIR, "audio/sfx/c032"))

    # 12. Localized Dialogue Vault
    extract_dialogue_vault(os.path.join(ASSETS_DIR, "text/miranda_dialogue_vault.json"))

    print("\n=== MIRANDA ASSET EXTRACTION COMPLETE ===")

if __name__ == "__main__":
    main()
