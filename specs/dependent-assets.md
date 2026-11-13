# Dependent and Compound Asset Specification: Maiden & Miranda

Target: `Goddess of Victory: NIKKE` (PC Client Build 578825, Version 153.6.10)  
Entity: Maiden (`c181`, `c183`) and Miranda (`c032`)  
Pipeline Stage: Stage 3 (Asset Categorization)  
Workspace: `workspace/nikke-maiden/`

---

## Executive summary

Stage 3 partitions the 452 verified files on disk into two core architectural categories:
- **Category A: Standalone Assets (226 files, 202,152,864 bytes):** Media and datasets that operate independently without engine runtime dependencies (Audio, Standalone Textures & UI Badges, and Localized Dialogue Databases).
- **Category B: Dependent and Compound Clusters (226 files, 89,036,789 bytes):** Multi-file assemblies whose file roles, relative linkages, and internal bindings must remain anchored in their extracted paths to preserve runtime compatibility (Live2D Spine Puppets, 3D SD Chibi Rigs, Action Animations, VFX Assemblies, and Burst Cutscenes).

---

## Part 1: Pre-organization snapshot

The raw directory tree and physical file inventory as finalized at the Stage 2 checkpoint:

```text
assets/
├── animations/                 # 91 files (6,676,756 bytes)
│   ├── c032/                   # 30 action clips (.anim)
│   ├── c181/                   # 45 action clips (.anim)
│   └── c183/                   # 16 action clips (.anim)
├── audio/                      # 170 files (51,430,698 bytes)
│   ├── ja/                     # 151 Japanese voice clips (WAV)
│   │   ├── c032/               # 39 clips (38 voice + 1 titlecall)
│   │   ├── c181/               # 60 voice clips
│   │   └── c183/               # 52 voice clips
│   └── sfx/                    # 19 combat and action cues (WAV)
│       ├── c032/               # 12 cues (reload, actions, Favorite Item)
│       └── c183/               # 7 cues (reload, skill triggers)
├── cutscenes/                  # 4 files (3,221,777 bytes)
│   ├── c032/                   # 3 files (c032_00_skillcut.skel/atlas/png)
│   └── c181/                   # 1 file (EventScene_c181_cutscene_mi.png)
├── models/                     # 37 files (7,800,204 bytes)
│   └── sd/                     # 3D SD Chibi skeletal meshes, avatars, textures
│       ├── c032_00/            # 6 files (body/weapon OBJ, avatar, PNG)
│       ├── c032_01/            # 6 files (cheerleader body/weapon OBJ, avatar, PNG)
│       ├── c181_00/            # 6 files (base body/weapon OBJ, avatar, PNG)
│       ├── c181_01/            # 6 files (nurse body/weapon OBJ, avatar, PNG)
│       ├── c181_02/            # 6 files (summer body/weapon OBJ, avatar, PNG)
│       └── c183_00/            # 7 files (ice rose body/weapon/broom OBJ, avatar, PNG)
├── spine/                      # 70 files (68,819,528 bytes)
│   ├── combat/                 # 36 files (12 combat posture puppets: Aim & Cover)
│   │   ├── c032/               # 12 files (c032_00 and c032_01 Aim/Cover)
│   │   ├── c181/               # 18 files (c181_00, c181_01, c181_02 Aim/Cover)
│   │   └── c183/               # 6 files (c183_00 Aim/Cover)
│   ├── favoriteitem/           # 3 files (favoriteitem_c032_00 skel/atlas/png)
│   ├── favoriteitem_scene/     # 13 files (FavoriteItemScene_c032_00 rig, VFX, meshes)
│   └── standing/               # 18 files (6 standing puppets: skel/atlas/png)
│       ├── c032/               # 6 files (c032_00 and c032_01)
│       ├── c181/               # 9 files (c181_00, c181_01, c181_02)
│       └── c183/               # 3 files (c183_00)
├── text/                       # 24 files (144,199,456 bytes)
│   ├── *.lss                   # 22 localized SQLite database tables
│   ├── maiden_dialogue_vault.json  # 1,303 localized dialogue lines (EN, JA, KO, ZH-CN)
│   └── miranda_dialogue_vault.json # 1,212 localized dialogue lines (EN, JA, KO, ZH-CN)
├── textures/                   # 32 files (6,522,710 bytes)
│   ├── backgrounds/            # 2 event background cards (PNG)
│   ├── c032/                   # 6 UI badges and mini icons (PNG)
│   ├── c181/                   # 10 UI badges and mini icons (PNG)
│   ├── c183/                   # 3 UI badges and gacha banners (PNG)
│   ├── field_npc/              # 5 summer event NPC sprite sheets (PNG)
│   └── full_cards/             # 6 character splash illustration cards (PNG)
└── vfx/                        # 24 files (2,518,524 bytes)
    └── *.png, *.obj            # Combat skill particles, shockwaves, auramaps
```

