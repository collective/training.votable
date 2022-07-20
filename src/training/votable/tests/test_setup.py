# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles

from training.votable.testing import TRAINING_VOTABLE_INTEGRATION_TESTING  # noqa: E501

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that training.votable is properly installed."""

    layer = TRAINING_VOTABLE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if training.votable is installed."""
        self.assertTrue(self.installer.is_product_installed("training.votable"))

    def test_browserlayer(self):
        """Test that ITrainingVotableLayer is registered."""
        from plone.browserlayer import utils

        from training.votable.interfaces import ITrainingVotableLayer

        self.assertIn(ITrainingVotableLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TRAINING_VOTABLE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("training.votable")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if training.votable is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("training.votable"))

    def test_browserlayer_removed(self):
        """Test that ITrainingVotableLayer is removed."""
        from plone.browserlayer import utils

        from training.votable.interfaces import ITrainingVotableLayer

        self.assertNotIn(ITrainingVotableLayer, utils.registered_layers())
