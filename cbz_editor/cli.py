import click

from .logger.create_logger import create_logger
from .features.combine_to_volume import build_volume as run_build_volume
from .utils import create_directory, CBZ_DIR, TEMP_DIR, check_if_project_initialized
from .config import save_config, load_config, LOG_FILE


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
@click.option('--output-directory-schema', help="Output directory template (use `%d` for volume number)",
              required=False)
def init(series: str, writer: str) -> None:
    """Initialize a new CBZ project."""
    try:
        check_if_project_initialized()
        click.echo("Project is already initialized.", err=True)
        return
    except FileNotFoundError:
        # Continue with initialization
        pass
    except PermissionError:
        click.echo("Permission denied", err=True)
        return

    create_directory(CBZ_DIR)
    create_directory(TEMP_DIR)

    series_name = series or click.prompt("Enter the series name")
    writer_name = writer or click.prompt("Enter the writer's name (optional)", default="", show_default=False)

    while True:
        output_directory_schema = click.prompt(
            "Output directory template (use `%d` where the volume number should be)",
            default="Volume_%d", show_default=True)
        if "%d" in output_directory_schema:
            break
        else:
            click.echo("The output directory template must include `%d` for the volume number.", err=True)

    try:
        save_config(series_name, writer_name, output_directory_schema)
    except PermissionError:
        click.echo("Permission denied", err=True)
        return
    except FileNotFoundError:
        click.echo("File not found", err=True)
        return
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        return

    click.echo("CBZ project initialized.")


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
        click.echo(str(e))
        return

    try:
        series_name, writer_name, output_directory_schema = load_config()
    except FileNotFoundError as e:
        click.echo(str(e))
        return

    logger = create_logger('build_volume', verbose=ctx.obj['VERBOSE'], log_file=LOG_FILE)

    run_build_volume(CBZ_DIR, output_directory_schema, volume_number,
                 series_name, writer_name, move_originals, logger)


if __name__ == '__main__':
    cli()
