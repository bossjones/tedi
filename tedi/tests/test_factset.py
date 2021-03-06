import os
from ..factset import Factset
from pytest import fixture, raises
from unittest.mock import patch


@fixture
def facts():
    return Factset(sky_color='blue')


def test_can_test_membership(facts):
    assert 'sky_color' in facts


def test_can_set_facts_like_a_dictionary(facts):
    facts['key_canary'] = 'bird'
    assert facts['key_canary'] == 'bird'


def test_can_set_facts_via_contructor_keywords(facts):
    assert facts['sky_color'] == 'blue'


def test_can_delete_facts(facts):
    del(facts['sky_color'])
    assert 'sky_color' not in facts


def test_setting_a_fact_to_none_deletes_it(facts):
    facts['sky_color'] = None
    assert 'sky_color' not in facts


def test_setting_a_new_key_to_none_does_nothing(facts):
    facts['point'] = None
    assert 'point' not in facts


def test_setting_non_string_facts_is_an_error(facts):
    for value in (True, False, 5, object()):
        with raises(ValueError):
            facts['test'] = value


def test_using_non_string_keys_is_an_error(facts):
    for value in (True, False, 5, object()):
        with raises(ValueError):
            facts[value] = 'test'


def test_to_dict_returns_a_dictionary(facts):
    assert isinstance(facts.to_dict(), dict)
    assert 'sky_color' in facts.to_dict()


def test_update_updates_facts_from_a_dict(facts):
    facts.update({'sky_color': 'black'})
    assert facts['sky_color'] == 'black'


def test_update_updates_facts_from_keywords(facts):
    facts.update(sky_color='pink')
    assert facts['sky_color'] == 'pink'


def test_get_returns_none_on_missing_key(facts):
    assert facts.get('complaints') is None


def test_get_returns_default_on_missing_key_when_asked(facts):
    assert facts.get('first_prize', 'consolation_prize') == 'consolation_prize'


def test_copy_returns_an_independant_factset(facts):
    new_facts = facts.copy()
    new_facts['sky_color'] = 'grey'
    assert facts['sky_color'] == 'blue'
    assert new_facts['sky_color'] == 'grey'


def test_it_can_glean_facts_from_special_environment_variables():
    with patch.dict('os.environ', {'TEDI_FACT_bird': 'emu'}):
        assert Factset()['bird'] == 'emu'


def test_it_maps_standard_environment_variable_to_facts():
    for var, value in os.environ.items():
        assert Factset()[f'ENV_{var}'] == value
