import json
import unittest

from application import translate_sections


class AppTest(unittest.TestCase):
    def test_translate_sections(self):
        sections = [
"""
Peace brothers and sisters
""",
"""
For Christmas, we preached that the incarnation is God’s main act of communication with us. Unlike TV ads, Instagram and Facebook where everything feels staged and good-looking, God communicates to us from reality, as the gospel of the birth of Jesus describes a much messier situation than we tend to perceive.
"""
        ]

        translated_sections = json.dumps(translate_sections(sections, "English", "Simplified Chinese"))

        # can't assert because the translation can be different every time
        print(translated_sections)


if __name__ == '__main__':
    unittest.main()
