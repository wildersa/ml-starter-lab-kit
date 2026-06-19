# Contributing

## Automated PR validation policy

This repository may use recurring assistant/watch tasks to validate implementation pull requests created by Jules, Codex, or local agents.

The watcher is allowed to inspect issues, PR bodies, diffs, changed files, relevant source code, tests, CI status, and previous PR comments before producing a verdict.

## Review discipline

Automated validation must check the implementation, not just the PR description.

Each validation should verify:

- the linked issue P0 contract;
- allowed and forbidden scope;
- changed files and full diff/patch;
- relevant source code when needed;
- tests and CI/check status;
- CLI/wizard behavior, generated examples, docs, contracts, data-processing boundaries, and training/evaluation behavior when touched;
- whether the PR should merge now, wait for a small fix, require human approval, or be blocked.

The watcher must not use `REQUEST_CHANGES`. When a fix is needed, it should leave a normal top-level PR comment with a concrete local fix and required proof.

## Watcher labels

Use these labels when available:

- `watcher:active` — PR/issue is under automatic validation;
- `watcher:blocked` — automatic validation is blocked;
- `watcher:needs-human` — human review/intervention is required;
- `watcher:validated` — PR was validated as safe by the watcher.

If labels are unavailable, the watcher should use explicit PR/issue comments with the same meaning.

## Validation loop limit

Each PR gets at most three automatic validation/comment cycles.

Watcher comments should include a marker like:

```txt
Watcher validation: 1/3
Status: waiting-update | blocked | needs-human | validated | mergeable
```

After three unsuccessful validations, the watcher must stop acting on that PR/issue flow and notify the maintainer that human intervention is required.

While blocked, the watcher must not:

- comment again;
- merge the PR;
- add `jules` to the next issue;
- continue the issue chain.

The blocked flow may resume only after the maintainer explicitly authorizes continuation.

## Auto-merge policy

Auto-merge is allowed only for low-risk PRs, such as:

- docs-only changes;
- isolated tests;
- prompt/help-text/UI copy changes with targeted proof;
- CLI shell/wizard ergonomics that do not alter backend/data/training semantics;
- generated example updates when runtime behavior is unaffected and tests prove compatibility.

Do not auto-merge without maintainer approval when a PR touches sensitive areas, including:

- training/evaluation behavior;
- reward/action semantics;
- data leakage checks;
- data preprocessing or schema contracts;
- model-selection/runtime behavior;
- persistence/output artifact formats;
- generated project templates with broad blast radius;
- CI/build/release workflows;
- dependency or lockfile changes;
- broad architecture or cross-layer contracts.

For sensitive PRs, the watcher may validate and provide a verdict, but must wait for maintainer approval before merge.

## Single-active-flow rule

Do not start the next issue by adding `jules` if there is already an active implementation PR or another issue already running with `jules`, unless the issue body explicitly states the work is parallel-safe.

Never start dependent issues early.

## PR comment style

Watcher comments must be atomic to the current PR. They should not ask the agent to coordinate adjacent PRs, rebase against unrelated work, or solve broad repository cleanup.

A good watcher comment includes:

- the concrete issue found;
- the expected local fix;
- required proof/test command;
- watcher validation count and status marker.
