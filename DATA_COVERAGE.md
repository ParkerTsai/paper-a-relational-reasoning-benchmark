# Data coverage and interpretation

## Main benchmark and execution archive

The main benchmark has 200 unique questions over ten independent P100 synthetic worlds. The 60 SQL, 70 Graph, and 70 Narrative questions are expanded into seven evidence conditions and two naming variants, giving 2,800 basic input configurations. Another 180 padding configurations give 2,980 unique message payloads.

The full historical execution plan contains 4,380 model cells: 2,980 Luna-low cells, 700 Luna-high cells, and 700 Haiku-medium cells. Retries and provider outcomes yield 5,008 recorded attempts. First and selected scoring views contain 8,760 rows together. These quantities describe different units and should not be substituted for one another.

The manuscript's narrower accounting uses 2,890 response cells, or 3,070 with the additional code-naming appendix rows. The release preserves the larger underlying execution evidence rather than discarding cells outside a particular manuscript table.

## Common 100 questions and Haiku parsing

The common-question selector uses the original deterministic hash rule with three SQL, three Graph, and four Narrative questions per world. This gives 100 shared questions and 700 question-level cells per model across B0–B6, or 2,100 rows for the three-model comparison.

Original strict parsing and deterministic JSON-fence recovery are retained separately. For the 700 selected Haiku responses, the strict channel has 139 valid outputs and 79 correct answers. The specified recovery channel has 696 valid outputs and 489 correct answers. It strips a complete outer JSON code fence in 557 outputs; the four remaining invalid outputs have length/empty-content outcomes. Raw responses and selected attempts are unchanged.

Fresh verification and any reconstruction of a missing historical analysis program are identified in the analysis documentation. A newly written verifier is not labeled as the author's original historical script.

## Two distinct length-control datasets

| Dataset | Questions | New requests | Baseline reuse |
|---|---:|---:|---|
| Ten-world length study | 30 across ten worlds | 180 | Original main-experiment baseline cells |
| Fixed-world length pilot | 30 from one P100 world | 180 | 180 B1/B3/B5 baseline cells |

The coinciding question counts do not make these the same experiment. Their cohort identifiers and provenance are preserved. First and selected views are separate even when their numerical outcomes coincide.

## P100 and P500 pilots

| Pilot | Selected questions | Sent payloads | Attempts | Unsent B6 cells |
|---|---:|---:|---:|---:|
| P100 | 34 | 476 | 476 | 0 |
| P500 | 33 | 396 | 400 | 66 |

The original source question banks each contain 300 questions. Their selected subsets and answer mappings are included. P100/P500 refer to person populations, while each graph also contains other node types. The source P100 graph has 683 total nodes and 4,883 edges; P500 has 3,072 nodes and 25,070 edges.

P500's 66 B6 cells are blocked/NA configurations, not failed or incorrect model answers. Four additional attempts belong to retries among the 396 sent configurations. The P100 and P500 cohorts are not a paired per-question comparison.

## Validation boundaries

Delivery validation covers source hashes, curated-file hashes, restoration, request binding, and the specific offline analysis checks listed in `VALIDATION.json`. Existing model responses are reused; no provider calls were made to prepare this release. Historical statistical and semantic reports retain their original scope. File integrity does not, by itself, establish every scientific conclusion; use the included executable analyses and documented channels when reproducing a table.