---

## Part 2: Provenance ledger

The provenance ledger tracks standalone media files (Category A). These files function independently without runtime dependencies and are organized into standard asset directories (`audio/`, `textures/`, `text/`).

### 2.1 Graphics and illustrations (`assets/textures/`)

| Target file path | Original package / container source | Size (bytes) | SHA-256 hash | Role |
| :--- | :--- | :--- | :--- | :--- |
| `assets/textures/backgrounds/ui_event_bg_acpufreeze.png` | `dp/chunk/store.cdb (ScenarioBackgroundLocal)` | 349,459 | `9a4105648a1136ff...` | Standalone event background illustration |
| `assets/textures/backgrounds/ui_event_bg_phantomthiefvsdetective.png` | `dp/chunk/store.cdb (ScenarioBackgroundLocal)` | 406,367 | `60678169800469a3...` | Standalone event background illustration |
| `assets/textures/c032/fi_c032_00_badge.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 20,638 | `e2659ec069f3cbcd...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c032/icn_skill_c032_ult.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 4,049 | `f3961143534d76a3...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c032/mi_c032_00_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 231,127 | `35c4fe2f37e73e74...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c032/mi_c032_01_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 219,855 | `ab39238e776d77a4...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c032/si_c032_00_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 30,400 | `be5e25e0bc9250ff...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c032/si_c032_01_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 28,683 | `dfda70bdb35a0aa0...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/icn_skill_c181_ult.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 9,336 | `3a614b15b9c87712...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/mi_c181_00_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 230,118 | `d9a3d4a6a9211525...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/mi_c181_01_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 212,975 | `6ed88055168aa4db...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/mi_c181_02_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 196,895 | `936de35df1d536e9...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/si_c181_00_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 33,635 | `0f0c80c786631be3...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/si_c181_01_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 32,748 | `b0e85d6631670273...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c181/si_c181_02_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 31,242 | `0046a9f20ad1922c...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c183/ele_gacha_btn_c183_01.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 111,008 | `349a7e20194b811e...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c183/ele_gacha_btn_c183_02.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 91,406 | `9cd78d86be95e323...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c183/ele_gacha_title_c183_re.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 143,888 | `6b56925394a39c84...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c183/icn_skill_c183_ult.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 7,759 | `4acb29c450ae5ca8...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c183/mi_c183_00_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 239,017 | `07cc6eff70f813f5...` | UI badge, mini icon, or burst portrait |
| `assets/textures/c183/si_c183_00_s.png` | `dp/chunk/store.cdb (UIPortraitGroup)` | 38,996 | `8db0ae19928303c7...` | UI badge, mini icon, or burst portrait |
| `assets/textures/field_npc/SDToon_Tex_RimDefault.png` | `dp/chunk/store.cdb (FieldNPCGroup)` | 310 | `8b0404ce3382ac94...` | Summer event 2D field NPC sprite sheet |
| `assets/textures/field_npc/c181_02.png` | `dp/chunk/store.cdb (FieldNPCGroup)` | 272,029 | `b9048f4682b43e7f...` | Summer event 2D field NPC sprite sheet |
| `assets/textures/field_npc/febg_tropical_003_ani_01.png` | `dp/chunk/store.cdb (FieldNPCGroup)` | 964,489 | `f35fa4057bff2155...` | Summer event 2D field NPC sprite sheet |
| `assets/textures/field_npc/fx_fishing_spot_atlas.png` | `dp/chunk/store.cdb (FieldNPCGroup)` | 45,381 | `4a7b22dff1a9c019...` | Summer event 2D field NPC sprite sheet |
| `assets/textures/field_npc/fx_sb_fieldmap_flowmap_03.png` | `dp/chunk/store.cdb (FieldNPCGroup)` | 53,727 | `643998c68e52fdb1...` | Summer event 2D field NPC sprite sheet |
| `assets/textures/full_cards/c032_00.png` | `dp/chunk/store.cdb (FullCardSplashGroup)` | 304,414 | `fe871b053fdaf43d...` | Full character card vertical splash illustration (1024x1024) |
| `assets/textures/full_cards/c032_01.png` | `dp/chunk/store.cdb (FullCardSplashGroup)` | 327,220 | `8923c9b556d21329...` | Full character card vertical splash illustration (1024x1024) |
| `assets/textures/full_cards/c181_00_full.png` | `dp/chunk/store.cdb (FullCardSplashGroup)` | 521,025 | `5b72acbc3d3c15b4...` | Full character card vertical splash illustration (1024x1024) |
| `assets/textures/full_cards/c181_01_full.png` | `dp/chunk/store.cdb (FullCardSplashGroup)` | 550,875 | `6fa9a979a1523562...` | Full character card vertical splash illustration (1024x1024) |
| `assets/textures/full_cards/c181_02_full.png` | `dp/chunk/store.cdb (FullCardSplashGroup)` | 431,308 | `0402374c40a5dfe5...` | Full character card vertical splash illustration (1024x1024) |
| `assets/textures/full_cards/c183_00_full.png` | `dp/chunk/store.cdb (FullCardSplashGroup)` | 382,331 | `34dc4a347deac554...` | Full character card vertical splash illustration (1024x1024) |

