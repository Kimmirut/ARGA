from dataclasses import dataclass


@dataclass
class Config:
    font_name: str
    year: str


def load_config() -> Config:
    return Config(
        font_name=font_name,
        year=year
    )


font_name = 'DejaVu'
year = 2024
