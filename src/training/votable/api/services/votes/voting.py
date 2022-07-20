# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import Unauthorized
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

from training.votable import DoVotePermission
from training.votable.behaviors.votable import IVotable


class VotingPost(Service):
    """Vote for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_vote = not api.user.is_anonymous() and api.user.has_permission(
            DoVotePermission, obj=self.context
        )
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
        can_vote = not api.user.is_anonymous() and api.user.has_permission(
            DoVotePermission, obj=self.context
        )
        if not can_vote:
            raise Unauthorized("User not authorized to delete votes.")
        voting = IVotable(self.context)
        voting.clear()
        return vote_info(self.context, self.request)


class VotingGet(Service):
    """Voting information about the current object"""

    def reply(self):
        return vote_info(self.context, self.request)


def vote_info(obj, request=None):
    """Returns voting information about the given object."""
    if not request:
        request = getRequest()
    voting = IVotable(obj)
    can_vote = not api.user.is_anonymous() and api.user.has_permission(
        DoVotePermission, obj=obj
    )
    can_clear_votes = any(
        role in api.user.get_roles() for role in ["Manager", "Site Manager"]
    )
    info = {
        "average_vote": voting.average_vote(),
        "total_votes": voting.total_votes(),
        "has_votes": voting.has_votes(),
        "already_voted": voting.already_voted(request),
        "can_vote": can_vote,
        "can_clear_votes": can_clear_votes,
    }
    return info
