# From method calls to next edits: relevance and research questions

[Home](../README.md) · [Representation](representation.md) · [Reproducibility](reproducibility.md)

Sources checked **2026-10-19**. Dates and versions below identify the evidence reviewed; they are not a claim of exhaustive coverage or of the latest model release. The connections below are analytical comparisons; the cited sources do not document adoption of the 2022 action representation.

The 2022 paper makes code representation and naming context explicit experimental variables. That remains a useful starting point for studying what information a code assistant needs. The unresolved modern hypothesis is whether these action fields add quality or reduce cost when a stronger model receives comparable information. A small structured record is not automatically shorter in BPE tokens: repeated context and delimiters may offset information removed from source.

## Distinguish the prediction tasks

| Problem | Evidence available to the model | Prediction and evaluation |
| --- | --- | --- |
| This paper's next-method-call task | Static source converted to actions and naming context | Next method-call token; slides describe a first-word target. [Metric details](reproducibility.md#metric-and-length-definitions) |
| Repository-level code completion | Source prefix/suffix and relevant code elsewhere in a repository | Text or code completion; exact-match or execution-based measures, depending on the benchmark |
| Next-edit prediction | Current editor state and a supplied history of edits or interactions | Where and what to edit; timing and user acceptance may also matter |
| Post-acceptance editing, as evaluated in DECODE | An accepted AI completion and, in some settings, early edit snapshots | Classify its eventual retention category or generate its final edited state; not necessarily the immediately next edit |

In particular, AST order, reconstructed commit sequences, and recorded IDE interactions are different kinds of evidence. One cannot substitute for another without evaluating the resulting assumptions.

## Selected academic connections

