"""Init and utils."""

from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "training.votable"

_ = MessageFactory(PACKAGE_NAME)

logger = logging.getLogger(PACKAGE_NAME)

ViewVotesPermission = "training.votable: View Votes"
CanVotePermission = "training.votable: Can Vote"
ClearVotesPermission = "training.votable: Clear Votes"
