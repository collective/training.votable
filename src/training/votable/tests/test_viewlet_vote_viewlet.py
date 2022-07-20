# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.dexterity.interfaces import IDexterityFTI
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter, queryUtility
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

from training.votable.interfaces import ITrainingVotableLayer
from training.votable.testing import (
    TRAINING_VOTABLE_FUNCTIONAL_TESTING,
    TRAINING_VOTABLE_INTEGRATION_TESTING,
)


class ViewletIntegrationTest(unittest.TestCase):

    layer = TRAINING_VOTABLE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST

        # Register behavior for type "Document"
        fti = queryUtility(IDexterityFTI, name="Document")
        behavior_list = [a for a in fti.behaviors]
        behavior_list.append("training.votable.votable")
        fti.behaviors = tuple(behavior_list)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Document", "other-document")
        api.content.create(self.portal, "News Item", "newsitem")

    def test_vote_viewlet_is_registered(self):
        view = BrowserView(self.portal["other-document"], self.request)
        manager_name = "plone.belowcontenttitle"
        alsoProvides(self.request, ITrainingVotableLayer)
        manager = queryMultiAdapter(
            (self.portal["other-document"], self.request, view),
            IViewletManager,
            manager_name,
            default=None,
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [
            v for v in manager.viewlets if v.__name__ == "vote-viewlet"
        ]  # NOQA: E501
        self.assertEqual(len(my_viewlet), 1)

    # XXX would be nice to have this test working:
    # def test_vote_viewlet_is_not_available_on_newsitem(self):
    #     view = BrowserView(self.portal['newsitem'], self.request)
    #     manager_name = 'plone.abovecontenttitle'
    #     alsoProvides(self.request, ITrainingVotableLayer)
    #     manager = queryMultiAdapter(
    #         (self.portal['newsitem'], self.request, view),
    #         IViewletManager,
    #         manager_name,
    #         default=None
    #     )
    #     self.assertIsNotNone(manager)
    #     manager.update()
    #     my_viewlet = [v for v in manager.viewlets if v.__name__ == 'vote-viewlet']  # NOQA: E501
    #     self.assertEqual(len(my_viewlet), 0)


class ViewletFunctionalTest(unittest.TestCase):

    layer = TRAINING_VOTABLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
