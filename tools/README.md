# Extraction tooling

This directory holds the extraction script for Miranda `c032` assets from Goddess of Victory: NIKKE Build 578825.

## Tool inventory

| File | Purpose | Upstream |
|---|---|---|
| [`extract_miranda.py`](extract_miranda.py) | Extracts Miranda `c032` Spine 4.1.20 puppets, Favorite Item scene textures, 3D SD models and animations, UI textures, `.nab` JA voice clips, SFX, and `.lss` dialogue | [UnityPy](https://github.com/K0lb3/UnityPy), `zstandard`, `texture2ddecoder`, `Pillow` |

## Prerequisites

```bash
pip install UnityPy Pillow zstandard texture2ddecoder
```

## Usage

```bash
python tools/extract_miranda.py --patch-dir <path-to-com.shiftup.patch> --lss-dir <path-to-StreamingAssets/lss> --saus-dir <path-to-saus/ja>
```

By default, extracted files are written to `assets/` at the repository root. Pass `--assets-dir` to override the output directory.
