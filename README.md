# Paper A: relational reasoning benchmark

Reproducibility materials for **evidence-conditioned relational identity reasoning** with seven answer-preserving evidence levels, B0–B6. The benchmark contains synthetic worlds, executable question definitions, exact model inputs, recorded responses, scoring data, and offline analysis programs.

This repository is public. Licensing is specified below. Tagged releases are archived on Zenodo; cite the version-specific DOI shown on the Zenodo record for the release you use.

## Download, restore, and verify

The release contains **14,221 restored files** (1,138,698,813 bytes). The compressed archive is 409,862,763 bytes, split into **20 parts**, each at most 20 MiB. A fresh-directory restoration and strict per-file hash verification passed before upload.

From release `v1.0.0` onward, the repository itself contains the complete bundle: all 20 `paper_a_data.tar.gz.partNNN` files and the 12 metadata, documentation, and verification files are at the repository root. Clone the repository, or download the **Source code (zip)** of a release or its Zenodo archive, and extract it into a new folder. The historical 32-file archive is also available as the asset **`paper-a-reproducibility-bundle-2026-11-06.zip`** on the [Releases page](https://github.com/ParkerTsai/paper-a-relational-reasoning-benchmark/releases/tag/data-2026-11-06). The asset is 424,221,101 bytes (SHA-256: `698c38c1bf8afcbb52374398357c278db57b19586c29fd783036459bbcd17593`).

The 20 parts in the repository are byte-identical to those in the `data-2026-11-06` release asset; their hashes are recorded in `archive_manifest.json`. `SHA256SUMS` is kept as issued with that asset, so its entry for `README.md` refers to the README inside the asset, not to this updated file.

Use Python 3.10 or newer. The following utilities use only the Python standard library:

```bash
python verify.py --parts
python restore.py --output restored
python verify.py --data restored --strict
```

If you also run `sha256sum -c SHA256SUMS`, the `README.md` entry reports FAILED because `SHA256SUMS` retains the checksum of the original release-asset README. Documentation-only updates to the repository README do not modify the archived data or code. The other checksum entries should report OK; use the archive and file manifests with `verify.py` for dataset integrity verification.

Run these commands from the folder containing this README and all 20 parts. `restore.py` joins the parts, verifies the combined archive, restores into an empty directory, and verifies every restored file. The parts are slices of one compressed archive; they are not individually extractable archives. Restoration uses temporary disk space for the joined archive as well as space for the restored files.

These utilities operate locally. They do not call a model API, install dependencies, or submit new experiments. `archive_manifest.json` records archive and part hashes; `file_manifest.json` records the SHA256 and size of every restored file. `SHA256SUMS` covers the bundle's delivery files other than itself.

## Run offline research checks

After restoration:

```bash
python -B restored/main/verify_inputs.py
python -B restored/analysis/reproduce.py --root restored --output-dir recomputed
```

The first command reconstructs and checks all 4,380 original complete request bodies without sending them. The second runs the portable pilot, common-100, Haiku-recovery, and length-receipt checks. Use a new output directory for each run. Both quick checks use Python standard-library code and included scoring modules.

The restored `analysis/README.md` documents optional full bootstrap and semantic-audit runs, historical outputs, and additional dependencies. These longer analyses are not invoked by the default quick check.

## Code information

Paths starting with `restored/` refer to files available after the archive has been restored.

| Location | Purpose |
|---|---|
| `verify.py`, `restore.py` (repository root) | Check the split archive, restore it, and validate restored files |
| `restored/main/science/scripts/world.py` | Seeded synthetic-world generator |
| `restored/main/science/scripts/questions.py` | Question sampler and SQL/Graph/Narrative renderers |
| `restored/main/science/scripts/oracle.py`, `tree_oracle.py`, `public_contract.py` | Independent answer oracles and public-world schema checks |
| `restored/main/science/scripts/build_new_worlds.py` | Rebuild the ten worlds, 200 questions, and fixed subsets from seeds |
| `restored/main/science/scripts/build_views_v2.py`, `exposure_original.py` | Construct the B0–B6 evidence views |
| `restored/main/science/scripts/build_naming_v2.py` | Construct the person-name and opaque-code naming variants |
| `restored/main/verify_inputs.py` | Reconstruct and verify the 4,380 recorded request bodies offline |
| `restored/results/main/evaluation_tools/` | Attempt selection, scoring, and outcome summaries |
| `restored/analysis/reproduce.py` | Recompute archived research checks; see `restored/analysis/README.md` for extended analyses |

## Regenerate the benchmark from seeds

The generator and recorded seeds can rebuild the synthetic worlds, questions, and evidence inputs. The build scripts do not overwrite existing outputs, so execute them from a new directory after restoration:

```bash
mkdir regen
cp -r restored/main/science/scripts regen/scripts
cd regen
python -B scripts/build_new_worlds.py
python -B scripts/build_views_v2.py
python -B scripts/build_naming_v2.py
cd ..
```

Compare the regenerated `regen/public/`, `regen/author/`, `regen/views_v2/`, and `regen/naming_v2/` with the corresponding directories under `restored/main/science/`. Worlds, questions, fixed subsets, and manifests can be checked byte-for-byte. For gzip-compressed message files, compare *decompressed contents*: the compressed bytes may differ across zlib versions even if the messages are identical. The two naming variants comprise 2,800 B0–B6 input versions; the original submitted message payloads are archived under `restored/main/payloads/`. The independent verification recorded on 20 November 2026 found identical regenerated contents. Padding inputs were separately replayed from archived filler counts; provider tokenization was not rerun.

## Requirements

- Python 3.10 or newer. Restoration, verification, input reconstruction, seed regeneration, and the quick research checks use the Python standard library.
- Extended statistical analyses require `numpy`, `pandas`, and `scipy`; plotting additionally uses `matplotlib`. See `restored/analysis/README.md` for commands and optional dependencies.
- After obtaining the public archive, local verification and analysis need neither a GPU, an API key, nor any model-service network calls. At least approximately 2.5 GB of disk space is needed for restoration alone; about 5 GB is recommended when also regenerating data and storing analysis outputs.
- An independent clean-environment check on Linux (kernel 6.18, 2 vCPU, 7 GB RAM) used Python 3.13.18, NumPy 2.5.3, pandas 3.0.5, and SciPy 1.18.1; this was the *reproduction* environment, not necessarily the original inference environment.

## Methodology

1. Ten 100-person synthetic worlds are generated from the recorded fixed seeds. The generated worlds are frozen before question selection.
2. Twenty questions per world (60 SQL, 70 Graph, and 70 Narrative in total) are selected and checked for a unique answer using independent oracle procedures.
3. Seven cumulative B0–B6 evidence views preserve each question's answer. Two naming variants yield 2,800 base input versions; the archived ten-world length controls add 180 padded input versions.
4. Model inference was performed in the original experiment, with documented retries. The archive retains attempts, selection decisions, and separate strict and deterministic format-recovered scoring channels.
5. The principal analyses can be recomputed offline using stored responses, without new model API requests. The archived analysis documentation identifies the relevant cohorts and extended commands.

Detailed definitions and experimental comparisons are provided in the accompanying manuscript.

## Citation

For use of the dataset and code, cite the *specific archived version* used. For `v1.0.0`: Tsai, M.-H. (2026). *Paper A: relational reasoning benchmark* (Version v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24216316. If citing a later documentation release, use that release's own version-specific Zenodo DOI instead.

Associated manuscript (currently submitted, not yet published): Tsai, M.-H. *A reproducible, answer-preserving benchmark for relational identity reasoning: accuracy, answer stability, and response coverage of large language models under controlled evidence conditions.* Manuscript submitted to PeerJ Computer Science.

## Dataset information (research scope)

| Component | Scope |
|---|---|
| Main benchmark | 10 P100 worlds; 200 questions: 60 SQL, 70 Graph, and 70 Narrative |
| Main evidence inputs | 2,800 B0–B6 configurations across two naming variants, plus 180 padding configurations; 2,980 unique message payloads |
| Complete historical main execution | 4,380 planned model cells, 5,008 recorded attempts, and separate first/selected scoring views |
| Common-question comparison | A fixed 100-question subset, evaluated over seven levels for three model conditions |
| Ten-world length control | 30 questions; 180 new padded requests plus reused baseline results |
| Fixed-world length pilot | A separate 30-question cohort; 180 new requests plus 180 baseline results |
| Semantic and oracle audit | Executable question/oracle checks and per-question/per-input audit evidence |
| P100 pilot | 34 selected questions; 476 sent configurations and responses |
| P500 pilot | 33 selected questions; 396 sent configurations, 400 attempts, and 66 blocked B6 configurations |

See [DATA_COVERAGE.md](DATA_COVERAGE.md) for the relationship between these scopes. The source files distinguish a *question*, a *payload*, a planned model *cell*, and a response *attempt*.

## Data and score channels

The original raw response contents and selected-attempt decisions are retained. Haiku strict parsing and deterministic JSON-fence recovery are separate channels. Recovery strips one complete JSON code fence where the recorded recovery rule applies; it does not change the question, evidence, answer, or attempt selection. Both strict and recovered outcomes remain available.

The two length-control cohorts use different questions. Their files and analyses are kept separate. P100 and P500 likewise contain different question sets. P500 B6 configurations marked blocked/NA have no invented responses.

## Provenance and curation

[PROVENANCE.json](PROVENANCE.json) identifies retrieved source archives by original filename, size, and SHA256. [CURATION.json](CURATION.json) records the derived release's retention, exclusions, and transformations. Account-balance records, internal authorization notes, temporary runtime snapshots, and unrelated experiments are excluded where documented. Scientific request parameters, sent messages, response attempts, scoring channels, selection rules, token usage, and retry/blocked evidence are retained.

The delivered archive is a newly assembled scientific package, so its hash differs from the original backup archive hashes. Exact benchmark payload preservation and request reconstruction are checked separately; see [VALIDATION.json](VALIDATION.json).

Some analysis programs and tables are historical research artifacts. New delivery and analysis verifiers are identified as such. Validation distinguishes checks rerun for this delivery from historical reports; it does not imply new model execution.

## Licensing

Copyright (c) 2026 Ming-Han Tsai.

Except where otherwise stated:

- Original project source code, including the world generator, query solvers, validation, scoring, analysis, plotting, restoration, and verification programs, is licensed under the [MIT License](LICENSE-MIT.txt).
- The synthetic datasets and associated documentation, including question definitions, evidence views, recorded model inputs and responses, scoring records, and result tables, are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-CC-BY-4.0.txt).

These licenses apply to the corresponding materials in this repository and in the existing `data-2026-11-06` release asset, `paper-a-reproducibility-bundle-2026-11-06.zip`, including files restored from its split archive. This notice supersedes earlier statements that a license had not yet been assigned. The existing release archive and its verification hashes are unchanged. Any separately identified third-party material remains subject to its original terms.

For CC BY 4.0 attribution, identify Ming-Han Tsai as the creator and cite this repository and the data version used; retain the license notice and indicate any changes. The complete license texts are provided in the two files linked above.

**Contributions.** This repository accompanies a manuscript submitted to PeerJ Computer Science. To report problems or propose corrections, please use GitHub Issues; existing archived release data and code are preserved.

除另有註明外，本研究的原創程式碼採 MIT License；合成資料集及相關說明文件採 CC BY 4.0。此授權亦涵蓋既有 `data-2026-11-06` Release 資料包內的相應內容，取代舊版「尚未指定授權」的說明。既有資料包與校驗碼維持原樣；另有標示的第三方內容仍依原授權。使用 CC BY 4.0 資料時，請註明作者蔡明翰（Ming-Han Tsai）、儲存庫及所用資料版本，保留授權聲明並標示修改。

## 中文操作說明

請到 [Releases 頁面](https://github.com/ParkerTsai/paper-a-relational-reasoning-benchmark/releases) 下載 **`paper-a-reproducibility-bundle-2026-11-06.zip`**，解壓至新資料夾。這個附件含完整 32 個交付檔案，其中包括全部 20 個資料分卷。自 `v1.0.0` 起，儲存庫本身（`main` 分支、各 Release 的 Source code 壓縮檔及其 Zenodo 存檔）也含完整 32 個交付檔案與全部 20 個資料分卷，其中 20 個資料分卷與上述附件逐位元組相同；README 等說明文件可能因版本更新而不同，請依指定版本使用。

在解壓後的資料夾依上方三個 Python 指令依序檢查、還原及逐檔驗證。資料分卷需要合併後解壓，請交由 `restore.py` 處理。還原與驗證不需要 API key，也不會呼叫付費模型。主要研究、共同 100 題、兩組長度控制與 P100／P500 先導研究的範圍，分別記錄於資料及分析目錄。若額外執行 `sha256sum -c SHA256SUMS`，因 README 已更新，`README.md` 一項會與原始封存版雜湊不符；其他項目與正式資料完整性請依前述驗證方式核對。
