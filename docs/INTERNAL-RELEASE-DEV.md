# Internal Release & Development Guide

This file is for internal developer use only. It documents the release process for this Python package, how to obtain a PyPI (twine) token, how to build and publish releases with twine, and the recommended development workflow.

Files of interest:
- `pyproject.toml` (primary metadata and version)
- `setup.py` (legacy/compat; update if you maintain version here)
- `requirements.txt` (development dependencies)
- `run_tests.py`, `pytest.ini`, and `tests/` (test harness)

## Quick checklist
- [ ] Bump version in `pyproject.toml` before release
- [ ] Commit and tag the release (git tag vX.Y.Z)
- [ ] Build artifacts with `python -m build`
- [ ] Upload to PyPI with `twine`
- [ ] Verify release on PyPI and update changelog if needed

## Prerequisites
- Python 3.8+
- Recommended tools (install locally or in CI):

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade build twine
```

Optional useful dev tools:

```bash
pip install -r requirements.txt
pip install black ruff mypy
```

## 1) Bump the version
The single source of truth for the version is `pyproject.toml` under the `[project]` table. Update the `version` string there to the new release.

Example edit:

```toml
[project]
name = "bubbletea"
version = "0.6.5"  # bump to new version
```

If your repository also maintains a version in `setup.py`, update it there as well to avoid mismatches.

Commit and tag:

```bash
git add pyproject.toml
# add setup.py too if updated
git commit -m "chore(release): bump version to X.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin --follow-tags
```

Notes:
- Avoid reusing versions already published on PyPI — twine will reject duplicates.

## 2) Build distributions
From the repository root run:

```bash
python -m build
```

This will produce files in `dist/`, typically:
- `dist/bubbletea-X.Y.Z.tar.gz` (sdist)
- `dist/bubbletea-X.Y.Z-py3-none-any.whl` (wheel)

Confirm files exist before publishing.

## 3) Obtain a PyPI API token (twine token)
1. Sign in to https://pypi.org/ (your account).
2. Go to "Account settings" → "API tokens" or directly: https://pypi.org/manage/account/.
3. Create a new API token scoped to your project (recommended) or account-wide if necessary.
4. Copy the token (starts with `pypi-...`) and store it securely. You will not be able to see it again after closing the modal.

Local usage (temporary environment variables):

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-XXXXXXXXXXXXXXXXXXXXXXXX"
```

CI usage (recommended):
- Add the token to your CI secret store (e.g., GitHub Actions Secrets) as `PYPI_API_TOKEN` or similar.
- In the CI publish job set `TWINE_USERNAME` to `__token__` and `TWINE_PASSWORD` to `${{ secrets.PYPI_API_TOKEN }}`.

## 4) Publish with twine
To publish to PyPI (after setting `TWINE_USERNAME` and `TWINE_PASSWORD`):

```bash
python -m twine upload dist/*
```

Explicit environment inline example:

```bash
TWINE_USERNAME="__token__" TWINE_PASSWORD="$PYPI_API_TOKEN" python -m twine upload dist/*
```

Publish to TestPyPI for a dry run:

```bash
python -m twine upload --repository testpypi dist/*
```

Notes:
- Use `--repository-url` for custom indexes.
- Twine will prompt or error if credentials are missing or invalid.

## 5) Post-release
- Verify the release page on PyPI: https://pypi.org/project/<package-name>/
- Update CHANGELOG.md/release notes and project docs.
- Merge/push any release branches and clean up.

## 6) Recommended development workflow
1. Create a feature branch for each change: `git switch -c feat/your-change`.
2. Run unit tests locally:

```bash
python -m pytest -q
```

3. Keep `pyproject.toml` up-to-date.
4. Use pre-commit hooks (optional) for formatting and linting.

Example local setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install build twine pytest
```

Run tests and lint:

```bash
python -m pytest
ruff check .
black --check .
```


## Troubleshooting
- Invalid token: regenerate token on PyPI and update secret.
- Version already exists: bump `pyproject.toml` version.
- Build failures: ensure `pyproject.toml` metadata is valid and `build` package installed.

## Security & best practices
- Use project-scoped API tokens where possible.
- Keep tokens in CI secrets, not in repo or logs.
- Revoke tokens if a leak is suspected.

---

Keep this file updated with any CI specifics, policies, or changes to the release process.