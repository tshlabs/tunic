# -*- coding: utf-8 -*-

from fabric.api import (
    lcd,
    local,
    task,
    warn_only)


@task
def clean():
    local('rm -rf wheelhouse')
    local('rm -rf dist')
    local('rm -rf build')

    with lcd('doc'):
        local('make clean')


@task
def docs():
    with lcd('doc'):
        local('make html')

@task
def lint():
    with warn_only():
        local('pylint --rcfile .pylintrc tunic')


@task
def push():
    local('git push origin')
    local('git push github')


@task
def push_tags():
    local('git push --tags origin')
    local('git push --tags github')


@task
def pypi():
    local('python setup.py sdist bdist_wheel')
    local('twine upload dist/*')
