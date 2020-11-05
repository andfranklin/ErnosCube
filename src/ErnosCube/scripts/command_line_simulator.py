import click
from ..cube import Cube
from ..rotation_enum import RotationEnum
from ..axis_enum import AxisEnum
from ..cube_rotation import CubeRotation


help_str = """There are two classes of interpreter commands: general commands
and cube manipulations. All commands for the `ernos-cube` interpreter are
case-insensitive.

GENERAL COMMANDS
    help:  display this message.
    show:  show the cube.
    clear: clear the terminal.
    exit:  exit the interpreter.

CUBE MANIPULATIONS
    cw <axis> <layer>
    ccw <axis> <layer>
    ht <axis> <layer>
    scramble <number of moves>

The `cw`, `ccw`, and `ht` commands invoke a clockwise, counter-clockwise or, a
half-turn rotation on the cube about a specified axis, respectively. The
argument, `<axis>`, must be `x`, `y`, or `z`. The optional argument, `<layer>`,
may be an integer between -1 and N-1 (where N is the size of the cube). If
`<layer>` is not specified, or if it is specified as -1, then the entire cube
is rotated about the specified `<axis>`.

The command, `scramble`, (pseudo)randomly scrambles the cube by the specified
number of moves. Warning: the moves might be negating. In other words, there is
no guarantee that a random sequence of moves will not cancel-out, and
effectively result in no mutation of the cube.
"""


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

    For information about the available commands, type `help` into the
    interactive interpreter.
    """

    # setup
    prompt_text = click.style("ernos-cube", bold=True, fg="green")
    prompt_suffix = click.style("> ", bold=True, fg="green")
    cube = Cube(N=size)
    show_before_prompt = evaluate_terminal_size(cube, show)

    # event loop
    while True:
        # pre-processing
        if show_before_prompt:
            click.echo(repr(cube))

        # reading next command
        value = click.prompt(prompt_text, prompt_suffix=prompt_suffix, type=str)

        # lexing
        tokens = value.strip().lower().split(" ")

        # parsing / interpreting
        if tokens[0] == "cw" or tokens[0] == "ccw" or tokens[0] == "ht":
            show_before_prompt = show
            parse_success, data = parse_rotation_command(size, value, tokens)
            if not parse_success:
                show_before_prompt = False
                continue
            cube.rotate(CubeRotation(*data))

        elif tokens[0] == "show":
            show_before_prompt = True

        elif tokens[0] == "help":
            click.echo_via_pager(help_str)
            show_before_prompt = False

        elif tokens[0] == "clear":
            click.clear()
            show_before_prompt = False

        elif tokens[0] == "exit":
            break

        else:
            err_str = f"unrecognized command ({repr(value)})."
            error(err_str)
            show_before_prompt = show

    click.get_current_context().exit()


def evaluate_terminal_size(cube, show_before_prompt):
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


def parse_rotation_command(size, value, tokens):
    rotation_enum = RotationEnum.get_enum(tokens[0])

    try:
        axis_enum = AxisEnum.get_enum(tokens[1])
    except KeyError:
        err_str = f"unrecognized axis specification: "
        err_str += f"{repr(tokens[1])}. An axis can be specified as "
        err_str += "'(x|y|z)'."
        error(err_str)
        return False, None

    if len(tokens) == 2:
        layer = -1
    elif len(tokens) == 3:
        parse_layer_e = False

        try:
            layer = int(tokens[2])
        except ValueError:
            parse_layer_e = True

        parse_layer_e = parse_layer_e or layer < -1 or layer >= size
        if parse_layer_e:
            err_str = f"the layer of a rotation must be between -1 and"
            err_str += f" {size-1}. The user supplied {layer} "
            err_str += f"({repr(value)})."
            error(err_str)
            return False, None
    else:
        err_str = f"unrecognized command ({repr(value)}). A rotation "
        err_str += "can be specified as '(cw|ccw|ht) <axis> <layer>'."
        error(err_str)
        return False, None

    return True, (axis_enum, rotation_enum, layer)


def warn(warn_str, err=True):
    warn_tag = click.style("Warning", fg="yellow", bold=True)
    click.echo(click.wrap_text(f"{warn_tag}: {warn_str}"), err=err)


def error(error_str):
    error_tag = click.style("Error", fg="red", bold=True)
    error_str = f"{error_tag}: {error_str} Type `help` for more information."
    click.echo(click.wrap_text(error_str), err=True)
