----------------
training.votable
----------------

Votable Behavior
----------------

*training.votable* is part of the training story of 'Mastering Plone Development' on https://training.plone.org/.
The training story takes the use case of selecting talk and training submissions for a conference.

*training.votable* adds the feature for registered users to vote for talks and trainings.
It started as a Plone Classic Add-On and is still valuable for Plone Classic with its viewlet for voting and reviewing.
The Add-On evolved to a Plone REST API provider for **Mastering Plone Development** roundtrip story on how to join backend and frontend if 
Plone REST API does not fit your needs, because you need more elaborated info from your backend.


Installation
------------

Install training.votable by adding it to your buildout::

    [buildout]

    ...

    eggs =
        training.votable


and then running ``bin/buildout``


Authors
-------

- Katja Süss, ksuess, k.suess@rohberg.ch
- Patrik Gerken, do3cc
- Philip Bauer, pbauer, bauer@starzel.de


Contributors
------------


Contribute
----------

- Issue Tracker: https://github.com/collective/training.votable/issues
- Source Code: https://github.com/collective/training.votable
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know. https://community.plone.org/


License
-------

The project is licensed under the GPLv2.
