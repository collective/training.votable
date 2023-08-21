# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("training.votable")

ViewVotesPermission = "training.votable: View Votes"
CanVotePermission = "training.votable: Can Vote"
ClearVotesPermission = "training.votable: Clear Votes"
