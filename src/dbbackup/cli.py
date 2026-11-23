from typing import Annotated
import typer
from pydantic import ValidationError
from dbbackup.connection import ConnectionParams , DatabaseType
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
def test_connection(
    db_type: Annotated[
        DatabaseType,
        typer.Argument(help="Type of the database."),
    ],
    database: Annotated[
        str,
        typer.Option("--database", "-d", help="Database name (or file path for sqlite)."),
    ],
    host: Annotated[str | None, typer.Option("--host", "-h", help="Database host.")] = None,
    port: Annotated[int | None, typer.Option("--port", "-P", help="Database port.")] = None,
    username: Annotated[str | None, typer.Option("--user", "-u", help="Database user.")] = None,
    password: Annotated[
        str | None,
        typer.Option(
            "--password",
            envvar="DBBACKUP_PASSWORD",
            help="Database password. Prefer the DBBACKUP_PASSWORD env var or --ask-password.",
        ),
    ] = None,
    ask_password: Annotated[
        bool,
        typer.Option("--ask-password", help="Prompt for the password (hidden input)."),
    ] = False,
) -> None:
    """Test db connection."""
    if ask_password:
        password = typer.prompt("Password", hide_input=True)

    try:
        params = ConnectionParams(
            db_type=db_type,
            database=database,
            host=host,
            port=port,
            username=username,
            password=password,
        )
    except ValidationError as exc:
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"]) or "connection"
            typer.echo(f"Invalid {location}: {error['msg']}", err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Parsed parameters: {params}")
    typer.echo("(real connection test comes in the next step)")
