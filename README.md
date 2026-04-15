# ProjectArrange

A clean, fast, and smart CLI file organizer for messy folders.

ProjectArrange automatically sorts files into logical directories so your workspace stays tidy and predictable. It is designed for day-to-day desktop use, with practical defaults for developers, creators, and power users.

## Features

- Smart screenshot detection (`Capture`, `Screenshot`, `IMG_`, `Snap`, etc.) with priority over generic image rules.
- Temporal organization for media: creates `YYYY-MM` subfolders for `Images` and `Screenshots`.
- Developer-friendly categorization, including Roblox file support (`.rbxl`, `.rbxm`, etc.) and common code formats.
- Safe preview mode with `--dry-run` before any file is moved.
- Real-time organization with `--watch` for continuously monitored folders.
- Automatic filename conflict handling using numeric suffixes (for example, `_1`, `_2`).
- Clear CLI output powered by Rich tables and progress indicators.

## Requirements

- Python `3.10+`
- [uv](https://github.com/astral-sh/uv) (recommended package/dependency manager)

Dependencies such as `rich` and `watchdog` are installed automatically.

## Installation

```bash
git clone https://github.com/<your-username>/ProjectArrange.git
cd ProjectArrange
uv sync
```

## Usage

Run commands from the directory you want to organize.

### Common commands

| Task | Command |
| :--- | :--- |
| Preview changes | `uv run projectarrange --dry-run` |
| Organize now | `uv run projectarrange` |
| Watch continuously | `uv run projectarrange --watch` |

### CLI options

| Option | Shorthand | Description |
| :--- | :--- | :--- |
| `--dry-run` | `-d` | Show planned moves without writing changes. |
| `--watch` | `-w` | Monitor the folder and organize new files in real time. |
| `--help` | `-h` | Display help information. |

## Example (dry run)

| Original File | Category | Destination |
| :--- | :--- | :--- |
| `Capture.PNG` | `Screenshots` | `Screenshots/2026-04/Capture.PNG` |
| `BloxFruits.rbxl` | `Roblox` | `Roblox/BloxFruits.rbxl` |
| `vacation_vlog.mp4` | `Video` | `Video/vacation_vlog.mp4` |
| `notes.docx` | `Documents` | `Documents/notes.docx` |

## Project structure

```text
ProjectArrange/
├── src/
│   └── projectarrange/
│       ├── __init__.py
│       ├── cli.py
│       └── organizer.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## Customization

Update file extension mappings and target folder names in `DEFAULT_CATEGORIES`:

`src/projectarrange/organizer.py`

## License

Distributed under the MIT License. See `LICENSE` for details.
