import importlib
import logging
import sys


def get_banner(project_name: str) -> str:
    width = 73
    version = importlib.metadata.version(project_name)

    project_name_for_banner = "".join(
        [
            project_name,
            " " * (width - 11 - len(project_name)),
        ],
    )

    project_version_for_banner = "".join(
        [
            version,
            " " * (width - 11 - len(version)),
        ],
    )

    return """

  ██████████████████████████████████████████████████████████████████████████████
 ░█▌                                                                          ▐█
 ░█▌            █████       ███  ████  ████      █████                        ▐█
 ░█▌           ░░███       ░░░  ░░███ ░░███     ░░███                         ▐█
 ░█▌    ██████  ░███████   ████  ░███  ░███   ███████   ██████  █████ █████   ▐█
 ░█▌   ███░░███ ░███░░███ ░░███  ░███  ░███ ░███ ░███ ░███░░███ ░███  ░███    ▐█
 ░█▌  ░███ ░░░  ░███ ░███  ░███  ░███  ░███ ░███ ░███ ░███████  ░███  ░███    ▐█
 ░█▌  ░███  ███ ░███ ░███  ░███  ░███  ░███ ░███ ░███ ░███░░░   ░░███ ███     ▐█
 ░█▌  ░░██████  ████ █████ █████ █████ █████░░████████░░██████   ░░█████      ▐█
 ░█▌   ░░░░░░  ░░░░ ░░░░░ ░░░░░ ░░░░░ ░░░░░  ░░░░░░░░  ░░░░░░     ░░░░░       ▐█
 ░█▌                                                                          ▐█
 ░█▌   project: {project_name_for_banner}▐█
 ░█▌   version: {project_version_for_banner}▐█
 ░█▌                                                                          ▐█
 ░██████████████████████████████████████████████████████████████████████████████
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """.format(
        project_name_for_banner=project_name_for_banner,
        project_version_for_banner=project_version_for_banner,
    )


def get_logging_config() -> dict:
    return {
        "level": logging.INFO,
        "stream": sys.stdout,
        "format": "%(levelname).1s :: %(asctime)s :: %(message)s",
    }
