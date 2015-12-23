# -*- coding: utf-8 -*-
'''
    :codeauthor: Nitin Madhok <nmadhok@clemson.edu>`

    tests.unit.modules.zfs_test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# Import Python libs
from __future__ import absolute_import

# Import Salt Testing libs
from salttesting import skipIf, TestCase
from salttesting.helpers import ensure_in_syspath

# Import Mock libraries
from salttesting.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON,
)

ensure_in_syspath('../../')

# Import Salt Execution module to test
from salt.modules import zfs

# Globals
zfs.__salt__ = {}


# Skip this test case if we don't have access to mock!
@skipIf(NO_MOCK, NO_MOCK_REASON)
class ZfsTestCase(TestCase):
    '''
    This class contains a set of functions that test salt.modules.zfs module
    '''

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_exists_success(self):
        '''
        Tests successful return of exists function
        '''
        ret = {}
        ret['stdout'] = "NAME        USED  AVAIL  REFER  MOUNTPOINT\nmyzpool/mydataset    30K   157G    30K  /myzpool/mydataset"
        ret['stderr'] = ''
        ret['retcode'] = 0
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertTrue(zfs.exists('myzpool/mydataset'))

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_exists_failure_not_exists(self):
        '''
        Tests unsuccessful return of exists function if dataset does not exist
        '''
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = "cannot open 'myzpool/mydataset': dataset does not exist"
        ret['retcode'] = 1
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertFalse(zfs.exists('myzpool/mydataset'))

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_exists_failure_invalid_name(self):
        '''
        Tests unsuccessful return of exists function if dataset name is invalid
        '''
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = "cannot open 'myzpool/': invalid dataset name"
        ret['retcode'] = 1
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertFalse(zfs.exists('myzpool/'))

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_success(self):
        '''
        Tests successful return of create function on ZFS file system creation
        '''
        res = {'myzpool/mydataset': 'created'}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = ""
        ret['retcode'] = 0
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(zfs.create('myzpool/mydataset'), res)

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_success_with_create_parent(self):
        '''
        Tests successful return of create function when ``create_parent=True``
        '''
        res = {'myzpool/mydataset/mysubdataset': 'created'}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = ""
        ret['retcode'] = 0
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(zfs.create('myzpool/mydataset/mysubdataset', create_parent=True), res)

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_success_with_properties(self):
        '''
        Tests successful return of create function on ZFS file system creation (with properties)
        '''
        res = {'myzpool/mydataset': 'created'}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = ""
        ret['retcode'] = 0
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(
                zfs.create(
                    'myzpool/mydataset',
                    properties={
                        'mountpoint': '/export/zfs',
                        'sharenfs': 'on'
                    }
                ), res
            )

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_error_missing_dataset(self):
        '''
        Tests unsuccessful return of create function if dataset name is missing
        '''
        res = {'myzpool': 'cannot create \'myzpool\': missing dataset name'}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = "cannot create 'myzpool': missing dataset name"
        ret['retcode'] = 1
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(zfs.create('myzpool'), res)

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_error_trailing_slash(self):
        '''
        Tests unsuccessful return of create function if trailing slash in name is present
        '''
        res = {'myzpool/': 'cannot create \'myzpool/\': trailing slash in name'}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = "cannot create 'myzpool/': trailing slash in name"
        ret['retcode'] = 1
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(zfs.create('myzpool/'), res)

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_error_no_such_pool(self):
        '''
        Tests unsuccessful return of create function if the pool is not present
        '''
        res = {'myzpool/mydataset': 'cannot create \'myzpool/mydataset\': no such pool \'myzpool\''}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = "cannot create 'myzpool/mydataset': no such pool 'myzpool'"
        ret['retcode'] = 1
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(zfs.create('myzpool/mydataset'), res)

    @patch('salt.modules.zfs._check_zfs', MagicMock(return_value='/sbin/zfs'))
    def test_create_error_missing_parent(self):
        '''
        Tests unsuccessful return of create function if the parent datasets do not exist
        '''
        res = {'myzpool/mydataset/mysubdataset': 'cannot create \'myzpool/mydataset/mysubdataset\': parent does not exist'}
        ret = {}
        ret['stdout'] = ""
        ret['stderr'] = "cannot create 'myzpool/mydataset/mysubdataset': parent does not exist"
        ret['retcode'] = 1
        mock_cmd = MagicMock(return_value=ret)
        with patch.dict(zfs.__salt__, {'cmd.run_all': mock_cmd}):
            self.assertEqual(zfs.create('myzpool/mydataset/mysubdataset'), res)

if __name__ == '__main__':
    from integration import run_tests
    run_tests(ZfsTestCase, needs_daemon=False)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
