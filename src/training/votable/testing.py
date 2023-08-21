# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
)
from plone.testing import z2
from plone.testing.zope import WSGI_SERVER_FIXTURE

import training.votable


def enable_votable_behavior_for_document(portal):
    # TODO enable votable behavior for type document
    pass


class TrainingVotableLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=training.votable)

        self.loadZCML("testing.zcml", package=training.votable)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "training.votable:default")
        applyProfile(portal, "training.votable:testing")
        enable_votable_behavior_for_document(portal)


TRAINING_VOTABLE_FIXTURE = TrainingVotableLayer()


TRAINING_VOTABLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TRAINING_VOTABLE_FIXTURE,),
    name="TrainingVotableLayer:IntegrationTesting",
)


TRAINING_VOTABLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TRAINING_VOTABLE_FIXTURE, WSGI_SERVER_FIXTURE),
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
