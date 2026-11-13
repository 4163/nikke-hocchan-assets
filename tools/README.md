# Proprietary and custom extraction tooling

This directory contains custom utilities and scripts created for extracting, decrypting, and parsing assets for **Maiden and Miranda** from **Goddess of Victory: NIKKE** (Build 578825).

## Tool inventory

| File | Language | Purpose | Upstream / Reference |
|---|---|---|---|
| [`extract_miranda.py`](extract_miranda.py) | Python | Extracts Miranda (`c032`) assets from Unity AssetBundle chunks, exports Spine 4.1.20 skeletons, and demuxes `.nab` audio chunks | Custom extraction protocol using [UnityPy](https://github.com/K0lb3/UnityPy) |
| [`catalog_ondemand_manifest.py`](catalog_ondemand_manifest.py) | Python | Parses `store.cdb` SQLite databases to catalog on-demand remote CDN addresses and hashes | NIKKE Addressables catalog parser |
| [`deploy_resolved_assets.py`](deploy_resolved_assets.py) | Python | Cleans raw alpha channels and deploys repaired textures to target directories | Custom Pillow post-processing |
| [`build_gallery.py`](build_gallery.py) | Python | Builds the standalone visual confirmation gallery HTML with static relative paths | Custom gallery generator |
| [`verify_stage_2.py`](verify_stage_2.py) | Python | Verifies extracted asset sizes, formats, and integrity against catalog manifests | Stage 2 verification suite |

## Usage and prerequisites

### Python environment
Install required Python libraries:
```bash
pip install UnityPy Pillow requests
```

### Rebuilding the visual gallery
```bash
python tools/build_gallery.py
```

### Verifying stage deliverables
```bash
python tools/verify_stage_2.py
```
