# Paper A: relational reasoning benchmark

Reproducibility materials for **evidence-conditioned relational identity reasoning** with seven answer-preserving evidence levels, B0–B6. The benchmark contains synthetic worlds, executable question definitions, exact model inputs, recorded responses, scoring data, and offline analysis programs.

This repository was created as a **private research repository** on 2026-11-06. A public license and archival DOI have not been assigned.

## Download, restore, and verify

Download the whole repository, including every `paper_a_data.tar.gz.partNNN` file. Use Python 3.10 or newer. The following utilities use only the Python standard library:

```bash
python verify.py --parts
python restore.py --output restored
python verify.py --data restored --strict
```

Run these commands from the directory containing this README. `restore.py` joins the parts, verifies the combined archive, restores into an empty directory, and verifies every restored file. The parts are slices of one compressed archive; they are not individually extractable archives. Restoration uses temporary disk space for the joined archive as well as space for the restored files.

These utilities operate locally. They do not call a model API, install dependencies, or submit new experiments. `archive_manifest.json` records archive and part hashes; `file_manifest.json` records the SHA256 and size of every restored file. `SHA256SUMS` covers the repository delivery files other than itself.

## Research scope

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

## 中文操作說明

請下載完整 repository，保留所有分卷檔，依上方三個 Python 指令依序檢查、還原及逐檔驗證。資料分卷需要合併後解壓，請交由 `restore.py` 處理。還原與驗證不需要 API key，也不會呼叫付費模型。主要研究、共同 100 題、兩組長度控制與 P100／P500 先導研究的範圍，分別記錄於資料及分析目錄。
