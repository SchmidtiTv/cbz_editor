import logging
import click

from .utils import create_directory, CBZ_DIR, TEMP_DIR, check_if_project_initialized
from .config import save_config, load_config
from .processing import extract_cbz_and_rename_images

# Setup logging (module-level)
logging.basicConfig(filename='cbz_editor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@click.group()
def cli() -> None:
    """CBZ Processor CLI"""
    pass


@cli.command()
@click.option('--series', help="The name of the series", required=False)
@click.option('--writer', help="The writer's name", required=False)
@click.option('--output-directory-schema', help="Output directory template (use `%d` for volume number)",
              required=False)
def init(series: str, writer: str) -> None:
    """Initialize the cbz_editor by setting up directories and storing metadata."""
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
    output_directory_schema = click.prompt(
        "Output directory template (use `%d` where the volume number should be)",
        default="Volume_%d", show_default=True)

    save_config(series_name, writer_name, output_directory_schema)
    click.echo("Stored series and writer and output_directory_schema info in config.xml")


@cli.command()
@click.argument('volume_number', type=int)
@click.option('--move-originals', is_flag=True,
              help="Move original files to a temp folder after processing.")
def process(volume_number: int, move_originals: bool) -> None:
    """Process CBZ files and rename images for the given volume."""
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

    extract_cbz_and_rename_images(CBZ_DIR, output_directory_schema, volume_number,
                                  series_name, writer_name, move_originals)


if __name__ == '__main__':
    cli()
