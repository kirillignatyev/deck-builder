from pathlib import Path

from pptx.presentation import Presentation as PresentationType


def to_pptx(
    presentation: PresentationType,
    output_path: str | Path,
) -> None:
    path = Path(output_path)

    if path.suffix.lower() != ".pptx":
        path = path.with_suffix(".pptx")

    path.parent.mkdir(parents=True, exist_ok=True)
    presentation.save(str(path))
