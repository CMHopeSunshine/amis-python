from pathlib import Path
from string import Template
from typing import Literal

from .base import AmisNode

template_dir = Path(__file__).parent / "templates"


def render_as_html(
    amis: AmisNode,
    template_name: Literal["page.html", "app.html"] = "page.html",
    locale: str = "zh_CN",
    cdn: str = "https://unpkg.com",
    version: str = "latest",
    site_title: str = "AMIS",
    site_icon: str = "",
    theme: Literal["default", "antd", "ang"] = "default",
    custom_style: str = "",
    request_adaptor: str = "",
    response_adaptor: str = "",
    **kwargs,
) -> str:
    template = Template((template_dir / template_name).read_text(encoding="utf-8"))
    theme_css = f'<link href="{cdn}/amis@{version}/sdk/{theme}.css" rel="stylesheet"/>' if theme != "default" else ""

    return template.safe_substitute(
        {
            "AmisSchemaJson": amis.to_json(),
            "locale": locale,
            "cdn": cdn,
            "version": version,
            "site_title": site_title,
            "site_icon": site_icon,
            "theme_css": theme_css,
            "theme_name": "cxd" if theme == "default" else theme,
            "custom_style": custom_style,
            "request_adaptor": request_adaptor,
            "response_adaptor": response_adaptor,
            **kwargs,
        },
    )
