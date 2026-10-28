# FHD_SpaceBG — configuration review sources (artwork missing)

Пакет исходников только для двух файлов присланного архива. Конфигурация и ModuleInfo пересобираются побайтово точно. **Полного мода здесь нет: все 33 GAI-фона, на которые ссылается CacheData, отсутствуют в исходном архиве. Папка дополнительных фонов DATA/FON также не прислана.**

## Included source and actual scope

The uploaded `FHD_SpaceBG(1).rar` contains only:

- `CFG/CacheData.dat` — 299 bytes.
- `ModuleInfo.txt` — 4,230 bytes.

The archive is RAR5, 2,177 bytes, SHA-256 `d7bde3ee4ebd20b55872e34961ef5102ddb68ace1ed114589af449d01924531f`. Original metadata credits **Prolog_D**.

`source/CacheData.json` is a complete editable representation of the decoded configuration. `source/ModuleInfo.txt` is UTF-8 source, automatically rebuilt with the original UTF-16LE BOM and original line endings. Both original output hashes are recorded in `original-file-sha256.json`. No prebuilt DAT or opaque compressed config blob is needed to build them.

No main config, language DAT, DLL, SCR or image was supplied. No RSON project is needed for these two data files. There is no extra material to remove from the input; the added files are source, build/verification tooling and reports. The repository stays below 100 files.

## Resource completeness

The CacheData contains **33** `Bm.BGO` mappings to `DATA/BGObj/*.gai`:

`bg00`–`bg15`, `bg50`–`bg55`, `bg70`–`bg72`, `bg79`–`bg86`.

Every target is absent from this upload. The metadata describes 25 new backgrounds and 74 additional choices in `DATA/FON`; those description counts do not establish which artwork files exist, and the description was not changed to match the 33 mappings.

The report lists each missing filename. The original metadata also contains both `Conflict=SkyBG,PolarLights` and a later empty `Conflict=` line, and repeated language fields. They are preserved without guessing how a particular loader resolves them. Priority remains 99.

Previously saved Animated 0.1 TEST material is a separate, modified animated overlay. It is not used as a replacement for the missing original static artwork. No blank, vanilla or generated background was substituted.

## Automatic reconstruction

Python 3.12 and its standard library are sufficient:

```sh
python3 tests/verify.py --report build-verification.json
python3 build.py --verify-original
```

The output `dist/FHD_SpaceBG-CONFIG-ONLY.zip` contains exactly the two uploaded mod files below `Mods/FHD_MODS/FHD_SpaceBG/`. It is explicitly **config-only**, not a complete installable graphics mod. `dist/resource-audit.json` lists the missing resources. GitHub Actions publishes only that config-only artifact and the verification/audit reports.

For reviewers who require a complete resource set, `python3 build.py --verify-original --require-resources` deliberately refuses this incomplete package. The workflow's successful reconstruction job does not mean resource completeness passed.

`build-verification.json` records seven passing reconstruction/audit checks. Both SHA-256 hashes match the upload; DAT checksum, decompression and complete parse/encode pass; UTF-16 metadata is preserved; all 33 missing paths are reported; and the full-resource gate correctly blocks. No game or image-editor execution was performed. zlib 1.3.2 / Python 3.12.14 was used; compressed DAT bytes can vary across zlib implementations.

## What is needed for the full mod

The original `DATA/BGObj` resource files and the described `DATA/FON` folder are needed to prepare and verify the complete artwork package. They cannot be recovered from the two supplied config/metadata files. This repository does not present the absence as a successful full-mod build or imply Nexus approval.

The DAT codec reimplements the format used by Sergei Osminin's MIT-licensed rangers-utils. This packaging does not assign a new license to the original mod; no original license file was supplied.
