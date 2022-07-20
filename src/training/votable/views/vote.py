# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from training.votable.behaviors.votable import IVotable


class Vote(BrowserView):
    def __call__(self, rating):
        voting = IVotable(self.context)
        voting.vote(rating, self.request)
        notify(ObjectModifiedEvent(self.context, "A vote has been submitted"))
        return "success"
