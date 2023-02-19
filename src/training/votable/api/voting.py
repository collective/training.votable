# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import Unauthorized
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

from training.votable import (
    CanVotePermission,
    ClearVotesPermission,
    ViewVotesPermission,
)
from training.votable.behaviors.votable import IVotable


class VotingGet(Service):
    """Voting information about the current object"""

    def reply(self):
        can_view_votes = api.user.has_permission(ViewVotesPermission, obj=self.context)
        if not can_view_votes:
            raise Unauthorized("User not authorized to view votes.")
        return vote_info(self.context, self.request)


class VotingPost(Service):
    """Vote for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_vote = api.user.has_permission(CanVotePermission, obj=self.context)
        if not can_vote:
            raise Unauthorized("User not authorized to vote.")
        voting = IVotable(self.context)
        data = json_body(self.request)
        vote = data["rating"]
        voting.vote(vote, self.request)

        return vote_info(self.context, self.request)


class VotingDelete(Service):
    """Unlock an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_clear_votes = api.user.has_permission(
            ClearVotesPermission, obj=self.context
        )
        if not can_clear_votes:
            raise Unauthorized("User not authorized to clear votes.")
        voting = IVotable(self.context)
        voting.clear()
        return vote_info(self.context, self.request)


def vote_info(obj, request=None):
    """Returns voting information about the given object."""
    if not request:
        request = getRequest()
    voting = IVotable(obj)
    info = {
        "average_vote": voting.average_vote(),
        "total_votes": voting.total_votes(),
        "has_votes": voting.has_votes(),
        "already_voted": voting.already_voted(request),
        "can_vote": api.user.has_permission(CanVotePermission, obj=obj),
        "can_clear_votes": api.user.has_permission(ClearVotesPermission, obj=obj),
    }
    return info
