import os
import json
import struct
from PIL import Image

template_path = r"E:\REA\.agents\skills\asset-extraction\resources\gallery-template.html"
gallery_dir = r"E:\REA\workspace\nikke-maiden\gallery"
assets_dir = r"E:\REA\workspace\nikke-maiden\assets"
os.makedirs(gallery_dir, exist_ok=True)

with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

core_categories = [
    ("textures/full_cards", "Full Character Card Splash Art"),
    ("textures/field_npc", "Field NPC Sprites (Maiden)"),
    ("textures/c181", "UI Portraits & Icons (Maiden)"),
    ("textures/c183", "UI Portraits & Icons (Maiden Ice Rose)"),
    ("textures/c032", "UI Portraits & Icons (Miranda)"),
    ("spine/combat/c181", "Live2D Spine Combat Atlas (Maiden)"),
    ("spine/combat/c183", "Live2D Spine Combat Atlas (Maiden Ice Rose)"),
    ("spine/combat/c032", "Live2D Spine Combat Atlas (Miranda)"),
    ("spine/standing/c181", "Live2D Spine Standing Atlas (Maiden)"),
    ("spine/standing/c183", "Live2D Spine Standing Atlas (Maiden Ice Rose)"),
    ("spine/standing/c032", "Live2D Spine Standing Atlas (Miranda)"),
    ("spine/favoriteitem_scene", "Favorite Item Scene Assets (Miranda)"),
    ("spine/favoriteitem", "Live2D Spine Favorite Item (Miranda)"),
    ("cutscenes/c181", "Skill Cutscenes (Maiden)"),
    ("cutscenes/c032", "Skill Cutscenes (Miranda)"),
    ("models/sd/c181", "3D SD Chibi & Weapon (Maiden)"),
    ("models/sd/c183", "3D SD Chibi & Weapon (Maiden Ice Rose)"),
    ("models/sd/c032", "3D SD Chibi & Weapon (Miranda)"),
    ("vfx", "Combat VFX Particle Textures"),
    ("textures/backgrounds", "Scenario Backgrounds"),
]

# 1. Visual Assets
visual_assets = []
for root, dirs, files in os.walk(assets_dir):
    for f in sorted(files):
        if f.lower().endswith(".png"):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, assets_dir).replace("\\", "/")
            disk_rel = f"assets/{rel_p}"

            cat = None
            for prefix, label in core_categories:
                if prefix in rel_p:
                    cat = label
                    break

            if not cat:
                continue

            if "_thumb.png" in f:
                continue

            mtime = os.path.getmtime(full_p)
            size = os.path.getsize(full_p)
            w, h = 0, 0
            try:
                with open(full_p, "rb") as fh:
                    w, h = struct.unpack(">II", fh.read(24)[16:24])
            except Exception:
                try:
                    with Image.open(full_p) as img:
                        w, h = img.size
                except Exception:
                    w, h = 0, 0

            visual_assets.append({
                "name": f,
                "category": cat,
                "url": f"../assets/{rel_p}?v={int(mtime)}",
                "relPath": disk_rel,
                "sizeBytes": size,
                "format": "PNG",
                "width": w,
                "height": h
            })

# Add Third-Party Community Video Captures
video_dir = os.path.join(assets_dir, "videos")
if os.path.exists(video_dir):
    for f in sorted(os.listdir(video_dir)):
        if f.lower().endswith(".mp4"):
            full_p = os.path.join(video_dir, f)
            rel_p = f"videos/{f}"
            disk_rel = f"assets/{rel_p}"
            thumb_name = f.replace(".mp4", "_thumb.png")
            thumb_p = os.path.join(video_dir, thumb_name)
            thumb_rel = f"videos/{thumb_name}"
            mtime = os.path.getmtime(full_p)
            size = os.path.getsize(full_p)

            w, h = (888, 1920) if "c181" in f else (1920, 1080)
            char_tag = "Maiden Base (c181)" if "c181" in f else "Maiden Ice Rose (c183)"

            visual_assets.append({
                "name": f"{char_tag} Burst Cutscene [Third-Party]",
                "category": "Skill Cutscenes (Third-Party Capture)",
                "url": f"../assets/{thumb_rel}?v={int(mtime)}",
                "videoUrl": f"../assets/{rel_p}?v={int(mtime)}",
                "relPath": disk_rel,
                "sizeBytes": size,
                "format": "MP4_VIDEO",
                "width": w,
                "height": h
            })

# 2. Models (Spine 2D Models + 3D SD Mesh Objs)
models = []
for root, dirs, files in os.walk(os.path.join(assets_dir, "spine")):
    for f in sorted(files):
        if f.lower().endswith((".skel", ".atlas")):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, assets_dir).replace("\\", "/")
            size = os.path.getsize(full_p)
            fmt = "SPINE_SKEL" if f.lower().endswith(".skel") else "SPINE_ATLAS"
            models.append({
                "name": f,
                "format": fmt,
                "sizeBytes": size,
                "relPath": f"assets/{rel_p}"
            })

for root, dirs, files in os.walk(os.path.join(assets_dir, "models")):
    for f in sorted(files):
        if f.lower().endswith(".obj"):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, assets_dir).replace("\\", "/")
            size = os.path.getsize(full_p)
            models.append({
                "name": f,
                "format": "OBJ_3D",
                "sizeBytes": size,
                "relPath": f"assets/{rel_p}"
            })

