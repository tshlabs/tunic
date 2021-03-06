.. Tunic documentation master file, created by
   sphinx-quickstart on Mon Sep 22 21:26:34 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. NOTE: Copied from README.rst, keep in sync.
   Copied because github won't execute include directives so
   having the README.rst just include some common text file
   isn't an option.

Tunic
=====

A Python library for deploying code on remote servers.

Tunic is designed so that you can make use of as much or as little of
its functionality as you'd like, the choice is yours.

It only requires the Fabric library as a dependency and can be installed
from the Python Package Index (PyPI) using the pip tool like so. ::

    pip install tunic

You could then make use of it in your deploy process like so. ::

    from fabric.api import task
    from tunic.api import get_release_id, ReleaseManager, VirtualEnvInstallation

    APP_BASE = '/srv/www/myapp'

    @task
    def deploy():
        stop_my_app()
        release = get_release_id()

        installer = VirtualEnvInstaller(APP_BASE, ['myapp'])
        release_manager = ReleaseManager(APP_BASE)

        installer.install(release)
        release_manager.set_current_release(release)

        start_my_app()

The above snippet is just the start, take a look around the code base
for more methods that can save you work in your deploy process.

Contents
========

.. toctree::
    :maxdepth: 2

    design
    usage
    api
    changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

