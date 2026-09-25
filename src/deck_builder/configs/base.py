from dataclasses import dataclass
from pathlib import Path

from pptx.dml.color import RGBColor
from pptx.util import Length

BLUE = RGBColor(14, 103, 161)
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)
BEIGE = RGBColor(246, 231, 224)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

LINGUA_LOGO = ASSETS_DIR / "logo_lingua.png"
LINGUA_ICON = ASSETS_DIR / "icon_lingua.png"


@dataclass(frozen=True)
class ColorsConfig:
    blue: RGBColor = BLUE
    white: RGBColor = WHITE
    black: RGBColor = BLACK
    beige: RGBColor = BEIGE


@dataclass(frozen=True)
class PresentationAssets:
    logo: Path = LINGUA_LOGO
    icon: Path = LINGUA_ICON


@dataclass(frozen=True)
class SlideSizeConfig:
    width: Length
    height: Length


@dataclass(frozen=True)
class SlideMarginsConfig:
    left: Length
    right: Length
    top: Length
    bottom: Length


@dataclass(frozen=True)
class TypographyConfig:
    font_family: str
    header_1: Length
    header_2: Length
    header_3: Length
    header_4: Length
    text: Length


@dataclass(frozen=True)
class TitleSlideConfig:
    logo_top: Length
    logo_height: Length
    title_top: Length
    suptitle_top: Length
    attribution_top: Length


@dataclass(frozen=True)
class BookInfoSlideConfig:
    text_box_width: Length
    text_box_left: Length

    author_top: Length
    title_top: Length
    annotation_top: Length

    reasons_accent_top: Length
    reasons_top: Length

    params_top: Length

    backdrop_left: Length
    backdrop_top: Length
    cover_left: Length
    cover_top: Length
    cover_max_width: Length
    cover_max_height: Length

    tags_left: Length
    tags_top: Length

    icon_height: Length
    icon_left: Length
    icon_top: Length


@dataclass(frozen=True)
class PresentationConfig:
    assets: PresentationAssets
    slide_size: SlideSizeConfig
    margins: SlideMarginsConfig
    typography: TypographyConfig
    colors: ColorsConfig
    title_slide: TitleSlideConfig
    book_info_slide: BookInfoSlideConfig
