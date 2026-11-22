from typing import Annotated
import typer

from dbbackup import __version__

app = typer.Typer(
    name = "dbbackup",
    help = "A CLI utility for db backup and restore operations.",
    no_args_is_help=True,
        )


def version_callback(value:bool) -> None:
    """Print the version and exit if --version was passed  """
    if value:
        typer.echo(f"dbbackup v{__version__}")
        raise typer.Exit()
    

@app.callback()
def main(
    show_version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="Show the version and exit.",),
        ] = False,
        ) -> None:
    """
    Database backup utility.

    Manage db backup and restore operations.
    """
   



@app.command()
def test_connection(database: str) -> None:
    """Test db connection. """
    print(f"Selected db: {database}")

