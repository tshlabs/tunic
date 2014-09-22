# -*- coding: utf-8 -*-
import re

import mock
import tshfab.core


class StrDecorator(str):
    """Simple subclass to allow us to set attributes on
    instances of this class (which you can't do with a
    normal string instance). We do this to emulate the
    way Fabric does return values.
    """


class TestReleaseManager(object):
    def setup(self):
        self.runner = mock.Mock(spec=tshfab.core.FabRunner)

    def test_get_current_release(self):
        self.runner.run.return_value = StrDecorator('/srv/test/releases/20140921215951\n')
        self.runner.run.return_value.failed = False

        rm = tshfab.core.ReleaseManager('/srv/test', runner=self.runner)

        assert '20140921215951' == rm.get_current_release()
        self.runner.run.assert_called_once_with('readlink /srv/test/current')

    def test_get_releases(self):
        self.runner.run.return_value = StrDecorator(
            '20140921220657\n20140921220642\n20140921215951\n')
        self.runner.run.return_value.failed = False

        rm = tshfab.core.ReleaseManager('/srv/test', runner=self.runner)
        assert ['20140921220657', '20140921220642', '20140921215951'] == \
               rm.get_releases()
        self.runner.run.assert_called_once_with('ls -1r /srv/test/releases')

    def test_get_previous_release(self):
        def return_values(*args, **kwargs):
            if args[0].startswith('readlink'):
                res = StrDecorator('/srv/test/releases/20140921220657\n')
                res.failed = False
                return res
            if args[0].startswith('ls'):
                res = StrDecorator(
                    '20140921220657\n20140921220642\n20140921215951\n')
                res.failed = False
                return res
            return None

        self.runner.run.side_effect = return_values
        rm = tshfab.core.ReleaseManager('/srv/test', runner=self.runner)

        assert '20140921220642' == rm.get_previous_release()

    def test_set_current_release(self):
        rm = tshfab.core.ReleaseManager('/srv/test', runner=self.runner)
        rm._set_current_release('20140921220642', rand='1234')

        self.runner.run.assert_any_call(
            'ln -s /srv/test/releases/20140921220642 /srv/test/1234')
        self.runner.run.assert_any_call(
            'mv -T /srv/test/1234 /srv/test/current')

    def test_cleanup(self):
        pass


class TestProjectSetup(object):
    def setup(self):
        self.runner = mock.Mock(spec=tshfab.core.FabRunner)

    def test_setup_directories_with_sudo(self):
        setup = tshfab.core.ProjectSetup('/srv/test', runner=self.runner)
        setup.setup_directories(use_sudo=True)

        self.runner.sudo.assert_called_once_with('mkdir -p /srv/test/releases')

    def test_setup_directories_no_sudo(self):
        setup = tshfab.core.ProjectSetup('/srv/test', runner=self.runner)
        setup.setup_directories(use_sudo=False)

        self.runner.run.assert_called_once_with('mkdir -p /srv/test/releases')

    def test_set_permissions_with_sudo(self):
        setup = tshfab.core.ProjectSetup('/srv/test', runner=self.runner)
        setup.set_permissions('user:group', use_sudo=True)

        self.runner.sudo.assert_any_call('chown -R user:group /srv/test')
        self.runner.sudo.assert_any_call('chmod u+rwx,g+rws,o+rx /srv/test')
        self.runner.sudo.assert_any_call('chmod u+rwx,g+rws,o+rx /srv/test/releases')
        self.runner.sudo.assert_any_call('chmod -R u+rw,g+rw,o+r /srv/test')

    def test_set_permissions_no_sudo(self):
        setup = tshfab.core.ProjectSetup('/srv/test', runner=self.runner)
        setup.set_permissions('user:group', use_sudo=False)

        self.runner.run.assert_any_call('chown -R user:group /srv/test')
        self.runner.run.assert_any_call('chmod u+rwx,g+rws,o+rx /srv/test')
        self.runner.run.assert_any_call('chmod u+rwx,g+rws,o+rx /srv/test/releases')
        self.runner.run.assert_any_call('chmod -R u+rw,g+rw,o+r /srv/test')


def test_split_by_line_no_newline():
    assert ['foobar'] == tshfab.core.split_by_line('foobar')
    assert ['foobar'] == tshfab.core.split_by_line(' foobar ')


def test_split_by_line_windows():
    assert ['foo', 'bar'] == tshfab.core.split_by_line('foo\n\rbar')
    assert ['foo', 'bar'] == tshfab.core.split_by_line(' foo\n\rbar ')
    assert ['foo', 'bar'] == tshfab.core.split_by_line(' foo \n\r bar ')


def test_split_by_line_unix():
    assert ['foo', 'bar'] == tshfab.core.split_by_line('foo\nbar')
    assert ['foo', 'bar'] == tshfab.core.split_by_line(' foo\nbar ')
    assert ['foo', 'bar'] == tshfab.core.split_by_line('foo \n bar')


def test_get_current_path():
    assert '/var/www/test/current' == tshfab.core.get_current_path('/var/www/test')


def test_get_releases_path():
    assert '/var/www/test/releases' == tshfab.core.get_releases_path('/var/www/test')


def test_get_release_id():
    assert re.match(
        '[\d]+\-local', tshfab.core.get_release_id('local')) is not None
