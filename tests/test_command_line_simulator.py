from ErnosCube.scripts.command_line_simulator import cli
from click.testing import CliRunner
from pytest import fixture, mark


class TestCommandLineSimulator:
    @fixture
    def runner(self):
        return CliRunner(mix_stderr=False)

    @mark.dependency(name="cl_help")
    def test_cl_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)

    @mark.dependency(name="version")
    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert ", version " in result.stdout, repr(result.stdout)

    @mark.dependency(name="exit", depends=["cl_help"])
    def test_exit(self, runner):
        result = runner.invoke(cli, [], input="exit\n")
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_terminal_size_warning(self, runner):
        result = runner.invoke(cli, ["--size", 7], input="exit\n")
        assert result.exit_code == 0, result.exit_code
        assert result.stdout == "ernos-cube> exit\n", repr(result.stdout)
        assert len(result.stderr) != 0, repr(result.stderr)
        assert "Warning" in result.stderr, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_unrecognized_command_error(self, runner):
        result = runner.invoke(cli, [], input="qwerty123\nexit")
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) != 0, repr(result.stdout)
        assert len(result.stderr) != 0, repr(result.stderr)
        assert "Error" in result.stderr, repr(result.stderr)

    @mark.dependency(name="no_show", depends=["exit"])
    def test_no_show(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="exit\n")
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == "ernos-cube> exit\n", repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(name="show_1", depends=["no_show"])
    def test_show_1(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="show\nexit\n")

        gold = "ernos-cube> show\n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n   "
        gold += "       ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑ "
        gold += " ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑"
        gold += "  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑ "
        gold += " ↑  ↑ \nernos-cube> exit\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(name="show_2", depends=["show_1"])
    def test_show_2(self, runner):
        result = runner.invoke(cli, [], input="show\nexit\n")

        gold = "          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n ↑"
        gold += "  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n          "
        gold += "↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \nernos-cube"
        gold += "> show\n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  "
        gold += "↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n "
        gold += "         ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n"
        gold += "ernos-cube> exit\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(name="clear", depends=["no_show"])
    def test_clear(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="clear\nexit\n")

        gold = "ernos-cube> clear\nernos-cube> exit\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(name="command_help", depends=["no_show"])
    def test_command_help(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="help\nexit\n")

        part_gold = "ernos-cube> help\nThere are two classes of interpreter"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert part_gold in result.stdout, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_cw_rotation(self, runner):
        result = runner.invoke(cli, [], input="cw z 2\nexit\n")

        gold = "          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n ↑"
        gold += "  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n          "
        gold += "↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \nernos-cube>"
        gold += " cw z 2\n          ←  ←  ← \n          ←  ←  ← \n          ← "
        gold += " ←  ← \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑ "
        gold += " ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n"
        gold += "          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n"
        gold += "ernos-cube> exit\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_full_ccw_rotation(self, runner):
        result = runner.invoke(cli, [], input="ccw z\nexit\n")

        gold = "          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n ↑"
        gold += "  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n          "
        gold += "↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \nernos-cube>"
        gold += " ccw z\n          →  →  → \n          →  →  → \n          →  "
        gold += "→  → \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n "
        gold += "         ←  ←  ← \n          ←  ←  ← \n          ←  ←  ← \n"
        gold += "ernos-cube> exit\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_rotation_error_1(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="zw z 2\nexit\n")

        stdout_gold = "ernos-cube> zw z 2\nernos-cube> exit\n"

        stderr_gold = "Error: unrecognized command ('zw z 2'). Type `help` "
        stderr_gold += "for more\ninformation.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_rotation_error_2(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="cw a 2\nexit\n")

        stdout_gold = "ernos-cube> cw a 2\nernos-cube> exit\n"

        stderr_gold = "Error: unrecognized axis specification: 'a'. An axis "
        stderr_gold += "can be\nspecified as '(x|y|z)'. Type `help` for more"
        stderr_gold += " information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_rotation_error_3(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="cw x -2\nexit\n")

        stdout_gold = "ernos-cube> cw x -2\nernos-cube> exit\n"

        stderr_gold = "Error: the layer of a rotation must be between -1 and "
        stderr_gold += "2. The user\nsupplied -2 ('cw x -2'). Type `help` for "
        stderr_gold += "more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_rotation_error_4(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="cw x 3\nexit\n")

        stdout_gold = "ernos-cube> cw x 3\nernos-cube> exit\n"

        stderr_gold = "Error: the layer of a rotation must be between -1 and "
        stderr_gold += "2. The user\nsupplied 3 ('cw x 3'). Type `help` for "
        stderr_gold += "more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_rotation_error_5(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="cw x abc\nexit\n")

        stdout_gold = "ernos-cube> cw x abc\nernos-cube> exit\n"

        stderr_gold = "Error: the layer of a rotation must be between -1 and "
        stderr_gold += "2. The user\nsupplied 'abc' ('cw x abc'). Type `help`"
        stderr_gold += " for more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_rotation_error_6(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="cw z 1 2\nexit\n")

        stdout_gold = "ernos-cube> cw z 1 2\nernos-cube> exit\n"

        stderr_gold = "Error: unrecognized command ('cw z 1 2'). A rotation "
        stderr_gold += "can be\nspecified as '(cw|ccw|ht) <axis> <layer>'. "
        stderr_gold += "Type `help` for more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_scramble_1(self, runner):
        input = "scramble\nexit\n"
        result = runner.invoke(cli, [], input=input)

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_scramble_2(self, runner):
        input = "scramble 20 42\nexit\n"
        result = runner.invoke(cli, [], input=input)

        stdout_gold = "          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑ "
        stdout_gold += " ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑"
        stdout_gold += "  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ "
        stdout_gold += " ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n   "
        stdout_gold += "       ↑  ↑  ↑ \nernos-cube> scramble 20 42\n         "
        stdout_gold += " ←  ↓  ← \n          ↑  ↓  ↑ \n          ↑  ↓  ↓ \n ↓ "
        stdout_gold += " ←  ←  →  ←  ↑  ←  →  →  →  ↓  ↓ \n →  ↑  →  →  ↑  ↓  "
        stdout_gold += "↓  ↑  ↓  →  ↑  → \n ←  ↓  ←  →  ↓  →  →  ↑  →  ←  ←  ←"
        stdout_gold += " \n          ↓  ↑  → \n          ↑  ↑  ↑ \n          ↓"
        stdout_gold += "  →  ↓ \nernos-cube> exit\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) == 0, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_scramble_error_1(self, runner):
        input = "scramble abc\nexit\n"
        result = runner.invoke(cli, ["--no-show"], input=input)

        stdout_gold = "ernos-cube> scramble abc\nernos-cube> exit\n"

        stderr_gold = "Error: invalid specification of the number of turns: "
        stderr_gold += "'abc'. Type\n`help` for more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_scramble_error_2(self, runner):
        input = "scramble 0\nexit\n"
        result = runner.invoke(cli, ["--no-show"], input=input)

        stdout_gold = "ernos-cube> scramble 0\nernos-cube> exit\n"

        stderr_gold = "Error: The specified number of turns must be a positive"
        stderr_gold += " number.\nType `help` for more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_scramble_error_3(self, runner):
        input = "scramble 1 abc\nexit\n"
        result = runner.invoke(cli, ["--no-show"], input=input)

        stdout_gold = "ernos-cube> scramble 1 abc\nernos-cube> exit\n"

        stderr_gold = "Error: invalid specification of the seed: "
        stderr_gold += "'abc'. Type `help` for\nmore information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)

    @mark.dependency(depends=["exit"])
    def test_scramble_error_4(self, runner):
        input = "scramble 1 42 4\nexit\n"
        result = runner.invoke(cli, ["--no-show"], input=input)

        stdout_gold = "ernos-cube> scramble 1 42 4\nernos-cube> exit\n"

        stderr_gold = "Error: unrecognized command ('scramble 1 42 4'). A "
        stderr_gold += "scramble can\nbe specified as 'scramble <N> <seed>'. "
        stderr_gold += "Type `help` for more information.\n"

        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, repr(result.stdout)
        assert result.stdout == stdout_gold, repr(result.stdout)
        assert len(result.stderr) > 0, repr(result.stderr)
        assert result.stderr == stderr_gold, repr(result.stderr)
