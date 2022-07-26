# -*- coding: utf-8 -*-

from hashlib import md5

from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone import api, schema
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives, model
from Products.CMFPlone.utils import safe_bytes
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import Interface, implementer, provider

"""
The key must be unique. Using the class name with the complete module name
is a good idea. But be careful, you might want to change the key if you move
the location to a different place. Else you won't find your own annotations
"""
KEY = "training.votable.behaviors.votable.Votable"


class IVotableMarker(Interface):
    """Marker interface for content types or instances that should be votable"""

    pass


@provider(IFormFieldProvider)
class IVotable(model.Schema):
    """Behavior interface for the votable behavior

    IVotable(object) returns the adapted object with votable behavior
    """

    if not api.env.debug_mode():
        form.omitted("votes")
        form.omitted("voted")

    directives.fieldset(
        "debug",
        label="debug",
        fields=("votes", "voted"),
    )

    votes = schema.Dict(
        title="Vote info",
        key_type=schema.TextLine(title="Voted number"),
        value_type=schema.Int(title="Voted so often"),
        default={},
        missing_value={},
        required=False,
    )
    voted = schema.List(
        title="Vote hashes",
        value_type=schema.TextLine(),
        default=[],
        missing_value=[],
        required=False,
    )

    def vote(request):
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """

    def average_vote():
        """
        Return the average voting for an item
        """

    def has_votes():
        """
        Return whether anybody ever voted for this item
        """

    def already_voted(request):
        """
        Return the information wether a person already voted.
        This is not very high level and can be tricked out easily
        """

    def clear():
        """
        Clear the votes. Should only be called by admins
        """


@implementer(IVotable)
@adapter(IVotableMarker)
class Votable(object):
    """Adapter implementing the votable behavior"""

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            # You know what happens if we don't use persistent classes here?
            annotations[KEY] = PersistentDict(
                {"voted": PersistentList(), "votes": PersistentDict()}
            )
        self.annotations = annotations[KEY]

    @property
    def votes(self):
        return self.annotations["votes"]

    @votes.setter
    def votes(self, value):
        self.annotations["votes"] = value

    @property
    def voted(self):
        return self.annotations["voted"]

    @voted.setter
    def voted(self, value):
        self.annotations["voted"] = value

    def vote(self, vote, request):
        vote = int(vote)
        if self.already_voted(request):
            # Exceptions can create ugly error messages. If you or your user
            # can't resolve the error, you should not catch it.
            # Transactions can throw errors too.
            # What happens if you catch them?
            raise KeyError("You may not vote twice")
        current_user = api.user.get_current()
        self.annotations["voted"].append(current_user.id)
        votes = self.annotations.get("votes", {})
        if vote not in votes:
            votes[vote] = 1
        else:
            votes[vote] += 1

    def total_votes(self):
        return sum(self.annotations.get("votes", {}).values())

    def average_vote(self):
        total_votes = sum(self.annotations.get("votes", {}).values())
        if total_votes == 0:
            return 0
        total_points = sum(
            [
                vote * count
                for (vote, count) in self.annotations.get("votes", {}).items()
            ]
        )
        return float(total_points) / total_votes

    def has_votes(self):
        return len(self.annotations.get("votes", {})) != 0

    def already_voted(self, request):
        current_user = api.user.get_current()
        return current_user.id in self.annotations["voted"]

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict(
            {"voted": PersistentList(), "votes": PersistentDict()}
        )
        self.annotations = annotations[KEY]
