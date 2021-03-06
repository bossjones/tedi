from pathlib import Path
from pytest import fixture
from ..project import Project
from ..assetset import Assetset
from ..factset import Factset
from unittest.mock import Mock


def get_project(name) -> Project:
    return Project(Path(f'tedi/tests/fixtures/projects/{name}'))


@fixture
def project() -> Project:
    return get_project('simple')


def test_path_is_a_path(project):
    assert isinstance(project.path, Path)


def test_render_calls_render_on_each_image(project):
    for image in project.images:
        image.render = Mock()
    project.render()
    for image in project.images:
        assert image.render.called


def test_build_calls_build_on_each_image(project):
    for image in project.images:
        image.build = Mock()
    project.build()
    for image in project.images:
        assert image.build.called


def test_projects_have_a_dictionary_of_asset_sets(project):
    assert isinstance(project.asset_sets, dict)
    for asset_set in project.asset_sets.values():
        assert isinstance(asset_set, Assetset)


def test_projects_expand_facts_in_assets(project):
    asset = project.asset_sets['fact_based_assets'].assets[0]
    assert asset.filename == 'filename-from-fact.tar.gz'
    assert asset.source == 'file:///source-from-fact'


def test_projects_have_a_factset(project):
    assert isinstance(project.facts, Factset)


def test_projects_can_declare_project_level_facts(project):
    assert project.facts['animal'] == 'cow'
    assert project.facts['cow_color'] is None
