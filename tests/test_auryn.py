import unittest
from fantasia.auryn import Auryn, Wish


class TestAuryn(unittest.TestCase):
    def test_inscription(self):
        auryn = Auryn()
        self.assertEqual(auryn.INSCRIPTION, "DO WHAT THOU WILT")

    def test_grant_wish(self):
        auryn = Auryn("Bastian")
        wish = auryn.grant_wish("Build a terminal bridge to the Ivory Tower")
        self.assertEqual(wish.status, "granted")
        self.assertTrue(wish.wish_id.startswith("wish_"))
        self.assertEqual(auryn.wish_count, 1)

    def test_memory_anchor(self):
        auryn = Auryn()
        initial_anchor = auryn.remaining_memory_anchor
        auryn.grant_wish("First wish")
        self.assertEqual(auryn.remaining_memory_anchor, initial_anchor - 1)

    def test_talisman_signature(self):
        auryn = Auryn()
        sig = auryn.talisman_signature()
        self.assertEqual(len(sig), 16)
        auryn.grant_wish("Change state")
        self.assertNotEqual(auryn.talisman_signature(), sig)


if __name__ == "__main__":
    unittest.main()
