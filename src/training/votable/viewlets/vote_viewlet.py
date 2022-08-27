# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.utils import getToolByName

from training.votable import (
    ClearVotesPermission,
    CanVotePermission,
    ViewVotesPermission,
)
from training.votable.behaviors.votable import IVotable


class VoteViewlet(ViewletBase):
    vote = None
    can_clear_votes = None
    can_view_votes = None
    can_vote = None

    def update(self):
        super(VoteViewlet, self).update()

        membership_tool = getToolByName(self.context, "portal_membership")
        self.can_view_votes = membership_tool.checkPermission(
            ViewVotesPermission, self.context
        )
        self.can_vote = membership_tool.checkPermission(CanVotePermission, self.context)
        self.can_clear_votes = membership_tool.checkPermission(
            ClearVotesPermission, self.context
        )

        if self.can_view_votes:
            self.vote = IVotable(self.context)

    def voted(self):
        return self.vote.already_voted(self.request)

    def average(self):
        return self.vote.average_vote()

    def has_votes(self):
        return self.vote.has_votes()
