import os
import shutil
import struct
import zstandard as zstd
from PIL import Image
import texture2ddecoder
import numpy as np
from UnityPy.streams import EndianBinaryReader
from UnityPy.files import BundleFile, File

WORKSPACE = r"E:\REA\workspace\nikke-maiden"
FAV_DIR = os.path.join(WORKSPACE, "assets", "spine", "favoriteitem_scene", "c032")
CUT_DIR = os.path.join(WORKSPACE, "assets", "cutscenes", "c032")

DP_IDX = r"D:\Games\NIKKE\Unity\com_proximabeta_NIKKE\com.shiftup.patch\dp\chunk\store.cdb.idx"
DP_CDB = r"D:\Games\NIKKE\Unity\com_proximabeta_NIKKE\com.shiftup.patch\dp\chunk\store.cdb"
dctx = zstd.ZstdDecompressor()

def get_chunk(c):
    with open(DP_IDX, 'rb') as fi, open(DP_CDB, 'rb') as fc:
        fi.seek(28 + c * 28)
        off, clen, md5 = struct.unpack('<QI16s', fi.read(28))
        fc.seek(off)
        return dctx.decompress(fc.read(clen))

print("=== 1. Deploying c032_00_skillcut.png ===")
clean_skillcut = os.path.join(CUT_DIR, "test_140194_rgba.png")
target_skillcut = os.path.join(CUT_DIR, "c032_00_skillcut.png")
shutil.copyfile(clean_skillcut, target_skillcut)
print(f"Copied {clean_skillcut} -> {target_skillcut}")

print("\n=== 2. Reconstructing Bundle 70672 .resS stream ===")
accum = bytearray()
for c in range(70672, 70688): accum.extend(get_chunk(c))
accum.extend(get_chunk(70666))
accum.extend(get_chunk(70688))
accum.extend(get_chunk(70668))
for c in range(70689, 70742): accum.extend(get_chunk(c))

reader = EndianBinaryReader(bytes(accum))
sig = reader.read_string_to_null()
ver = reader.read_u_int()
p_ver = reader.read_string_to_null()
e_ver = reader.read_string_to_null()
bf = BundleFile.__new__(BundleFile)
File.__init__(bf, parent=None, name="FavoriteItemScene_c032_00.bundle")
bf.signature = sig
bf.version = ver
bf.version_player = p_ver
bf.version_engine = e_ver

m_DirectoryInfo, blocksReader = bf.read_fs(reader)
node1 = m_DirectoryInfo[1]
blocksReader.Position = node1.offset
resS = blocksReader.read(node1.size)
print(f"Reconstructed .resS size: {len(resS)} bytes")

# Extract and save all Favorite Item Scene textures
targets = [
    # (name, offset, size, w, h, fmt)
    ("fx_c032_FavoriteItemScene_uv.png", 0, 8192, 128, 128, "dxt1"),
    ("fx_gra_02.png", 8192, 65536, 256, 256, "bc7"),
    ("FavoriteItem_bg_solid.png", 73728, 4096, 64, 64, "bc7"),
    ("fx_jh_pattern_01_color.png", 77824, 65536, 256, 256, "dxt5"),
    ("fx_pattern_03_blur.png", 143360, 65536, 256, 256, "bc7"),
    ("fx_npc_c5010_summer_item_gun_atlas_dis.png", 208896, 16384, 128, 128, "bc7"),
    ("fx_c032_FavoriteItemScene_uv1.png", 230768, 16384, 128, 128, "dxt5"),
    ("fx_nimph_light_01.png", 247152, 262144, 512, 512, "bc7"),
    ("fx_c032_FavoriteItemScene_atlas.png", 574832, 262144, 512, 512, "bc7"),
    ("FavoriteItemScene_c032_00.png", 836976, 4194304, 2048, 2048, "bc7")
]

print("\n=== 3. Extracting and saving FavoriteItemScene textures ===")
for fn, off, sz, w, h, fmt in targets:
    raw = resS[off : off + sz]
    if fmt == "bc7":
        rgba = texture2ddecoder.decode_bc7(raw, w, h)
    elif fmt == "dxt5":
        rgba = texture2ddecoder.decode_bc3(raw, w, h)
    elif fmt == "dxt1":
        rgba = texture2ddecoder.decode_bc1(raw, w, h)
    
    img = Image.frombytes("RGBA", (w, h), rgba, "raw", "RGBA").transpose(Image.FLIP_TOP_BOTTOM)
    out_path = os.path.join(FAV_DIR, fn)
    img.save(out_path)
    
    arr = np.array(img, dtype=np.float32)
    diff = np.mean(np.abs(arr[1:] - arr[:-1]))
    print(f"  Saved {fn:44s} ({w:4d}x{h:<4d}) | Mean row diff: {diff:5.2f}")

print("\n=== 4. Cleaning up scratch/test files in assets/ ===")
for d in [FAV_DIR, CUT_DIR, WORKSPACE]:
    for fn in os.listdir(d):
        if fn.startswith("test_") and fn.endswith(".png"):
            fp = os.path.join(d, fn)
            try:
                os.remove(fp)
                print(f"  Removed scratch file: {fn}")
            except Exception as e:
                print(f"  Could not remove {fn}: {e}")

print("\nAll target assets resolved and deployed successfully!")
