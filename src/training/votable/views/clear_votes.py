# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from training.votable.behaviors.votable import IVotable


class ClearVotes(BrowserView):
    def __call__(self):
        voting = IVotable(self.context)
        voting.clear()
        notify(
            ObjectModifiedEvent(
                self.context, "All votes of this item have been removed"
            )
        )
        return "success"
