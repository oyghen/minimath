import itertools
from typing import Annotated

import minimath
import typer

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
def collatz(start: int) -> None:
    """Display the Collatz conjecture sequence starting from the given integer.

    Example:
    $ minimath collatz 837799
    """
    seq = tuple(minimath.seqs.collatz(start))
    prefix = typer.style("Sequence length", fg=typer.colors.GREEN)
    seq_length = typer.style(len(seq), fg=typer.colors.CYAN, bold=True)
    typer.echo(f"{prefix}: {seq_length}")
    typer.echo(seq)


@app.command()
def fibonacci(
    n: Annotated[int, typer.Argument(help="Number of terms.")],
    a: int = typer.Option(0, help="First starting integer."),
    b: int = typer.Option(1, help="Second starting integer."),
) -> None:
    """Display the first n terms of the Fibonacci sequence starting with a and b.

    Example:
    $ minimath fibonacci 10
    """
    gen = minimath.seqs.fibonacci(a, b)
    seq = tuple(itertools.islice(gen, n))
    typer.echo(seq)


@app.command()
def keypad(text: list[str]) -> None:
    """Display text with letters replaced by phone keypad digits.

    Example:
    $ minimath keypad hello world
    """
    typer.echo(" ".join(minimath.func.phone_keypad_digits(word) for word in text))
