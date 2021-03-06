import os
import random
import unittest
from .testcases_base import TestcasesBase


class TestSALLSSHD(TestcasesBase):

    def setUp(self):
        super().setUp()
        self.sshd = self.j.sal.sshd
        keyfile = self.sshd.SSH_AUTHORIZED_KEYS
        if keyfile.exists():
            self.authorized_keys = keyfile.text().splitlines()
        else:
            self.authorized_keys = []

    def tearDown(self):
        self.sshd.SSH_AUTHORIZED_KEYS.write_lines(self.authorized_keys)
        super().tearDown()

    def read_authorized_keys_file(self):
        path = str(self.sshd.SSH_AUTHORIZED_KEYS)
        try:
            with open(path, 'r') as f:
                lines = [x.strip() for x in f.readlines()]
        except FileNotFoundError:
            lines = []
        return lines

    def test01_keys(self):
        """ JS-057

        **Test Scenario:**
        #. Get authorized keys.
        """
        self.lg.info('Get authorized keys')
        self.assertListEqual(self.sshd.keys, self.read_authorized_keys_file())

    def test02_add_key(self):
        """ JS-058

        **Test Scenario:**
        #. Add new key [K1].
        #. Check that key [K1] is added.
        """
        self.lg.info('Add new key [K1]')
        key = self.random_string()
        self.sshd.addKey(key)
        self.sshd.commit()

        self.lg.info('Check that key [K1] is added')
        self.assertIn(key, self.sshd.keys)
        self.assertIn(key, self.read_authorized_keys_file())

    def test03_delete_key(self):
        """ JS-059

        **Test Scenario:**
        #. Add new key [K1], should succeed.
        #. Delete key [K1], should succeed.
        #. Check that key [K1] is deleted, should succeed.
        """
        self.lg.info('Add new key [K1], should succeed')
        key = self.random_string()
        self.sshd.addKey(key)
        self.sshd.commit()

        self.lg.info('Delete key [K1], should succeed')
        self.sshd.deleteKey(key)
        self.sshd.commit()

        self.lg.info('Check that key [K1] is deleted, should succeed')
        self.assertNotIn(key, self.sshd.keys)
        self.assertNotIn(key, self.read_authorized_keys_file())

    def test04_erase(self):
        """ JS-060

        **Test Scenario:**
        #. Erase all authorized keys.
        #. Check that authorized keys file is empty.
        """
        self.lg.info('Erase all authorized keys')
        self.sshd.erase()
        self.sshd.commit()

        self.lg.info('Check that authorized keys file is empty')
        self.assertEqual(self.sshd.keys, [])
        self.assertEqual(self.read_authorized_keys_file(), [])
