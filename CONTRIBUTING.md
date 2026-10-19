# Contributing

Thanks for helping make this research artifact easier to understand, inspect, and build on. Start with the [README](README.md), [representation guide](docs/representation.md), and [reproducibility notes](docs/reproducibility.md).

## Useful contributions

| Area | A focused starting point |
| --- | --- |
| Documentation | Correct a paper/code mismatch, clarify an output example, or improve the English/Chinese entry points |
| Extraction | Add a minimal example for unsupported syntax, then document and implement the intended behavior |
| Batch preprocessing | Fix the documented import/indentation blockers, per-file visitor state, or path handling |
| Research resources | Recover original configurations, data manifests, evaluation scripts, or weights with their provenance |
| New experiments | Test a specific representation or context hypothesis against matched current baselines |

These are contribution opportunities, not a committed release schedule.

## Reporting a problem

Use [GitHub issues](https://github.com/JY0284/code_completion_as_human_action_prediction/issues). For code issues, include the Python version, command, smallest source input that demonstrates the issue, actual output, and expected behavior. For a paper/documentation discrepancy, cite the page, figure, or source function concerned.

## Preparing a change

Keep each change focused enough to explain its effect on readers or extracted actions. The following checks are useful for all changes:

```sh
python sample/extract_actions.py
git diff --check
```

For behavior changes, include representative input/output checks, especially for ordering, context, and sample boundaries. Do not silently update the historical output and call it the original paper's representation. Explain which definition the change follows and whether existing data needs to be regenerated.

For documentation changes, follow the links and run any new commands. Keep the English and Chinese READMEs aligned on capabilities, quickstart, and reported results. Detailed technical guides currently live in English under `docs/`.

There is no full training test suite or verified batch environment yet. State exactly what you exercised in a pull request; passing the extraction demo is not evidence that the paper's experiment has been reproduced.

## Research contributions

Provide model/data revisions, preprocessing and split rules, seeds, configurations, evaluation commands, and the meaning of each metric. Distinguish numbers quoted from the paper from results you reproduced or obtained in a new experiment. Keep large datasets and checkpoints out of routine source changes; link to versioned resources with their provenance and reuse terms.

## Scientific and editorial accuracy

- Write public guides, captions, and figure labels as standalone reference material. Keep editing history in commit messages or changelogs; include explicit versions or dates when history is needed to understand behavior or evidence.
- Explain scientific methods through inputs, transformations, and prediction targets. Put installation requirements and code execution issues in the reproducibility guide, with links from the relevant entry points.
- Make titles and introductions say what is predicted, what information is used, and what a reader can run. Preserve the paper's formal title in citations; do not imply that static AST extraction records human editing behavior.
- Attach a source location to reported numbers: PDF page/table/figure, or a dated primary publication. Preserve unresolved differences between sources instead of silently choosing or averaging values.
- State the prediction unit and denominator. Distinguish methods, action sequences, identifier words, BPE tokens, and source lines. Distinguish percentage points from relative percentages, and means from latency percentiles.
- Separate what the paper reports, what the released code does, what a new experiment measures, and what is proposed. Do not infer statistical significance from a difference without the required analysis.
- For current relevance, verify primary research and first-party engineering sources, record their publication/version dates and the review date, and explain the task differences. Describe potential value as a testable hypothesis unless a matched experiment establishes it. Do not claim priority, adoption, or present-day superiority without evidence.
- For figures, include the data or diagram source, exact units, scope, and material limitations. Replot printed results consistently; do not invent uncertainty intervals or mix incompatible evaluation metrics on one scale.

The source values for the historical accuracy figure are in [reported-results.json](docs/data/reported-results.json); the regeneration command is in the [experiment guide](docs/reproducibility.md#regenerate-the-documentation-figure).

Preserve the existing paper and slide paths when reorganizing documentation, so published links remain usable. Preserve third-party attribution in source files.

## Reuse terms

The repository does not currently declare a license. Please clarify reuse and contribution licensing with the owner before substantial code reuse or contributions. Do not assume the paper, slides, and source all share the same terms.
