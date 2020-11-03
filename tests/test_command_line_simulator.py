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
