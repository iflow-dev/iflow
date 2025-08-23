"""
Step definitions for artifact-related functionality.
"""

from radish import then
from bdd.controls import Tile
from bdd.logging_config import logger


@then(r"I see the artifact #{key:S}")
def i_see_the_artifact(step, key):
    logger.debug(f"I see the artifact #{key}")

    tile = Tile(key)
    tile.locate()


@then(r"I do not see the artifact #{key:S}")
def i_do_not_see_the_artifact(step, key):
    logger.debug(f"I do not see the artifact #{key}")

    tile = Tile(key)

    if tile.exists():
        raise AssertionError(f"Artifact #{key} was found but should not exist")

    logger.debug(f"Artifact #{key} correctly not found")
