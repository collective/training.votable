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

import training.votable


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

    def setUpPloneSite(self, portal):
        applyProfile(portal, "training.votable:default")


TRAINING_VOTABLE_FIXTURE = TrainingVotableLayer()


TRAINING_VOTABLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TRAINING_VOTABLE_FIXTURE,),
    name="TrainingVotableLayer:IntegrationTesting",
)


TRAINING_VOTABLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TRAINING_VOTABLE_FIXTURE,),
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
