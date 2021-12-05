import unittest
from output import pyaz
from tooling import load_command_table

class Constants:
    TEST_GROUP_NAME = "pyaz-test-group"

class TestIntegration(unittest.TestCase):

    def test_az_version_positive(self):
        """happy path test for pyaz.version"""
        result = pyaz.version()
        self.assertIsInstance(result, dict)
        
        # test that the result has a key named azure-cli
        version = result["azure-cli"]
        self.assertIsNotNone(version)


    def test_az_version_negative(self):
        """test that calling pyaz.version with an argument raises an error"""
        with self.assertRaises(TypeError):
            result = pyaz.version("test")
    
    
    def test_az_account_list_positive(self):
        """happy path test for az account list"""
        result = pyaz.account.list()
        self.assertIsInstance(result, list)
        
        # test that the first item in the result has a key named homeTenantId
        tenant_id = result[0]["homeTenantId"]
        self.assertIsNotNone(tenant_id)
        
    def test_az_group_create_positive(self):
        """happy path test for az group create"""
        try:
            result = pyaz.group.create(location="eastus", name=Constants.TEST_GROUP_NAME)
            self.assertEqual(Constants.TEST_GROUP_NAME, result['name'])
        finally:
            pyaz.group.delete(name=Constants.TEST_GROUP_NAME, yes=True, no_wait=True)

    def test_az_group_delete_positive(self):
        """happy path test for az group delete"""
        # first create test group
        result = pyaz.group.create(location="eastus", name=Constants.TEST_GROUP_NAME)
        self.assertEqual(Constants.TEST_GROUP_NAME, result['name'],'Unable to create test resource group')
        id = result['id']

        # now try to delete it
        pyaz.group.delete(name=Constants.TEST_GROUP_NAME, yes=True)

        # assert that the group no longer exists by attempted to show it
        with self.assertRaises(Exception):
            result = pyaz.group.show(name=Constants.TEST_GROUP_NAME)
            
