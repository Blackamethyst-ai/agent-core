# Changelog

## [2.0.1] - 2026-01-09

### Fixed
- Python 3.9 compatibility (`Optional[dict]` instead of `dict | None`)
- `scratchpad.json` now includes `urls_used` and `urls_skipped` keys
- `log_url.py` adds missing keys to existing scratchpads
- Setup.sh uses individual `mkdir` instead of brace expansion

### Added
- `--update` flag for setup.sh to update existing install
- `ensure_scratchpad_keys()` helper in log_url.py

## [2.0.0] - 2026-01-09

### Added
- `agent-log` command for URL tracking
- `agent-status` alias for quick status
- Cross-environment sync (CLI ↔ Antigravity ↔ Web)
- Auto-extract learnings on archive
- Session index tracking
- CLAUDE.md template
- Parallel sessions workflow

### Changed
- Separated global (`~/.agent-core/`) from local (`.agent/`)
- Improved status output with visual formatting

## [1.0.0] - 2026-01-09

### Added
- Initial release
- Innovation Scout workflow
- Deep Research workflow
- Memory system
- Session management
