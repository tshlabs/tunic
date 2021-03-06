Change Log
==========

1.3.0 - 2017-08-31
------------------
* Add retry settings to :class:`tunic.install.HttpArtifactInstallation` to allow more
  robust deploys over unreliable networks. Fixes `#8 <https://github.com/tshlabs/tunic/issues/8>`_.

1.2.3 - 2017-06-20
------------------
* **Bug** - Fix bug where local permissions were not mirrored on the remote side when
  using `LocalArtifactInstallation`.

1.2.2 - 2016-05-06
------------------
* **Bug** - Fix bug where newer version of ``cryptography`` module being pulled in than
  supported by the version of Fabric we depended on. Fixed by updating to Fabric 1.11.1.
  Fixes `#5 <https://github.com/tshlabs/tunic/issues/5>`_.

1.2.1 - 2016-02-25
------------------
* **Bug** - Fix bug when running with older versions of Fabric that didn't define
  a ``warn_only`` context manager. Fixes `#4 <https://github.com/tshlabs/tunic/issues/4>`_.

1.2.0 - 2016-02-25
------------------
* Add :class:`tunic.install.HttpArtifactInstallation` for installation of a single
  artifact downloaded from an HTTP or HTTPS URL. Useful when installation artifacts
  are stored in some central file store or repository (like Artifactory).
* Minor documentation fixes.

1.1.0 - 2015-06-03
------------------
* **Bug** - Fix bug in :func:`tunic.core.get_current_path` and
  :func:`tunic.core.get_releases_path` where input was not being checked to ensure
  it was a valid base directory. :class:`ValueError` will now be raised for invalid
  (blank or ``None``) values.
* Added fuzz testing to some parts of the Tunic unit test suite.
* Added :class:`tunic.install.LocalArtifactInstallation` for installation of single
  local artifact onto a remote server. Useful for Go binaries or Java JARs and WARs.

1.0.1 - 2015-04-04
------------------
* This is the first stable release of Tunic. From this point on, all breaking
  changes will only be made in major version releases.

  This release is almost functionally equivalent to the ``0.5.0`` release. There
  are only minor changes to the build process and project documentation.
* Packaging fixes (use ``twine`` for uploads to PyPI, stop using the setup.py
  ``register`` command).
* Assorted documentation updates.

0.5.0 - 2014-10-11
------------------
* **Breaking change** - Change behavior of :class:`tunic.install.LocalArtifactTransfer`
  to yield the final destination path on the remote server (a combination of the
  remote path and right-most component of the local path). This new value will
  be the only path removed on the remote server when the context manager exits.
* **Breaking change** - Trailing slashes on ``local_path`` and ``remote_path``
  constructor arguments to :class:`tunic.install.LocalArtifactTransfer` are now removed
  before being used.
* Add :class:`tunic.install.StaticFileInstallation` class for installation of static
  files into a release on a remote server.

0.4.0 - 2014-10-02
------------------
* Allow override of the ``virtualenv`` script location on the remote
  server when using the :class:`tunic.install.VirtualEnvInstallation` class.
* Add :doc:`usage` section to the documentation that explains how to use
  each part of the library at a higher level than just the :doc:`api` section.
* Add :class:`tunic.install.LocalArtifactTransfer` class for transferring locally
  built artifacts to a remote server and cleaning them up after deployment
  has completed.

0.3.0 - 2014-09-28
------------------
* Test coverage improvements
* :class:`tunic.core.ReleaseManager` and :class:`tunic.core.ProjectSetup`
  now throw :class:`ValueError` for invalid ``base`` values in their
  ``__init__`` methods.
* Fix bug where we attempted to split command output by ``\n\r`` instead
  of ``\r\n``.
* Add :class:`tunic.install.VirtualEnvInstallation` class for performing remote
  virtualenv installations.

0.2.0 - 2014-09-26
------------------
* Add initial documentation for Tunic API
* Add design decision documentation for library
* Change behavior of :meth:`tunic.core.ProjectSetup.set_permissions` to not
  attempt to change the ownership of the code deploy unless it is using the
  ``sudo`` function

0.1.0 - 2014-09-22
------------------
* Initial release
