import unittest
from unittest.mock import patch
import io
from fantasia.cli import main
from fantasia import __version__


class TestCLI(unittest.TestCase):
    def test_version_flag(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.argv", ["fantasia", "--version"]):
                try:
                    main()
                except SystemExit as e:
                    self.assertEqual(e.code, 0)
            self.assertIn(__version__, fake_out.getvalue())

    def test_demo_command(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.argv", ["fantasia", "demo"]):
                main()
            out = fake_out.getvalue()
            self.assertIn("FANTASIA // CLI", out)
            self.assertIn("DO WHAT THOU WILT", out)

    def test_oracle_command(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("sys.argv", ["fantasia", "oracle", "status", "report"]):
                main()
            out = fake_out.getvalue()
            self.assertIn("SPHINXES HAVE SPOKEN", out)


if __name__ == "__main__":
    unittest.main()
