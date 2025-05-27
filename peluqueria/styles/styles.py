from enum import Enum
from typing import Any


class Colors(Enum):
    PRIMARY_COLOR = "#D4AF37"
    PRIMARY_HOVER = "#aa7a24"
    OUTLINE_HOVER = "#382010"
    CUSTOM_WHITE = "#F5F5F5"
    PARAGRAPH_COLOR = "#4a4a4a"


BASE: dict[str, Any] = {
    "background": Colors.CUSTOM_WHITE.value,
}

# NAVBAR LINK items
NAVBAR_LINK: dict[str, Any] = {
    "position": "relative",
    "font_weight": "normal",
    "color": Colors.CUSTOM_WHITE.value,
    "_after": {
        "content": "''",
        "position": "absolute",
        "width": "0%",
        "height": "2px",
        "bottom": "0",
        "left": "0",
        "background_color": Colors.PRIMARY_COLOR.value,
        "transition": "width 0.3s ease, color 0.3s ease",
    },
    "_hover": {"color": Colors.PRIMARY_COLOR.value, "_after": {"width": "100%"}},
}

# SIMPLE button
SIMPLE_BUTTON: dict[str, Any] = {
    "padding_y": "0.6rem",
    "border" : "none",
    "font_size": "1rem",
    "background" : "transparent",
    "color" : Colors.CUSTOM_WHITE.value,
    "transition" : "color 0.3s ease",
    "_hover" : {
        "color" : Colors.PRIMARY_COLOR.value
    }
}

# OUTLINE button
OUTLINE_BUTTON: dict[str, Any] = {
    "background": "transparent",
    "border": "2px solid " + Colors.PRIMARY_COLOR.value,
    "padding_y": "0.6rem",
    "padding_x": "2rem",
    "border_radius" : "2rem",
    "font_weight": "normal",
    "color": Colors.PRIMARY_COLOR.value,
    "font_size": "1rem",
    "transition": "background 0.3s ease, color 0.3s ease",
    "_hover": {
        "background": Colors.PRIMARY_COLOR.value,
        "color" : Colors.CUSTOM_WHITE.value
    },
}

# SOLID button
SOLID_BUTTON: dict[str, Any] = {
    "background": Colors.PRIMARY_COLOR.value,
    "border": "1px solid " + Colors.PRIMARY_COLOR.value,
    "padding_y": "1rem",
    "padding_x": "1rem",
    "border_radius" : "2rem",
    "font_weight": "normal",
    "color": Colors.CUSTOM_WHITE.value,
    "font_size": "1rem",
    "transition": "background 0.3s ease, color 0.3s ease",
    "_hover": {
        "background": Colors.PRIMARY_HOVER.value,
        "border": "1px solid " + Colors.PRIMARY_HOVER.value,
    },
}

#OUTLINE BUTTON WHITE
OUTLINE_WHITE = {
    "background": "transparent",
    "border": "2px solid " + Colors.CUSTOM_WHITE.value,
    "padding_y": "1rem",
    "padding_x": "2rem",
    "border_radius" : "2rem",
    "font_weight": "normal",
    "color": Colors.CUSTOM_WHITE.value,
    "font_size": "1rem",
    "transition": "background 0.3s ease, color 0.3s ease",
    "_hover": {
        "background": Colors.CUSTOM_WHITE.value,
        "color" : Colors.PRIMARY_COLOR.value
    },
}

# CUSTOM INPUT
CUSTOM_INPUT: dict[str, Any] = {
    "border_radius" : "0.5rem",
    "border" : f"1px solid {Colors.PARAGRAPH_COLOR.value}",
    "padding_y" : "0.4rem",
    "padding_x" : "0.5rem",
    "transition" : "all 0.3s ease",
    "_focus": {
        "border" : f"1px solid {Colors.PRIMARY_COLOR.value}",
        "outline": f"1px solid {Colors.PRIMARY_COLOR.value}"
    },
}