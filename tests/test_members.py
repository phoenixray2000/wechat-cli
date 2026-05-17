import types
import unittest
from unittest import mock

from click.testing import CliRunner

import wechat_cli.commands.members as members_module


class MembersCommandTest(unittest.TestCase):
    def test_text_format_lists_group_members(self):
        runner = CliRunner()
        app = types.SimpleNamespace(cache=object(), decrypted_dir="unused")

        with (
            mock.patch.object(members_module, "resolve_username", return_value="room@chatroom"),
            mock.patch.object(members_module, "get_contact_names", return_value={"room@chatroom": "Team Group"}),
            mock.patch.object(
                members_module,
                "get_group_members",
                return_value={
                    "owner": "Alice",
                    "members": [
                        {
                            "username": "wxid_alice",
                            "display_name": "Alice",
                            "remark": "Lead",
                        },
                        {
                            "username": "wxid_bob",
                            "display_name": "Bob",
                            "remark": "",
                        },
                    ],
                },
            ),
        ):
            result = runner.invoke(members_module.members, ["Team Group", "--format", "text"], obj=app)

        self.assertEqual(result.exit_code, 0, result.output or repr(result.exception))
        self.assertIn("Team Group 的群成员（共 2 人），群主: Alice:", result.output)
        self.assertIn("Alice  (wxid_alice)  备注: Lead", result.output)
        self.assertIn("Bob  (wxid_bob)", result.output)


if __name__ == "__main__":
    unittest.main()
