from pptx.util import Mm, Pt

from deck_builder.configs.base import (
    BookInfoSlideConfig,
    ColorsConfig,
    PresentationAssets,
    PresentationConfig,
    SlideMarginsConfig,
    SlideSizeConfig,
    TitleSlideConfig,
    TypographyConfig,
)

TITLES_DIGEST_CONFIG = PresentationConfig(
    assets=PresentationAssets(),
    slide_size=SlideSizeConfig(
        width=Mm(254),
        height=Mm(143),
    ),
    margins=SlideMarginsConfig(
        left=Mm(10),
        right=Mm(10),
        top=Mm(4),
        bottom=Mm(4),
    ),
    typography=TypographyConfig(
        font_family="IBM Plex Sans",
        header_1=Pt(36),
        header_2=Pt(24),
        header_3=Pt(12),
        header_4=Pt(10),
        text=Pt(8),
    ),
    colors=ColorsConfig(),
    title_slide=TitleSlideConfig(
        logo_top=Mm(22.5),
        logo_height=Mm(40),
        title_top=Mm(60),
        suptitle_top=Mm(78),
        attribution_top=Mm(100),
    ),
    book_info_slide=BookInfoSlideConfig(
        text_box_width=Mm(127),
        text_box_left=Mm(117),
        author_top=Mm(2.5),
        title_top=Mm(7.5),
        annotation_top=Mm(25),
        reasons_accent_top=Mm(95),
        reasons_top=Mm(100),
        params_top=Mm(130),
        backdrop_left=Mm(10),
        backdrop_top=Mm(22.5),
        cover_left=Mm(12.5),
        cover_top=Mm(25),
        cover_max_width=Mm(87.5),
        cover_max_height=Mm(116.5),
        tags_left=Mm(10),
        tags_top=Mm(7.5),
        icon_height=Mm(9.8),
        icon_left=Mm(246),
        icon_top=Mm(130.6),
    ),
)
