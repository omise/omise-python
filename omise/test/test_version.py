import unittest
from unittest import mock

class VersionTest(unittest.TestCase):
    @mock.patch("importlib.metadata.version", side_effect=__import__("importlib").metadata.PackageNotFoundError)
    def test_version_package_not_found(self, mock_version):
        """Ensure that PackageNotFoundError sets version to 'unknown'."""
        from importlib import reload
        import omise.version as omise_version

        # Reload module so the import runs again and triggers our mock
        reload(omise_version)
        self.assertEqual(omise_version.__VERSION__, "unknown")
