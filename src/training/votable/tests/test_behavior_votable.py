# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import TEST_USER_ID, setRoles
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

from training.votable.behaviors.votable import IVotableMarker
from training.votable.testing import TRAINING_VOTABLE_INTEGRATION_TESTING  # noqa


class VotableIntegrationTest(unittest.TestCase):

    layer = TRAINING_VOTABLE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_votable(self):
        behavior = getUtility(IBehavior, "training.votable.votable")
        self.assertEqual(
            behavior.marker,
            IVotableMarker,
        )