| Work and reviewed version | What the source establishes | Implication for this repository |
| --- | --- | --- |
| [CrossCodeEval](https://arxiv.org/abs/2310.11248v2), NeurIPS 2023; v2 2023-11-17 | Completion samples selected to require cross-file context, across four programming languages | Test whether action context adds value beyond relevant repository code |
| [ExecRepoBench](https://arxiv.org/abs/2412.11990v1), preprint 2024-12-16 | Executable repository-level Python completion at statement, expression, and function granularity | Use functional checks for tasks that support them; token hits answer a narrower question |
| [Next Edit Prediction](https://arxiv.org/abs/2508.10074v2), preprint v2 2025-09-14 | Predicts edit location and content from commit-derived sequences; the described construction restricts edits to additions | Distinguish reconstructed edits from observed IDE actions and test deletions/replacements separately |
| [EditFlow](https://arxiv.org/abs/2602.21697v3), OOPSLA 2026; v3 2026-04-08 | Reconstructs developer editing flows to benchmark and optimize code-edit recommendation | Evaluate sequences of recommendations rather than only isolated token predictions |
| [DECODE](https://arxiv.org/abs/2607.25130v2), preprint v2 2026-09-14 | Tracks real in-IDE changes to accepted AI completions. Section 5 evaluates final-state classification and generation, with optional early edit history | Offers observed editing trajectories for related research; its sampled, completion-centered data are not a complete keystroke log or a direct replacement for a next-edit benchmark |

These works suggest useful comparison axes: available information, prediction granularity, how history is obtained, and whether evaluation covers a process or a single completion. They do not provide an apples-to-apples score comparison with the 2022 result.

## What industrial systems add

[Cursor's Tab report (2025-09-12)](https://cursor.com/blog/tab-rl) describes online reinforcement learning from accepted/rejected suggestions and learning when to withhold a suggestion. This adds a feedback loop and an intervention decision, neither of which this repository's static extraction models.

[GitHub's NES training report (2025-11-20, updated 2025-11-25)](https://github.blog/ai-and-ml/github-copilot/evolving-github-copilots-next-edit-suggestions-through-custom-model-training/) explains limitations of clean pull-request diffs and describes volunteered editor data, no-edit examples, latency work, and online A/B evaluation. A [2026-04-24 JetBrains release note](https://github.blog/changelog/2026-04-24-inline-agent-mode-in-preview-and-more-in-github-copilot-for-jetbrains-ides/) documents far-away edit suggestions and inline previews. Model output, timing, and editor presentation all affect the deployed task.

[Zed's Zeta2 development report (2026-04-07)](https://zed.dev/blog/how-we-developed-zeta2) describes recent edits, language-server context, and teacher-generated targets for real editing states. These training targets must not be described as the user's observed next action. The [Zeta2.1 report (2026-05-08)](https://zed.dev/blog/zeta2-1) changes the output to regions around proposed modifications. It reports average output length decreasing from approximately 270 to 90 tokens and median response time from 189 to 136 milliseconds. Those are different measures: the latter is a 53-millisecond reduction, not a threefold speedup. Neither is the original paper's 2022 prediction-time measurement.

These links are first-party engineering reports. They describe the authors' systems and measurements, not independent comparative evaluations of this repository.

This comparison suggests that the paper remains relevant as a **representation hypothesis**: selecting and organizing information can matter alongside model capacity. Current products also require editable locations, real interaction history, abstention decisions, and feedback. The 2022 result establishes none of those product capabilities, and the sources above do not establish that any product uses this action representation.

## Experiments worth running

The central hypothesis to retest is: **can explicit action structure improve prediction quality or efficiency beyond what a modern model gets from the same source and context?**

Start with a controlled comparison:

| Condition | Input |
| --- | --- |
| A | Raw source prefix |
| B | Raw source prefix plus the same contextual names supplied to the action representation |
| C | Actions plus that context |
| D | Raw source plus actions and that context |

First choose one target definition: reproducing the historical token metric, predicting a complete method name, or predicting an edit are separate experiments. For A–D, hold the base-model/tokenizer revision, training regime, prediction points, labels, and repository-disjoint test set constant. Report training examples, update steps, processed tokens, and compute; these budgets cannot all be assumed equal when sequence lengths differ. Compare B with C and D to test the value of the representation under matched contextual information. Include a structure × context × identifier-splitting ablation where feasible.

Condition C discards parts of the source syntax, while D adds a second encoding of some information already present. Thus B versus C is not a pure formatting intervention, and B versus D may change truncation at a fixed token limit. Report retained information and truncation alongside the scores.

Build inputs only from information available at the prediction point. In particular, extracting an AST from a completed file must not expose the target call, later code, or names introduced by future edits. Report parsing failures on incomplete editor buffers. Compare both fixed input-token budgets and full retained information, with explicit truncation rules and actual token counts. Define causal next-call experiments and suffix-visible fill-in-the-middle experiments separately.

Beyond the historical token/first-word metric, measure complete method-name accuracy, valid call arguments where labels allow it, and functional correctness for executable tasks. Report preprocessing overhead, model input/output tokens, and end-to-end latency alongside quality. Specify hardware, batch size, caching, concurrency, and whether latency is a mean, median (p50), or tail percentile (such as p95); keep milliseconds and seconds explicit. A loss of important syntax may offset any savings from a structured representation.

For next-edit prediction, add source positions and an explicit edit representation, use real or clearly labeled reconstructed interaction histories, and evaluate location, content, and when to suggest. Count accepted suggestions per shown suggestion separately from suggestions shown per eligible opportunity. Acceptance is not a measure of functional correctness or time saved; a productivity claim needs a study that measures developer outcomes. Static AST actions alone cannot establish those capabilities.

## Useful roles for this repository

- A teaching artifact for connecting Python ASTs, structured actions, and language-model inputs.
- A historical research reference with explicit distinctions between reported experiments and released code.
- A starting point for controlled studies of context selection and code representation.

A competitive next-edit system would need a broader dataset, prediction interface, and evaluation loop. See [contributing](../CONTRIBUTING.md) for ways to develop the extractor and experimental infrastructure.
