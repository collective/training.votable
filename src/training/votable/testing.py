# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2, zope

# from zope.configuration import xmlconfig


class TrainingVotableLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)

        import plone.restapi

        self.loadZCML(package=plone.restapi)

        # training.votable
        import training.votable

        self.loadZCML(package=training.votable)
        self.loadZCML("testing.zcml", package=training.votable)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "training.votable:default")
        applyProfile(portal, "training.votable:testing")


TRAINING_VOTABLE_FIXTURE = TrainingVotableLayer()


TRAINING_VOTABLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TRAINING_VOTABLE_FIXTURE,),
    name="TrainingVotableLayer:IntegrationTesting",
)


TRAINING_VOTABLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TRAINING_VOTABLE_FIXTURE, zope.WSGI_SERVER_FIXTURE),
    name="TrainingVotableLayer:FunctionalTesting",
)


TRAINING_VOTABLE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TRAINING_VOTABLE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="TrainingVotableLayer:AcceptanceTesting",
)
