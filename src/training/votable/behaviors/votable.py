from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone import api
from plone import schema
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


"""
The key must be unique.
Using the class name with the complete module name
is a good idea.
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

    votes = schema.Dict(
        title="Vote info",
        key_type=schema.TextLine(title="Voted number"),
        value_type=schema.Int(title="Voted so often"),
        default={},
        missing_value={},
        required=False,
    )
    voted = schema.List(
        title="List of users who voted",
        value_type=schema.TextLine(),
        default=[],
        missing_value=[],
        required=False,
    )

    if not api.env.debug_mode():
        form.omitted("votes")
        form.omitted("voted")

    directives.fieldset(
        "debug",
        label="debug",
        fields=("votes", "voted"),
    )

    def vote(request):
        """
        Store the vote information and store the user(name)
        to ensure that the user does not vote twice.
        """

    def average_vote():
        """
        Return the average voting for an item.
        """

    def has_votes():
        """
        Return whether anybody ever voted for this item.
        """

    def already_voted(request):
        """
        Return the information whether a person already voted.
        """

    def clear():
        """
        Clear the votes. Should only be called by admins.
        """


@implementer(IVotable)
@adapter(IVotableMarker)
class Votable:
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

    # getter
    @property
    def votes(self):
        return self.annotations["votes"]

    # setter
    # def votes(self, value):
    #     """We do not define a setter.
    #     Function 'vote' is the only one that shall set attributes
    #     of the context object."""
    #     self.annotations["votes"] = value

    # getter
    @property
    def voted(self):
        return self.annotations["voted"]

    # setter
    # def voted(self, value):
    #     self.annotations["voted"] = value

    def vote(self, vote, request):
        if self.already_voted(request):
            raise KeyError("You may not vote twice.")
        vote = int(vote)
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
