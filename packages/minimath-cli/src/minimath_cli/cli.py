import minimath
import typer
from rich.console import Console

console = Console()
app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    pkg_name = minimath.__name__
    pkg_version = typer.style(minimath.__version__, fg=typer.colors.CYAN)

    if version:
        typer.echo(f"{pkg_name} {pkg_version}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo(f"{pkg_name} {pkg_version} ready. See --help for usage.")
        raise typer.Exit()


@app.command()
def collatz(n: int) -> None:
    """Show the Collatz sequence."""
    seq = tuple(minimath.seq.collatz(n))
    console.print(f"length {len(seq)}")
    console.print(seq)
