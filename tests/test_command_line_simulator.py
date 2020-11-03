from ErnosCube.scripts.command_line_simulator import cli
from click.testing import CliRunner
from pytest import fixture, mark


class TestCommandLineSimulator:
    @fixture
    def runner(self):
        return CliRunner(mix_stderr=False)

    @mark.dependency(name="help")
    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, result.stdout

    @mark.dependency(name="version")
    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) > 0, result.stdout
        assert ", version " in result.stdout, result.stdout

    @mark.dependency(name="exit", depends=["help"])
    def test_exit(self, runner):
        result = runner.invoke(cli, [], input="exit\n")
        assert result.exit_code == 0, result.stdout
        assert len(result.stdout) > 0, result.stdout
        assert len(result.stderr) == 0, result.stderr

    @mark.dependency(depends=["exit"])
    def test_terminal_size_warning(self, runner):
        result = runner.invoke(cli, ["--size", 7], input="exit\n")
        assert result.exit_code == 0, result.exit_code
        assert result.stdout == "ernos-cube > exit\n", result.stdout
        assert len(result.stderr) != 0, result.stderr
        assert "Warning" in result.stderr, result.stderr

    @mark.dependency(depends=["exit"])
    def test_unrecognized_command_error(self, runner):
        result = runner.invoke(cli, [], input="qwerty123\nexit")
        assert result.exit_code == 0, result.exit_code
        assert len(result.stdout) != 0, result.stdout
        assert len(result.stderr) != 0, result.stderr
        assert "Error" in result.stderr, result.stderr

    @mark.dependency(name="no_show", depends=["exit"])
    def test_no_show(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="exit\n")
        assert result.exit_code == 0, result.stdout
        assert len(result.stdout) > 0, result.stdout
        assert result.stdout == "ernos-cube > exit\n", result.stdout
        assert len(result.stderr) == 0, result.stderr

    @mark.dependency(name="show_1", depends=["no_show"])
    def test_show_1(self, runner):
        result = runner.invoke(cli, ["--no-show"], input="show\nexit\n")

        gold = "ernos-cube > show\n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n   "
        gold += "       ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑ "
        gold += " ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑"
        gold += "  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑ "
        gold += " ↑  ↑ \nernos-cube > exit\n"

        assert result.exit_code == 0, result.stdout
        assert len(result.stdout) > 0, result.stdout
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, result.stderr

    @mark.dependency(name="show_2", depends=["show_1"])
    def test_show_2(self, runner):
        result = runner.invoke(cli, [], input="show\nexit\n")

        gold = "          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n ↑"
        gold += "  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n          "
        gold += "↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \nernos-cube "
        gold += "> show\n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  "
        gold += "↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  "
        gold += "↑  ↑  ↑  ↑  ↑  ↑  ↑ \n ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑ \n "
        gold += "         ↑  ↑  ↑ \n          ↑  ↑  ↑ \n          ↑  ↑  ↑ \n"
        gold += "ernos-cube > exit\n"

        assert result.exit_code == 0, result.stdout
        assert len(result.stdout) > 0, result.stdout
        assert result.stdout == gold, repr(result.stdout)
        assert len(result.stderr) == 0, result.stderr
