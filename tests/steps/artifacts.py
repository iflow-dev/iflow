"""
Step definitions for artifact-related functionality.
"""

from radish import then
from controls import Tile


@then(r"I see the artifact #{key:S}")
def i_see_the_artifact(step, key):
    """Verify that the given artifact exists on the page."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.debug(f"I see the artifact #{key}")
    
    from radish import world
    tile = Tile(key)
    tile.locate(world.driver)


@then(r"I do not see the artifact #{key:S}")
def i_do_not_see_the_artifact(step, key):
    """Verify that the given artifact does not exist on the page."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.debug(f"I do not see the artifact #{key}")
    
    from radish import world
    tile = Tile(key)
    
    # Use exists() method which returns False if element not found
    if tile.exists(world.driver):
        raise AssertionError(f"Artifact #{key} was found but should not exist")
    
    logger.debug(f"Artifact #{key} correctly not found")