### 2.2 Localized text and dialogue vaults (`assets/text/`)

| Target file path | Original package / container source | Size (bytes) | SHA-256 hash | Role |
| :--- | :--- | :--- | :--- | :--- |
| `assets/text/CharacterSearchTable_en.lss` | `StreamingAssets/lss (Client localized database)` | 8,192 | `0d3e1c53e2c9ce57...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/CharacterSearchTable_ja.lss` | `StreamingAssets/lss (Client localized database)` | 16,384 | `c2af99e29f3f6883...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/CharacterSearchTable_ko.lss` | `StreamingAssets/lss (Client localized database)` | 16,384 | `c0a4fb229e3b2e3c...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/CharacterSearchTable_zh-CN.lss` | `StreamingAssets/lss (Client localized database)` | 8,192 | `21f0768bf5cd3275...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/CharacterSearchTable_zh-TW.lss` | `StreamingAssets/lss (Client localized database)` | 8,192 | `7a89359a8eee823f...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_Character.lss` | `StreamingAssets/lss (Client localized database)` | 4,902,912 | `a6670e869a031aeb...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_CharacterCostume.lss` | `StreamingAssets/lss (Client localized database)` | 90,112 | `abb8b1578ccee590...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_Counseling.lss` | `StreamingAssets/lss (Client localized database)` | 13,209,600 | `d07774629266fa2c...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_Event.lss` | `StreamingAssets/lss (Client localized database)` | 2,375,680 | `9dcff1648dd68115...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_MainScenario.lss` | `StreamingAssets/lss (Client localized database)` | 23,810,048 | `bdc8c56dbdbd9dd2...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_NikkeEpisode.lss` | `StreamingAssets/lss (Client localized database)` | 31,993,856 | `a30deb569c714ad6...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_Skill.lss` | `StreamingAssets/lss (Client localized database)` | 2,863,104 | `a4f04cd98e6d47da...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_SubScenario.lss` | `StreamingAssets/lss (Client localized database)` | 34,787,328 | `a524770a6524ab7b...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_SuddenMessage.lss` | `StreamingAssets/lss (Client localized database)` | 10,698,752 | `fdaf9c4297c44e97...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/Locale_SuddenStory.lss` | `StreamingAssets/lss (Client localized database)` | 10,100,736 | `4f0679f2459de753...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/blabla_messages.json` | `Compiled from localized .lss database tables` | 96,313 | `addc398de402f689...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |
| `assets/text/bond_episodes.json` | `Compiled from localized .lss database tables` | 257,424 | `f5c06185a02f0f22...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |
| `assets/text/brief_encounters.json` | `Compiled from localized .lss database tables` | 10,872 | `36e5013567688124...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |
| `assets/text/campaign_scenarios.json` | `Compiled from localized .lss database tables` | 5,341 | `ea0a03cee03e970c...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |
| `assets/text/counseling_diary.json` | `Compiled from localized .lss database tables` | 102,741 | `6864905b4b37753c...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |
| `assets/text/event_240425.lss` | `StreamingAssets/lss (Client localized database)` | 5,173,248 | `ae4ee3d219248ffb...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/event_240704.lss` | `StreamingAssets/lss (Client localized database)` | 3,158,016 | `69e384fef69205c0...` | Raw encrypted/compressed SQLite dialogue table |
| `assets/text/event_cameos.json` | `Compiled from localized .lss database tables` | 152,689 | `9b302e487980e045...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |
| `assets/text/miranda_dialogue_vault.json` | `Compiled from localized .lss database tables` | 353,340 | `84280d5f640e158b...` | Consolidated multi-language character dialogue vault (EN, JA, KO, ZH-CN) |

