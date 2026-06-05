# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Remove the `datathon` preset and all its associated specialized scaffolding (dirs, config blocks, and docs).
- Simplify the generator by removing the preset selection step, defaulting to a standard structure.
- Replace `datathon` project type with real ML project type/preset separation (deprecated in favor of full removal).
- Add `vision` as a first-class project type.
- Add `preset` concept to separate ML task from delivery context.
- Add Python environment profiles (safe 3.12, modern 3.14).
- Add optional PyTorch requirements (CPU, CUDA 12.6, CUDA 12.8).
- Refactor pyproject.toml and requirements generation to use templates.

- Add CHANGELOG.md and link it from the root README.

## [0.1.1]

- Added a representative generated project sample in `examples/generated-project-sample/` for documentation and architectural guidance.
- Updated generator to create projects outside the starter repository by default to prevent accidental nesting.
- Added safety checks and confirmation prompts in `create_ml_starter.py` when generating projects inside the starter folder.

## [0.1.0]

- Initial release of the ML Starter Lab Kit.
- Interactive generator `create_ml_starter.py` with support for generic, supervised, unsupervised, timeseries, and datathon project types.
- Lightweight templates in `templates/common/` for EDA, preprocessing, visualization, metrics, optimization, and more.
- Comprehensive documentation hub in `docs/` covering architectures, workflows, models, metrics, and checklists.
- Support for JSON-based configuration and standard library-first implementation.
