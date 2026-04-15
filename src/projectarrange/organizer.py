from pathlib import Path
import shutil
import time
from rich.console import Console
from rich.table import Table
from rich.progress import track
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Dict, Any

# Default categories
DEFAULT_CATEGORIES: Dict[str, list[str]] = {
    "Roblox": [".rbxl", ".rbxm", ".rbxlx", ".rbxl.lock"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".bmp", ".tiff", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".csv", ".pptx", ".docm"],
    "Audio": [".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xapk", ".apk", ".bar"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".appimage", ".msix"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".toml", ".yaml", ".yml", ".lua"],
}

class Organizer:
    def __init__(self, target_dir: Path, config: Dict[str, Any], console: Console):
        self.target_dir = target_dir
        self.console = console
        self.categories = config.get("categories", DEFAULT_CATEGORIES)

    def get_category(self, file_path: Path) -> str:
        """Smart category detection with screenshot priority."""
        name_lower = file_path.name.lower()
        ext = file_path.suffix.lower()

        # Screenshot detection takes priority
        screenshot_keywords = ["screenshot", "capture", "screen", "snap", "img_", "ss_"]
        if any(keyword in name_lower for keyword in screenshot_keywords):
            return "Screenshots"

        # Extension categories
        for category, extensions in self.categories.items():
            if ext in extensions:
                return category

        return "Others"

    def organize(self, dry_run: bool = False):
        """Main organization logic."""
        files = [f for f in self.target_dir.iterdir() if f.is_file()]

        if not files:
            self.console.print("[yellow]No files found to organize.[/]")
            return

        # Table with lines (your preferred style) + better width control
        table = Table(
            title="Preview (Dry Run)" if dry_run else "Organized Files",
            show_lines=True,
            expand=True,
            title_style="bold cyan",
        )
        table.add_column("Original File", style="cyan", no_wrap=False, max_width=80, overflow="fold")
        table.add_column("Category", style="magenta", width=14)
        table.add_column("Destination", style="green", no_wrap=False, max_width=80, overflow="fold")

        moved = 0

        for file in track(files, description="Organizing files..."):
            category = self.get_category(file)

            dest_folder = self.target_dir / category

            # Year-Month subfolder for images/screenshots
            if category in ("Screenshots", "Images"):
                mtime = file.stat().st_mtime
                date_str = time.strftime("%Y-%m", time.localtime(mtime))
                dest_folder = dest_folder / date_str

            dest_folder.mkdir(parents=True, exist_ok=True)

            dest_path = dest_folder / file.name

            # Handle duplicate filenames
            if dest_path.exists():
                stem = dest_path.stem
                suffix = dest_path.suffix
                counter = 1
                while (dest_folder / f"{stem}_{counter}{suffix}").exists():
                    counter += 1
                dest_path = dest_folder / f"{stem}_{counter}{suffix}"

            table.add_row(
                file.name,
                category,
                str(dest_path.relative_to(self.target_dir))
            )

            if not dry_run:
                shutil.move(str(file), str(dest_path))
                moved += 1

        self.console.print(table)

        if dry_run:
            self.console.print("[bold yellow]Dry run completed — no files were moved.[/]")
        else:
            self.console.print(f"[bold green]Success![/] {moved} file(s) organized.")

    def start_watch_mode(self, dry_run: bool = False):
        """Watch mode for automatic organization."""
        class Handler(FileSystemEventHandler):
            def __init__(self, organizer):
                self.organizer = organizer

            def on_created(self, event):
                if not event.is_directory:
                    time.sleep(1.0)
                    self.organizer.organize(dry_run=dry_run)

        observer = Observer()
        event_handler = Handler(self)
        observer.schedule(event_handler, str(self.target_dir), recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.console.print("\n[bold yellow]Watch mode stopped.[/]")
        observer.join()