### 2.3 Audio voice bank and sound effects (`assets/audio/`)

170 isolated AudioClips extracted from official `.nab` archives and chunk containers:

- **Maiden Japanese voice bank:** 112 tracks (`assets/audio/ja/c181/` [60 tracks], `assets/audio/ja/c183/` [52 tracks]) from containers `62f4f4f0...nab` and `8ba38437...nab`.
- **Miranda Japanese voice bank:** 39 tracks (`assets/audio/ja/c032/` [38 voice tracks + 1 titlecall]) from containers `830c7765...nab`, `50aa2059...nab`, and `813b04cf...nab`.
- **Combat and action SFX:** 19 cues (`assets/audio/sfx/c183/` [7 cues], `assets/audio/sfx/c032/` [12 cues]) deserialized from patch Chunk 188178.

| Subdirectory | Track count | Total size (bytes) | Source container | Codec & Sample rate |
| :--- | :--- | :--- | :--- | :--- |
| `assets/audio/ja/c181/` | 60 | 17,998,348 | `ab/62f4f4f0...nab` | PCM WAV / 44.1 kHz 16-bit mono |
| `assets/audio/ja/c183/` | 52 | 16,842,510 | `ab/62f4f4f0...nab`, `ab/8ba3...nab` | PCM WAV / 44.1 kHz 16-bit mono |
| `assets/audio/ja/c032/` | 39 | 11,852,708 | `ab/830c7765...nab`, `ab/50aa...nab` | PCM WAV / 44.1 kHz 16-bit mono |
| `assets/audio/sfx/c183/` | 7 | 2,148,820 | Chunk 188178 (`core/chunk/store.cdb`) | PCM WAV / 44.1 kHz 16-bit stereo |
| `assets/audio/sfx/c032/` | 12 | 2,588,312 | Chunk 188178 (`core/chunk/store.cdb`) | PCM WAV / 44.1 kHz 16-bit stereo |

---

## Part 3: Compound clusters

Compound clusters (Category B) consist of multi-file assemblies where files have direct runtime dependencies on one another. Their relative paths within their subdirectories are preserved to maintain internal reference integrity.

### 3.1 Live2D Spine standing puppets (6 clusters)

Each standing puppet cluster requires a three-file triad: binary skeleton (`.skel`), atlas layout (`.atlas`), and texture page (`.png`).

| Cluster identifier | Preserved relative path | Constituent files | Runtime dependencies |
| :--- | :--- | :--- | :--- |
| **Maiden Base (`c181_00`)** | `assets/spine/standing/c181/00/` | `c181_00.skel`, `c181_00.atlas`, `c181_00.png` | Spine Web Player / Spine-Pixi 4.1 |
| **Maiden Covert Nurse (`c181_01`)** | `assets/spine/standing/c181/01/` | `c181_01.skel`, `c181_01.atlas`, `c181_01.png` | Spine Web Player / Spine-Pixi 4.1 |
| **Maiden Under The Sun (`c181_02`)** | `assets/spine/standing/c181/02/` | `c181_02.skel`, `c181_02.atlas`, `c181_02.png` | Spine Web Player / Spine-Pixi 4.1 |
| **Maiden Ice Rose (`c183_00`)** | `assets/spine/standing/c183/00/` | `c183_00.skel`, `c183_00.atlas`, `c183_00.png` | Spine Web Player / Spine-Pixi 4.1 |
| **Miranda Base (`c032_00`)** | `assets/spine/standing/c032/00/` | `c032_00.skel`, `c032_00.atlas`, `c032_00.png` | Spine Web Player / Spine-Pixi 4.1 |
| **Miranda Cheerleader (`c032_01`)** | `assets/spine/standing/c032/01/` | `c032_01.skel`, `c032_01.atlas`, `c032_01.png` | Spine Web Player / Spine-Pixi 4.1 |

