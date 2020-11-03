import click
from ..cube import Cube


@click.command()
@click.option(
    "--size", type=click.IntRange(min=1), default=3, help="Size of the Rubik's Cube."
)
@click.option(
    "--show/--no-show", default=True, help="Show the cube after every command."
)
@click.version_option()
def cli(size, show):
    """A command-line Rubik's Cube simulator.

    All commands are case-insensitive.
    """

    cube = Cube(N=size)
    show_before_prompt = evaluate_terminal_size(cube)
    while True:
        if show and show_before_prompt:
            click.echo(repr(cube))
        else:
            show_before_prompt = True

        value = click.prompt("ernos-cube", prompt_suffix=" > ", type=str)
        tokens = value.strip().lower().split(" ")
        if tokens[0] == "exit":
            break

        elif tokens[0] == "show":
            click.echo(repr(cube))
            show_before_prompt = False

        else:
            error(f"unrecognized command ({repr(value)}).")
            show_before_prompt = True

    click.get_current_context().exit()


def evaluate_terminal_size(cube):
    show_before_prompt = True
    cube_size = cube.get_raw_repr_size()
    cube_width, cube_height = cube_size

    term_size = click.get_terminal_size()
    term_width, term_height = term_size

    if (cube_width > term_width) or (cube_height > term_height):
        warn_str = f"the {cube.N} x {cube.N} x {cube.N} Rubik's Cube cannot be"
        warn_str += f" cleanly displayed in the terminal (cube size="
        warn_str += f"{cube_size}, terminal size={term_size}). Please consider"
        warn_str += " making the terminal larger."
        warn(warn_str)
        show_before_prompt = False

    return show_before_prompt


def warn(warn_str, err=True):
    warn_tag = click.style("Warning", fg="yellow", bold=True)
    click.echo(click.wrap_text(f"{warn_tag}: {warn_str}"), err=err)


def error(error_str):
    error_tag = click.style("Error", fg="red", bold=True)
    click.echo(click.wrap_text(f"{error_tag}: {error_str}"), err=True)
