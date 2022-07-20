# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import getToolByName

from training.votable import DoVotePermission
from training.votable.behaviors.votable import IVotable


class VoteViewlet(ViewletBase):
    vote = None
    is_manager = None
    can_vote = None

    def update(self):
        super(VoteViewlet, self).update()

        if self.vote is None:
            self.vote = IVotable(self.context)
        if self.is_manager is None:
            membership_tool = getToolByName(self.context, "portal_membership")
            self.is_manager = membership_tool.checkPermission(
                ViewManagementScreens, self.context
            )
            self.can_vote = membership_tool.checkPermission(
                DoVotePermission, self.context
            )

    def voted(self):
        return self.vote.already_voted(self.request)

    def average(self):
        return self.vote.average_vote()

    def has_votes(self):
        return self.vote.has_votes()