### 3.2 Live2D Spine combat puppets (12 clusters)

Combat models split into discrete Aim and Cover posture puppets per costume:

| Entity & Costume | Aim posture cluster | Cover posture cluster | Runtime format |
| :--- | :--- | :--- | :--- |
| **Maiden Base (`c181_00`)** | `assets/spine/combat/c181/00/aim/` (3 files) | `assets/spine/combat/c181/00/cover/` (3 files) | Spine 4.1 binary |
| **Maiden Nurse (`c181_01`)** | `assets/spine/combat/c181/01/aim/` (3 files) | `assets/spine/combat/c181/01/cover/` (3 files) | Spine 4.1 binary |
| **Maiden Summer (`c181_02`)** | `assets/spine/combat/c181/02/aim/` (3 files) | `assets/spine/combat/c181/02/cover/` (3 files) | Spine 4.1 binary |
| **Maiden Ice Rose (`c183_00`)** | `assets/spine/combat/c183/00/aim/` (3 files) | `assets/spine/combat/c183/00/cover/` (3 files) | Spine 4.1 binary |
| **Miranda Base (`c032_00`)** | `assets/spine/combat/c032/00/aim/` (3 files) | `assets/spine/combat/c032/00/cover/` (3 files) | Spine 4.1 binary |
| **Miranda Cheerleader (`c032_01`)** | `assets/spine/combat/c032/01/aim/` (3 files) | `assets/spine/combat/c032/01/cover/` (3 files) | Spine 4.1 binary |

### 3.3 Miranda Favorite Item system clusters (2 clusters)

The Favorite Item system is a compound multi-component architecture exclusive to Miranda in this scope:

1. **Favorite Item Spine Puppet (`favoriteitem_c032_00`):**
   - Location: `assets/spine/favoriteitem/c032/00/`
   - Files: `favoriteitem_c032_00.skel` (18,171 bytes), `favoriteitem_c032_00.atlas` (1,061 bytes), `favoriteitem_c032_00.png` (2,146,804 bytes)
   - Role: Interactive desktop puppet rendered during bond inspection.

2. **Interactive Cinemachine Scene (`FavoriteItemScene_c032_00`):**
   - Location: `assets/spine/favoriteitem_scene/c032/`
   - Spine Rig: `FavoriteItemScene_c032_00.skel` (24,115 bytes), `FavoriteItemScene_c032_00.atlas` (842 bytes), `FavoriteItemScene_c032_00.png` (2,947,192 bytes, 2048x2048)
   - 3D Mesh Geometry: `fx_fbx_cylinder_12.obj` (3D projection cylinder)
   - VFX Particle Textures: `fx_gra_02.png`, `FavoriteItem_bg_solid.png`, `fx_jh_pattern_01_color.png`, `fx_pattern_03_blur.png`, `fx_npc_c5010_summer_item_gun_atlas_dis.png`, `fx_c032_FavoriteItemScene_uv.png`, `fx_c032_FavoriteItemScene_uv1.png`, `fx_nimph_light_01.png`, `fx_c032_FavoriteItemScene_atlas.png`
   - Role: Cinemachine camera virtual set with animated light glows and interactive touch points.

### 3.4 3D SD chibi character and weapon skeletal rigs (6 clusters)

Each 3D SD model cluster binds skinned character geometry, weapon geometry, bone avatar hierarchy, diffuse BC7 textures, and shared toon rim ramp:

| Model cluster | Character mesh | Weapon mesh | Avatar structure | Textures & Materials |
| :--- | :--- | :--- | :--- | :--- |
| **Maiden Base (`c181_00`)** | `c181_00_skin.obj` | `c181_00_weapon_skin.obj` | `c181_00Avatar.json` (84 joints) | `c181_00.png`, `c181_00_weapon.png`, `SDToon_Tex_RimDefault.png` |
| **Maiden Nurse (`c181_01`)** | `c181_01_skin.obj` | `c181_01_weapon_skin.obj` | `c181_01Avatar.json` (84 joints) | `c181_01.png`, `c181_00_weapon.png`, `SDToon_Tex_RimDefault.png` |
| **Maiden Summer (`c181_02`)** | `c181_02_skin.obj` | `c181_02_weapon_skin.obj` | `c181_02Avatar.json` (84 joints) | `c181_02.png`, `c181_02_weapon.png`, `SDToon_Tex_RimDefault.png` |
| **Maiden Ice Rose (`c183_00`)** | `c183_00_skin.obj` | `c183_00_weapon_skin.obj` (+ broom) | `c183_00Avatar.json` (84 joints) | `c183_00.png`, `c183_00_weapon.png`, `SDToon_Tex_RimDefault.png` |
| **Miranda Base (`c032_00`)** | `c032_00_skin.obj` | `c032_00_weapon_skin.obj` | `c032_00Avatar.json` (78 joints) | `c032_00.png`, `c032_00_weapon.png`, `SDToon_Tex_RimDefault.png` |
| **Miranda Cheerleader (`c032_01`)** | `c032_01_skin.obj` | `c032_01_weapon_skin.obj` | `c032_01Avatar.json` (78 joints) | `c032_01.png`, `c032_01_weapon.png`, `SDToon_Tex_RimDefault.png` |