# Also include cutscenes .skel / .atlas
for root, dirs, files in os.walk(os.path.join(assets_dir, "cutscenes")):
    for f in sorted(files):
        if f.lower().endswith((".skel", ".atlas")):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, assets_dir).replace("\\", "/")
            size = os.path.getsize(full_p)
            fmt = "SPINE_SKEL" if f.lower().endswith(".skel") else "SPINE_ATLAS"
            models.append({
                "name": f,
                "format": fmt,
                "sizeBytes": size,
                "relPath": f"assets/{rel_p}"
            })

# 3. Audio Tracks
audio_tracks = []
for root, dirs, files in os.walk(os.path.join(assets_dir, "audio")):
    for f in sorted(files):
        if f.lower().endswith(".wav"):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, assets_dir).replace("\\", "/")
            url = f"../assets/{rel_p}"
            size = os.path.getsize(full_p)

            if "c032" in rel_p and "sfx" in rel_p:
                grp = "Combat & Action SFX (Miranda c032)"
            elif "sfx" in rel_p:
                grp = "Combat Sound FX (Maiden c183)"
            elif "c032" in rel_p:
                grp = "Miranda (c032) JA Voice (Horie Yui)"
            elif "c183" in rel_p:
                grp = "Ice Rose (c183) JA Voice (Horie Yui)"
            else:
                grp = "Base Maiden (c181) JA Voice (Horie Yui)"

            audio_tracks.append({
                "name": f,
                "group": grp,
                "playableUrl": url,
                "url": url,
                "relPath": f"assets/{rel_p}",
                "format": "WAV",
                "sizeBytes": size,
                "playable": True
            })

# 4. Animations
animations = []
for root, dirs, files in os.walk(os.path.join(assets_dir, "animations")):
    for f in sorted(files):
        if f.lower().endswith(".anim"):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, assets_dir).replace("\\", "/")
            size = os.path.getsize(full_p)
            animations.append({
                "name": f,
                "sizeBytes": size,
                "relPath": f"assets/{rel_p}"
            })

# Notices
notices = [
    {
        "title": "Consolidated Character Scope: Maiden & Miranda",
        "message": "All verified Maiden variants (c181 Base, c181_01 Nurse, c181_02 Swimsuit, c183 Ice Rose) and Miranda variants (c032 Base Uniform, c032_01 Cheerleader) are fully extracted and segregated on disk.",
        "type": "success"
    },
    {
        "title": "Voice Constraint Scope (Horie Yui / 堀江由衣)",
        "message": "Character voice is strictly restricted to Japanese audio voiced by Horie Yui (151 total WAV tracks: 112 Maiden, 39 Miranda). Non-Japanese tracks (English, Korean) and other client characters are excluded.",
        "type": "info"
    },
    {
        "title": "Favorite Item System (Miranda Exclusive)",
        "message": "Miranda features an active Favorite Item system with dedicated 2D Spine puppet, interactive Cinemachine Live2D scene (13 extracted assets), and 3 dedicated AudioClips. Maiden has no Favorite Item.",
        "type": "info"
    },
    {
        "title": "On-Demand CDN & Streaming Assets Cataloged",
        "message": "Historical event scenario backgrounds (43 bundles) and narrative audio packs (12 .nab containers) delivered on-demand via Shift Up CDNs are cataloged in specs/on-demand-cdns.md with reproducible recovery procedures.",
        "type": "info"
    },
    {
        "title": "Third-Party Community Burst Cutscene Captures Included",
        "message": "Maiden's animated burst cutscenes (c181 Base and c183 Ice Rose), which reside on Shift Up's remote Addressables CDN in the PC build, have been supplemented with clean 1080p community video captures and marked with third-party provenance.",
        "type": "warning"
    },
    {
        "badge": "External Audit",
        "title": "Community Gallery Manual Audit Required",
        "message": "External community gallery <a href=\"https://nikke-db.pages.dev/gallery\" target=\"_blank\" rel=\"noopener noreferrer\" style=\"color: var(--primary); text-decoration: underline; word-break: break-all;\">https://nikke-db.pages.dev/gallery</a> hosts additional Miranda and Maiden visual assets that require manual auditing and review.",
        "type": "warning"
    }
]

payload = {
    "projectName": "nikke-hocchan-assets",
    "projectTitle": "Goddess of Victory: NIKKE - Maiden & Miranda Consolidated Asset Extraction",
    "entityName": "Maiden (メイデン) & Miranda (ミランダ)",
    "faviconUrl": "../assets/textures/c181/si_c181_00_s.png",
    "repoUrl": "https://github.com/4163/nikke-hocchan-assets",
    "notices": notices,
    "visualAssets": visual_assets,
    "models": models,
    "audio": audio_tracks,
    "animations": animations
}

# Replace placeholders
html = template
html = html.replace("__PAYLOAD_PLACEHOLDER__", json.dumps(payload, ensure_ascii=False))
html = html.replace("{{PROJECT_TITLE}}", "Goddess of Victory: NIKKE - Maiden & Miranda Consolidated Asset Extraction")
html = html.replace("{{PROJECT_NAME}}", "nikke-hocchan-assets")
html = html.replace("{{ENTITY_NAME}}", "Maiden (メイデン) & Miranda (ミランダ)")
html = html.replace("{{SUBTITLE}}", "Consolidated Target-Mirrored Asset Extraction & Verification Gallery")
html = html.replace("{{FAVICON_URL}}", "../assets/textures/c181/si_c181_00_s.png")
html = html.replace("{{REPO_URL}}", "https://github.com/4163/nikke-hocchan-assets")

out_html_path = os.path.join(gallery_dir, "index.html")
with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Gallery successfully generated at: {out_html_path}")
print(f"  Visual Assets: {len(visual_assets)}")
print(f"  Models: {len(models)}")
print(f"  Audio Tracks: {len(audio_tracks)}")
print(f"  Animations: {len(animations)}")
