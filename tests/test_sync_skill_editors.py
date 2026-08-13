import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import sync_skill_editors as sync  # noqa: E402


class TestUpsertEntity(unittest.TestCase):
    def test_uses_post_upsert_without_patch_query_params(self):
        with patch.object(sync, "http_json") as http_json:
            sync.upsert_entity(
                "port-token",
                "skill",
                "revitalb-port/skills-registry-demo/skills/foo/SKILL.md",
                "alice",
                "2026-08-13T12:00:00Z",
            )

        http_json.assert_called_once()
        args, kwargs = http_json.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(
            args[1],
            "https://api.port.io/v1/blueprints/skill/entities?upsert=true",
        )
        self.assertNotIn("merge=", args[1])
        self.assertNotIn("create_missing_related_entities=", args[1])
        self.assertEqual(
            kwargs["body"],
            {
                "identifier": "revitalb-port/skills-registry-demo/skills/foo/SKILL.md",
                "properties": {
                    "lastEditor": "alice",
                    "lastEditedAt": "2026-08-13T12:00:00Z",
                },
            },
        )

    def test_includes_relations_when_provided(self):
        with patch.object(sync, "http_json") as http_json:
            relations = {"skills": ["repo/skills/a/SKILL.md"]}
            sync.upsert_entity(
                "port-token",
                "agentPlugin",
                "repo/my-plugin",
                "bob",
                "2026-08-13T12:00:00Z",
                relations=relations,
            )

        body = http_json.call_args.kwargs["body"]
        self.assertEqual(body["relations"], relations)


class TestGetPluginSkillIdentifiers(unittest.TestCase):
    def test_collects_skill_identifiers_from_symlinks(self):
        repo = "revitalb-port/skills-registry-demo"
        plugin_name = "code-quality-toolkit"
        identifiers = sync.get_plugin_skill_identifiers(repo, plugin_name)

        self.assertTrue(identifiers)
        for identifier in identifiers:
            self.assertTrue(identifier.startswith(f"{repo}/skills/"))
            self.assertTrue(identifier.endswith("/SKILL.md"))


class TestHttpJson(unittest.TestCase):
    def test_logs_http_error_body(self):
        import urllib.error

        error = urllib.error.HTTPError(
            "https://api.port.io/v1/blueprints/skill/entities",
            422,
            "Unprocessable Entity",
            {},
            MagicMock(read=MagicMock(return_value=b'{"message":"invalid"}')),
        )

        with patch("urllib.request.urlopen", side_effect=error):
            with patch("sys.stderr") as stderr:
                with self.assertRaises(urllib.error.HTTPError):
                    sync.http_json("POST", "https://example.com", body={})

        stderr.write.assert_called()
        logged = "".join(call.args[0] for call in stderr.write.call_args_list)
        self.assertIn("HTTP 422", logged)
        self.assertIn("invalid", logged)


if __name__ == "__main__":
    unittest.main()
