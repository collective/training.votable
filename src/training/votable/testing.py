from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import training.votable  # noQA


class Layer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=training.votable)
        self.loadZCML("testing.zcml", package=training.votable)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "training.votable:default")
        applyProfile(portal, "training.votable:testing")


FIXTURE = Layer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="Training.VotableLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="Training.VotableLayer:FunctionalTesting",
)


ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="Training.VotableLayer:AcceptanceTesting",
)
