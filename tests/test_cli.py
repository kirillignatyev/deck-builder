from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from deck_builder import cli
from deck_builder.builders.titles_digest import (
    DEFAULT_ATTRIBUTION_TEXT,
    DEFAULT_SUPTITLE_TEXT,
    DEFAULT_TITLE_TEXT,
)

runner = CliRunner()


@pytest.fixture
def input_file(tmp_path):
    path = tmp_path / "books.xlsx"
    path.touch()
    return path


@pytest.fixture
def factory(monkeypatch):
    digest = Mock()
    digest.build.return_value = digest
    factory = Mock(return_value=digest)
    monkeypatch.setattr(cli.TitlesDigest, "from_excel", factory)
    return factory


@pytest.mark.parametrize("name", ["digest", "digest.pptx", "digest.PPTX", "digest.txt"])
def test_build(input_file, tmp_path, factory, name):
    output = tmp_path / name
    result = runner.invoke(cli.app, [str(input_file), str(output)])
    assert result.exit_code == 0, result.output
    factory.assert_called_once_with(str(input_file))
    factory.return_value.build.assert_called_once_with(
        title_text=DEFAULT_TITLE_TEXT,
        suptitle_text=DEFAULT_SUPTITLE_TEXT,
        attribution_text=DEFAULT_ATTRIBUTION_TEXT,
    )
    expected = (
        output if output.suffix.lower() == ".pptx" else output.with_suffix(".pptx")
    )
    factory.return_value.to_pptx.assert_called_once_with(expected)
    assert str(expected) in result.output


def test_options(input_file, tmp_path, factory):
    result = runner.invoke(
        cli.app,
        [
            str(input_file),
            str(tmp_path / "out.pptx"),
            "--title",
            "Title",
            "--suptitle",
            "Sub",
            "--attribution",
            "By",
        ],
    )
    assert result.exit_code == 0
    factory.return_value.build.assert_called_once_with(
        title_text="Title", suptitle_text="Sub", attribution_text="By"
    )


@pytest.mark.parametrize("args", [[], ["missing.xlsx", "out.pptx"]])
def test_invalid_arguments(args, factory):
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 2
    factory.assert_not_called()


def test_input_directory(tmp_path, factory):
    assert (
        runner.invoke(cli.app, [str(tmp_path), str(tmp_path / "out.pptx")]).exit_code
        == 2
    )
    factory.assert_not_called()


def test_invalid_schema(input_file, tmp_path, factory):
    factory.return_value.df = None
    result = runner.invoke(cli.app, [str(input_file), str(tmp_path / "out")])
    assert result.exit_code == 1
    assert "столбцы" in result.output
    factory.return_value.build.assert_not_called()
    factory.return_value.to_pptx.assert_not_called()


@pytest.mark.parametrize("stage", ["load", "build", "save"])
def test_error(input_file, tmp_path, factory, stage):
    target = {
        "load": factory,
        "build": factory.return_value.build,
        "save": factory.return_value.to_pptx,
    }[stage]
    target.side_effect = OSError("broken")
    result = runner.invoke(cli.app, [str(input_file), str(tmp_path / "out")])
    assert result.exit_code == 1
    assert "broken" in result.output
    assert "Сохранено" not in result.output


def test_same_file(tmp_path, factory):
    path = tmp_path / "same.pptx"
    path.touch()
    assert runner.invoke(cli.app, [str(path), str(path)]).exit_code == 2
    factory.assert_not_called()


def test_help(factory):
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    assert "input_file" in result.output.lower()
    assert "output_file" in result.output.lower()
    factory.assert_not_called()
