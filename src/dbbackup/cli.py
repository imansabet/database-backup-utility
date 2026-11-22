import typer

app = typer.Typer(
    name = "dbbackup",
    help = "A CLI utility for db backup and restore operations.",
    no_args_is_help=True,
        )

@app.callback()
def main() -> None:
    """
    
    Database backup utility.

    Manage db backup and restore operations.
    """
    pass


@app.command()
def version() -> None:
    """Show the current app version."""
    print("Db backup utility v0.1.0")

@app.command()
def test_connection(database: str) -> None:
    """Test db connection. """
    print(f"Selected db: {database}")

