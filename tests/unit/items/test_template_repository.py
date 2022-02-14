import random

import pytest

from modules.items.repository import TemplateRepository


def test_has_all_templates(templates_as_dict, template_repository: TemplateRepository):
    for key, item in templates_as_dict.items():
        assert item == template_repository.templates[key].dict(
            by_alias=True, exclude_unset=True
        )


def test_get_template_by_id(
    template_repository: TemplateRepository,
    templates_as_dict: dict,
):
    template_id = "59fafb5d86f774067a6f2084"
    template = template_repository.get(template_id)
    template_dict = next(
        t for t in templates_as_dict.values() if t["_id"] == template_id
    )
    assert template.dict(by_alias=True, exclude_unset=True) == template_dict


def test_get_template_by_id_random(
    template_repository: TemplateRepository,
    templates_as_dict: dict,
):
    random.seed(42)
    templates = random.choices(list(templates_as_dict.values()), k=100)

    for template_dict in templates:
        template = template_repository.get(template_dict["_id"])
        assert template.dict(by_alias=True, exclude_unset=True) == template_dict


def test_find_by_name_if_not_exists(
    template_repository: TemplateRepository,
    templates_as_dict: dict,
):
    with pytest.raises(ValueError):
        template_repository.find(name="This name does not exist")


def test_find_by_name(
    template_repository: TemplateRepository,
    templates_as_dict: dict,
):
    for template_dict in templates_as_dict.values():
        try:
            template = template_repository.find(template_dict["_name"])
            assert template.dict(by_alias=True, exclude_unset=True) == template_dict
        except ValueError:
            pass
