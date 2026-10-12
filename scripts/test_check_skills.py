"""Regression coverage for frontmatter that previously passed the regex check."""

import unittest
from pathlib import Path

from check_skills import check_frontmatter


class FrontmatterTests(unittest.TestCase):
    def check(self, frontmatter):
        problems = []
        check_frontmatter(
            Path("skills/example/SKILL.md"),
            f"---\n{frontmatter}\n---\n\n# Example\n",
            lambda path, message: problems.append(message),
        )
        return problems

    def test_rejects_unquoted_colon_in_description(self):
        problems = self.check(
            "name: example\n"
            "description: Publish through Publora: text, images and video. "
            "Not for analytics or other platforms."
        )
        self.assertTrue(any("invalid YAML" in p for p in problems), problems)

    def test_accepts_quoted_and_folded_descriptions(self):
        description = (
            "Publish through Publora: text, images and video. "
            "Not for analytics or other platforms."
        )
        for value in (f'"{description}"', f">-\n  {description}"):
            with self.subTest(value=value):
                self.assertEqual(self.check(f"name: example\ndescription: {value}"), [])

    def test_checks_parsed_description_length(self):
        problems = self.check("name: example\ndescription: >-\n  Too short.")
        self.assertTrue(any("description is 10 chars" in p for p in problems), problems)

    def test_rejects_non_mapping_and_non_string_fields(self):
        for frontmatter in (
            "- example",
            "name: example\ndescription: [one, two]",
            "name: false\ndescription: text",
            "name: example",
        ):
            with self.subTest(frontmatter=frontmatter):
                self.assertTrue(self.check(frontmatter))

    def test_checks_quoted_name_against_folder(self):
        description = "Use this skill to publish and schedule posts through Publora."
        self.assertEqual(self.check(f'name: "example"\ndescription: "{description}"'), [])
        problems = self.check(f'name: "another"\ndescription: "{description}"')
        self.assertTrue(any("does not match folder" in p for p in problems), problems)

    def test_rejects_python_object_tags(self):
        self.assertTrue(self.check("!!python/object:builtins.object {}"))


if __name__ == "__main__":
    unittest.main()
