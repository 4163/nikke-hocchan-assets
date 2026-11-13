# Maiden & Miranda (Goddess of Victory: NIKKE)

Extracted game assets, technical specifications, and interactive visual confirmation gallery for **Maiden** (`c181`, `c183`) and **Miranda** (`c032`) from **Goddess of Victory: NIKKE** (v153.6.10). Both characters share Japanese voice acting by Horie Yui (堀江由衣).

## Pipeline and reproduction

These assets were mapped, extracted, categorized, and documented deterministically using the structured asset extraction pipeline:
https://github.com/4163/i-asset-extraction

## Live preview

Interactive web gallery: https://4163.github.io/nikke-hocchan-assets

## Asset overview

| Category | File count | Formats | Directory |
|---|---|---|---|
| Audio (Japanese, Horie Yui) | 170 | `.wav` | `assets/audio/ja/` |
| Live2D Spine Rigs | 70 | `.skel`, `.atlas`, `.png`, `.obj` | `assets/spine/` |
| 3D Chibi Models and Weapons | 37 | `.obj`, `.png`, `.json` | `assets/models/sd/` |
| Chibi Action Animations | 91 | `.anim` | `assets/animations/` |
| Textures, Cards, and Portraits | 32 | `.png` | `assets/textures/` |
| Combat VFX Textures and Meshes | 24 | `.png`, `.obj` | `assets/vfx/` |
| Skill Cutscenes (Engine Rig) | 4 | `.skel`, `.atlas`, `.png` | `assets/cutscenes/` |
| Skill Cutscenes (Community Capture) | 4 | `.mp4`, `.png` | `assets/videos/` |
| Dialogue Vaults and SQLite Tables | 24 | `.json`, `.lss` | `assets/text/` |

Total verified assets on disk: **456 files** (291.50 MB).

## Technical specifications

- **Live2D Spine runtime:** All 20 skeletal animations use binary **Spine 4.1.20** with premultiplied alpha (`pma: true`) and 2048x2048 texture atlases.
- **Procedural aiming tracking:** Combat aim rigs bind procedural crosshair tracking across normalized coordinate axes `aim_x` (-1.0 to 1.0) and `aim_y` (-1.0 to 1.0).
- **3D chibi toon rim shading:** SD chibi models bind `SDToon_Tex_RimDefault.png` (256x2 RGBA LUT) as a 1D Fresnel look-up table ($u = 1.0 - \max(\vec{N} \cdot \vec{V}, 0.0)$, $v = 0.5$) for cel-shaded contours.
- **Audio voice scope:** Voice assets strictly cover Japanese voicelines voiced by Horie Yui (112 Maiden lines, 39 Miranda lines, and 19 action audio clips). English and Korean dubs are documented as out of scope.
- **Maiden burst cutscene delivery:** Maiden's animated burst cutscenes reside on Shift Up's remote Addressables CDN in the PC build. They are cataloged in [specs/on-demand-cdns.md](specs/on-demand-cdns.md) and supplemented with clean 1080p community video captures marked with third-party provenance.
- **Favorite item system:** Miranda includes a complete Favorite Item system with a dedicated 2D Spine puppet, a 13-asset Cinemachine interactive scene, and unique audio cues. Maiden has no Favorite Item in client Build 578825.
- **External community gallery audit:** Added notice card referencing `https://nikke-db.pages.dev/gallery` for supplemental community review.

Full technical blueprints, material bindings, and camera parameters are documented in [specs/visualization-spec.md](specs/visualization-spec.md).

## Tools and utilities used

| Tool | Role | Repository / Reference |
|---|---|---|
| REA | Reverse engineering framework, MCP server, archive inspection, and pipeline automation | [morluto/rea](https://github.com/morluto/rea) |
| Custom extraction tooling | Proprietary container decompression, Spine export, and gallery generation | [tools/](tools/) |
| UnityPy | Python Unity AssetBundle deserialization library | [K0lb3/UnityPy](https://github.com/K0lb3/UnityPy) |
| FFmpeg | Audio stream transcoding and video poster frame generation | [FFmpeg](https://ffmpeg.org/) |
| yt-dlp | Clean community video capture acquisition | [yt-dlp](https://github.com/yt-dlp/yt-dlp) |

## Disclaimer

All game assets and character content are property of SHIFT UP Corporation and Level Infinite. This repository is maintained strictly for archival, educational, and research purposes.
