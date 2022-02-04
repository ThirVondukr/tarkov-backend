import pytest

from modules.items.repository import TemplateRepository


@pytest.fixture
def template_repository():
    return TemplateRepository()


def test_is_singleton():
    TemplateRepository._instance = None
    assert TemplateRepository() is TemplateRepository()


def test_has_all_templates(templates_as_dict, template_repository):
    for key, item in templates_as_dict.items():
        assert item == template_repository.templates[key].dict(
            by_alias=True, exclude_unset=True
        )
