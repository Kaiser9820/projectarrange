import typer
from rich.console import Console
from pathlib import Path
from typing import Optional

from .organizer import Organizer
from .config import load_config

app = typer.Typer(
    name="projectarrange",
    help="Automatically organize your messy Downloads folder into clean subfolders.",
    rich_markup_mode="rich",
    no_args_is_help=True,
)

console = Console()

@app.command()
def main(
    path: Optional[Path] = typer.Argument(
        None,
        help="Folder to organize (defaults to ~/Downloads)",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d", help="Show what would happen without moving files"
    ),
    watch: bool = typer.Option(
        False, "--watch", "-w", help="Watch the folder and organize new files automatically"
    ),
    config: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to custom config file"
    ),
):
    """Organize files by type into subfolders."""
    if path is None:
        path = Path.home() / "Downloads"

    if not path.exists():
        console.print(f"[red]Error:[/] Folder {path} does not exist.")
        raise typer.Exit(1)

    config_dict = load_config(config)

    organizer = Organizer(target_dir=path, config=config_dict, console=console)

    if watch:
        console.print("[bold green]Watch mode started.[/] New files will be organized automatically. Press Ctrl+C to stop.")
        organizer.start_watch_mode(dry_run=dry_run)
    else:
        organizer.organize(dry_run=dry_run)


if __name__ == "__main__":
    app()