### 3.5 3D SD action animation sets (3 clusters)

91 Unity `.anim` curve files deserialized across standard tactical states:

- `assets/animations/c181/`: 45 clips covering idle, walk, run, cover, aim, fire, reload, hit, die, and talk across all 3 Maiden costumes.
- `assets/animations/c183/`: 16 clips covering Ice Rose unique animations (rocket launcher posture, heavy stance, broom riding).
- `assets/animations/c032/`: 30 clips covering Miranda base and cheerleader postures (15 clips each for `c032_00` and `c032_01`).

### 3.6 Burst cutscenes (2 on-disk clusters + third-party captures)

| Cutscene cluster | Preserved path | Constituent files | Presentation type |
| :--- | :--- | :--- | :--- |
| **Maiden Event Scene (`c181`)** | `assets/cutscenes/c181/` | `EventScene_c181_cutscene_mi.png` (256x512) | Live wallpaper scene thumbnail; full animation bundles resolved on-demand via CDN |
| **Miranda Live Cutscene (`c032_00`)** | `assets/cutscenes/c032/` | `c032_00_skillcut.skel`, `c032_00_skillcut.atlas`, `c032_00_skillcut.png` (2048x2048) | Animated 2D Spine cutscene with dynamic eye motion and police siren effects |
| **Maiden Base Community Burst Video** | `assets/videos/` | `c181_00_burst_cutscene_community.mp4`, `..._thumb.png` | Clean community 1080p vertical video capture (third-party provenance) |
| **Maiden Ice Rose Community Burst Video** | `assets/videos/` | `c183_00_burst_cutscene_community.mp4`, `..._thumb.png` | Clean community 1080p60 video capture (third-party provenance) |

### 3.7 Combat VFX particle systems (Maiden exclusive, 24 files)

Located in `assets/vfx/`. Contains 21 high-definition texture atlases (`.png`) and 3 mesh geometries (`.obj`) driving Maiden's electric aura, hit sparks, shockwaves, and Ice Rose ice crystal shaders.

---

## Part 4: Dual-use items and transform-dependent standalones

### 4.1 Dual-use items

Assets categorized under standalone directories that are also referenced by compound runtime assemblies:
- `assets/textures/c032/fi_c032_00_badge.png`: Functions independently as a UI badge; referenced inside the Favorite Item interactive scene UI trigger.
- `assets/textures/c032/icn_skill_c032_ult.png`: Functions as a burst skill icon; referenced as the trigger thumbnail for the live cutscene playback.
- `assets/models/sd/c032_00/SDToon_Tex_RimDefault.png`: Stored with `c032_00`; shared as the universal toon rim ramp across `c032_01` and Maiden's chibi models.

### 4.2 Transform-dependent standalones

Media files requiring coordinate, aspect ratio, or camera transforms during rendering:
- **Burst Cutscene Canvas (`c032_00_skillcut.png`):** 2048x2048 square canvas. In original engine presentation, this is letterboxed/pillarboxed with a dynamic 16:9 viewport crop and high-speed diagonal zoom punch.
- **Favorite Item Scene Canvas (`FavoriteItemScene_c032_00.png`):** 2048x2048 canvas. Displayed via Cinemachine 2D virtual camera with parallax pan constrained to normalized horizontal coordinates `[-0.25, 0.25]`.
- **Full Character Cards (`assets/textures/full_cards/*.png`):** 1024x1024 power-of-two textures. Character artwork is centered horizontally and anchored to the lower margin, designed with a linear vertical alpha falloff for card framing.

