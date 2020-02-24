from dataclasses import dataclass

import yaml
from typing_extensions import Final


@dataclass
class Settings:
    _config_file = yaml.safe_load(open("./config.yml"))

    MUSE_ADDRESS: Final[str] = _config_file["Muse"]["MAC_Address"]
