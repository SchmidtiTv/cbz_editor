import rich_click as click  # drop-in, --help is now pretty
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

from cbz_editor.features.combine_volume import VolumeBuilder
from .logger.create_logger import create_logger
from .utils import create_directory, CBZ_DIR, TEMP_DIR, check_if_project_initialized
from .config import save_config, load_config, LOG_FILE

# Two consoles — stdout for normal output, stderr for errors
console = Console()
err_console = Console(stderr=True)

# Optional: configure rich-click styling
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_SWITCH = "bold green"
click.rich_click.STYLE_METAVAR = "dim"
click.rich_click.USE_RICH_MARKUP = True  # lets you use [bold]...[/bold] in help strings


@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output.")
@click.pass_context
def cli(ctx, verbose) -> None:
    """CBZ Processor CLI"""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@cli.command()
@click.option('--series', help="The name of the series", required=False)
@click.option('--writer', help="The writer's name", required=False)
@click.option('--output-directory-schema',
              help="Output directory template (use `%d` for volume number)", required=False)
def init(series: str, writer: str, output_directory_schema: str) -> None:
    """Initialize a new CBZ project."""
    try:
        check_if_project_initialized()
        err_console.print("[yellow]⚠ Project is already initialized.[/yellow]")
        return
    except FileNotFoundError:
        pass
    except PermissionError:
        err_console.print("[red]✗ Permission denied.[/red]")
        return

    create_directory(CBZ_DIR)
    create_directory(TEMP_DIR)

    series_name = series or Prompt.ask("[cyan]Series name[/cyan]")
    writer_name = writer if writer is not None else Prompt.ask(
        "[cyan]Writer's name[/cyan] [dim](optional)[/dim]", default=""
    )

    if not output_directory_schema or "%d" not in output_directory_schema:
        if output_directory_schema and "%d" not in output_directory_schema:
            err_console.print("[red]✗ Output directory template must include [bold]%d[/bold] for the volume number.[/red]")

        while True:
            output_directory_schema = Prompt.ask(
                "[cyan]Output directory template[/cyan] [dim](use %d for volume number)[/dim]",
                default="Volume_%d"
            )
            if "%d" in output_directory_schema:
                break
            err_console.print("[red]✗ Template must include [bold]%d[/bold].[/red]")

    try:
        save_config(series_name, writer_name, output_directory_schema)
    except PermissionError:
        err_console.print("[red]✗ Permission denied.[/red]")
        return
    except FileNotFoundError:
        err_console.print("[red]✗ File not found.[/red]")
        return
    except Exception as e:
        err_console.print(f"[red]✗ An error occurred:[/red] {e}")
        return

    console.print(Panel(
        Text("✓ CBZ project initialized.", style="bold green"),
        border_style="green",
        expand=False
    ))


@cli.command()
@click.pass_context
@click.argument('volume_number', type=int)
@click.option('--move-originals', is_flag=True,
              help="Move original files to a temp folder after processing.")
def build_volume(ctx, volume_number: int, move_originals: bool) -> None:
    """Combine CBZ files into a volume cbz."""
    try:
        check_if_project_initialized()
    except FileNotFoundError as e:
        err_console.print(f"[red]✗[/red] {e}")
        return

    try:
        series_name, writer_name, output_directory_schema = load_config()
    except FileNotFoundError as e:
        err_console.print(f"[red]✗[/red] {e}")
        return

    logger = create_logger('build_volume', verbose=ctx.obj['VERBOSE'], log_file=LOG_FILE)
    builder = VolumeBuilder(CBZ_DIR, output_directory_schema, volume_number,
                            series_name, writer_name, move_originals, logger)
    builder.build()


if __name__ == '__main__':
    cli()