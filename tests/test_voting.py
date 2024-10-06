from pkg_resources import resource_filename
from plone.app.testing import popGlobalRegistry
from plone.app.testing import pushGlobalRegistry
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import register_static_uuid_utility
from plone.restapi.testing import RelativeSession
from plone.restapi.tests.statictime import StaticTime
from plone.testing.zope import Browser
from training.votable.testing import FUNCTIONAL_TESTING
from zope.component.hooks import getSite

import collections
import json
import re
import transaction
import unittest


TUS_HEADERS = [
    "upload-offset",
    "upload-length",
    "upload-metadata",
    "tus-version",
    "tus-resumable",
    "tus-extension",
    "tus-max-size",
]

REQUEST_HEADER_KEYS = [
    "accept",
    "accept-language",
    "authorization",
    "lock-token",
    "prefer",
] + TUS_HEADERS

RESPONSE_HEADER_KEYS = ["content-type", "allow", "location"] + TUS_HEADERS


base_path = resource_filename("training.votable.tests", "http-examples")


# How do we open files?
open_kw = {"newline": "\n"}


def normalize_test_port(value):
    # When you run these tests in the Plone core development buildout,
    # the port number is random.  Normalize this to the default port.
    return re.sub(r"localhost:\d{5}", "localhost:55001", value)


def pretty_json(data):
    result = json.dumps(data, sort_keys=True, indent=4, separators=(",", ": "))
    # When generating the documentation examples on different machines,
    # it is all too easy to have differences in white space at the end of the line.
    # So strip space on the right.
    stripped = "\n".join([line.rstrip() for line in result.splitlines()])
    # Make sure there is an empty line at the end.
    # If you manually edit a file, many editors will automatically add such a line,
    # and you will see as diff: 'No newline at end of file'.  We do not want this.
    stripped += "\n"
    return normalize_test_port(stripped)


def save_request_and_response_for_docs(
    name, response, response_text_override="", request_text_override=""
):
    save_request_for_docs(name, response, request_text_override=request_text_override)
    filename = "{}/{}".format(base_path, "%s.resp" % name)
    with open(filename, "w", **open_kw) as resp:
        status = response.status_code
        reason = response.reason
        resp.write(f"HTTP/1.1 {status} {reason}\n")
        content_type = None
        for key, value in response.headers.items():
            if key.lower() in RESPONSE_HEADER_KEYS:
                if key.lower() == "location":
                    value = normalize_test_port(value)
                resp.write(f"{key.title()}: {value}\n")
                if key.lower() == "content-type":
                    content_type = value
        resp.write("\n")
        if response_text_override:
            resp.write(response_text_override)
            return
        if not response.text:
            # Empty response.
            return
        if not (content_type and content_type.startswith("application/json")):
            resp.write(response.text)
            return
        # Use pretty_json as a normalizer, especially for line endings.
        resp.write(pretty_json(response.json()))


def save_request_for_docs(name, response, request_text_override=""):
    filename = "{}/{}".format(base_path, "%s.req" % name)
    with open(filename, "w", **open_kw) as req:
        req.write(
            "{} {} HTTP/1.1\n".format(
                response.request.method, response.request.path_url
            )
        )
        ordered_request_headers = collections.OrderedDict(
            sorted(response.request.headers.items())
        )
        for key, value in ordered_request_headers.items():
            if key.lower() in REQUEST_HEADER_KEYS:
                req.write(f"{key.title()}: {value}\n")
        if response.request.body:
            # If request has a body, make sure to set Content-Type header
            if "content-type" not in REQUEST_HEADER_KEYS:
                content_type = response.request.headers["Content-Type"]
                req.write("Content-Type: %s\n" % content_type)

            req.write("\n")

            # Pretty print JSON request body
            if content_type == "application/json" and not request_text_override:
                json_body = json.loads(response.request.body)
                body = pretty_json(json_body)
                # Make sure Content-Length gets updated, just in case we
                # ever decide to dump that header
                response.request.prepare_body(data=body, files=None)

            req.flush()
            body = request_text_override or response.request.body
            if isinstance(body, str) or not hasattr(req, "buffer"):
                req.write(body)
            else:
                req.buffer.seek(0, 2)
                req.buffer.write(body)


class TestVotingBase(unittest.TestCase):
    def setUp(self):
        self.statictime = self.setup_with_context_manager(StaticTime())

        self.app = self.layer["app"]
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        setattr(self.portal, "_plone.uuid", "55c25ebc220d400393574f37d648727c")

        # Register custom UUID generator to produce stable UUIDs during tests
        pushGlobalRegistry(getSite())
        register_static_uuid_utility(prefix="SomeUUID")

        self.api_session = RelativeSession(self.portal_url, test=self)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization", f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}"
        )

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def setup_with_context_manager(self, cm):
        """Use a contextmanager to setUp a test case.

        Registering the cm's __exit__ as a cleanup hook *guarantees* that it
        will be called after a test run, unlike tearDown().

        This is used to make sure plone.restapi never leaves behind any time
        freezing monkey patches that haven't gotten reverted.
        """
        val = cm.__enter__()
        self.addCleanup(cm.__exit__, None, None, None)
        return val

    def tearDown(self):
        popGlobalRegistry(getSite())
        self.api_session.close()


class TestVoting(TestVotingBase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def create_document(self):
        self.portal.invokeFactory("Document", id="talk-python")
        document = self.portal["talk-python"]
        document.title = "What's new in Python"
        document.description = "New features, tips and tricks."
        return document

    def test_documentation_voting(self):
        talk_python = self.create_document()
        transaction.commit()

        self.assertEqual(self.portal["talk-python"].title, "What's new in Python")

        response = self.api_session.get(talk_python.absolute_url())
        save_request_and_response_for_docs("talk_get_content", response)

        # Get votes of talk
        response = self.api_session.get(f"{talk_python.absolute_url()}/@votes")
        save_request_and_response_for_docs("talk_get_votes", response)
        response = response.json()
        self.assertEqual(response["average_vote"], 0)

        # Vote on talk
        response = self.api_session.post(
            f"{talk_python.absolute_url()}/@votes",
            json={"rating": 1},
        )
        save_request_and_response_for_docs("talk_vote", response)
        response = response.json()
        self.assertEqual(response["average_vote"], 1)
