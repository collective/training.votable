from pytest_plone import fixtures_factory
from training.votable.testing import ACCEPTANCE_TESTING
from training.votable.testing import FUNCTIONAL_TESTING
from training.votable.testing import INTEGRATION_TESTING


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (ACCEPTANCE_TESTING, "acceptance"),
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)
