"""
Referencing implementations for JSON Schema specs (historic & current).
"""

from __future__ import annotations

from collections.abc import Sequence, Set
from typing import Any, Iterable, Union

from referencing import Anchor, Registry, Resource, Specification
from referencing._attrs import frozen
from referencing._core import Resolved as _Resolved, Resolver as _Resolver
from referencing.typing import URI, Anchor as AnchorType, Mapping

#: A JSON Schema which is a JSON object
ObjectSchema = Mapping[str, Any]

#: A JSON Schema of any kind
Schema = Union[bool, ObjectSchema]


@frozen
class UnknownDialect(Exception):
    """
    A dialect identifier was found for a dialect unknown by this library.

    If it's a custom ("unofficial") dialect, be sure you've registered it.
    """

    uri: URI


def _dollar_id(contents: Schema) -> URI | None:
    if isinstance(contents, bool):
        return
    return contents.get("$id")


def _legacy_dollar_id(contents: Schema) -> URI | None:
    if isinstance(contents, bool) or "$ref" in contents:
        return
    id = contents.get("$id")
    if id is not None and not id.startswith("#"):
        return id


def _legacy_id(contents: ObjectSchema) -> URI | None:
    if "$ref" in contents:
        return
    id = contents.get("id")
    if id is not None and not id.startswith("#"):
        return id


def _anchor(
    specification: Specification[Schema],
    contents: Schema,
) -> Iterable[AnchorType[Schema]]:
    if isinstance(contents, bool):
        return
    anchor = contents.get("$anchor")
    if anchor is not None:
        yield Anchor(
            name=anchor,
            resource=specification.create_resource(contents),
        )

    dynamic_anchor = contents.get("$dynamicAnchor")
    if dynamic_anchor is not None:
        yield DynamicAnchor(
            name=dynamic_anchor,
            resource=specification.create_resource(contents),
        )


def _anchor_2019(
    specification: Specification[Schema],
    contents: Schema,
) -> Iterable[Anchor[Schema]]:
    if isinstance(contents, bool):
        return []
    anchor = contents.get("$anchor")
    if anchor is None:
        return []
    return [
        Anchor(
            name=anchor,
            resource=specification.create_resource(contents),
        ),
    ]


def _legacy_anchor_in_dollar_id(
    specification: Specification[Schema],
    contents: Schema,
) -> Iterable[Anchor[Schema]]:
    if isinstance(contents, bool):
        return []
    id = contents.get("$id", "")
    if not id.startswith("#"):
        return []
    return [
        Anchor(
            name=id[1:],
            resource=specification.create_resource(contents),
        ),
    ]


def _legacy_anchor_in_id(
    specification: Specification[ObjectSchema],
    contents: ObjectSchema,
) -> Iterable[Anchor[ObjectSchema]]:
    id = contents.get("id", "")
    if not id.startswith("#"):
        return []
    return [
        Anchor(
            name=id[1:],
            resource=specification.create_resource(contents),
        ),
    ]


def _subresources_of(
    in_value: Set[str] = frozenset(),
    in_subvalues: Set[str] = frozenset(),
    in_subarray: Set[str] = frozenset(),
):
    """
    Create a callable returning JSON Schema specification-style subschemas.

    Relies on specifying the set of keywords containing subschemas in their
    values, in a subobject's values, or in a subarray.
    """

    def subresources_of(contents: Schema) -> Iterable[ObjectSchema]:
        if isinstance(contents, bool):
            return
        for each in in_value:
            if each in contents:
                yield contents[each]
        for each in in_subarray:
            if each in contents:
                yield from contents[each]
        for each in in_subvalues:
            if each in contents:
                yield from contents[each].values()

    return subresources_of


def _subresources_of_with_crazy_items(
    in_value: Set[str] = frozenset(),
    in_subvalues: Set[str] = frozenset(),
    in_subarray: Set[str] = frozenset(),
):
    """
    Specifically handle older drafts where there are some funky keywords.
    """

    def subresources_of(contents: Schema) -> Iterable[ObjectSchema]:
        if isinstance(contents, bool):
            return
        for each in in_value:
            if each in contents:
                yield contents[each]
        for each in in_subarray:
            if each in contents:
                yield from contents[each]
        for each in in_subvalues:
            if each in contents:
                yield from contents[each].values()

        items = contents.get("items")
        if items is not None:
            if isinstance(items, Sequence):
                yield from items
            else:
                yield items

    return subresources_of


def _subresources_of_with_crazy_items_dependencies(
    in_value: Set[str] = frozenset(),
    in_subvalues: Set[str] = frozenset(),
    in_subarray: Set[str] = frozenset(),
):
    """
    Specifically handle older drafts where there are some funky keywords.
    """

    def subresources_of(contents: Schema) -> Iterable[ObjectSchema]:
        if isinstance(contents, bool):
            return
        for each in in_value:
            if each in contents:
                yield contents[each]
        for each in in_subarray:
            if each in contents:
                yield from contents[each]
        for each in in_subvalues:
            if each in contents:
                yield from contents[each].values()

        items = contents.get("items")
        if items is not None:
            if isinstance(items, Sequence):
                yield from items
            else:
                yield items
        dependencies = contents.get("dependencies")
        if dependencies is not None:
            values = iter(dependencies.values())
            value = next(values, None)
            if isinstance(value, Mapping):
                yield value
                yield from values

    return subresources_of


DRAFT202012 = Specification(
    name="draft2020-12",
    id_of=_dollar_id,
    subresources_of=_subresources_of(
        in_value={
            "additionalProperties",
            "contains",
            "contentSchema",
            "else",
            "if",
            "items",
            "not",
            "propertyNames",
            "then",
            "unevaluatedItems",
            "unevaluatedProperties",
        },
        in_subarray={"allOf", "anyOf", "oneOf", "prefixItems"},
        in_subvalues={
            "$defs",
            "dependentSchemas",
            "patternProperties",
            "properties",
        },
    ),
    anchors_in=_anchor,
)
DRAFT201909 = Specification(
    name="draft2019-09",
    id_of=_dollar_id,
    subresources_of=_subresources_of_with_crazy_items(
        in_value={
            "additionalItems",
            "additionalProperties",
            "contains",
            "contentSchema",
            "else",
            "if",
            "not",
            "propertyNames",
            "then",
            "unevaluatedItems",
            "unevaluatedProperties",
        },
        in_subarray={"allOf", "anyOf", "oneOf"},
        in_subvalues={
            "$defs",
            "dependentSchemas",
            "patternProperties",
            "properties",
        },
    ),
    anchors_in=_anchor_2019,
)
DRAFT7 = Specification(
    name="draft-07",
    id_of=_legacy_dollar_id,
    subresources_of=_subresources_of_with_crazy_items_dependencies(
        in_value={
            "additionalItems",
            "additionalProperties",
            "contains",
            "else",
            "if",
            "not",
            "propertyNames",
            "then",
        },
        in_subarray={"allOf", "anyOf", "oneOf"},
        in_subvalues={"definitions", "patternProperties", "properties"},
    ),
    anchors_in=_legacy_anchor_in_dollar_id,
)
DRAFT6 = Specification(
    name="draft-06",
    id_of=_legacy_dollar_id,
    subresources_of=_subresources_of_with_crazy_items_dependencies(
        in_value={
            "additionalItems",
            "additionalProperties",
            "contains",
            "not",
            "propertyNames",
        },
        in_subarray={"allOf", "anyOf", "oneOf"},
        in_subvalues={"definitions", "patternProperties", "properties"},
    ),
    anchors_in=_legacy_anchor_in_dollar_id,
)
DRAFT4 = Specification(
    name="draft-04",
    id_of=_legacy_id,
    subresources_of=_subresources_of_with_crazy_items_dependencies(
        in_value={"additionalItems", "additionalProperties", "not"},
        in_subarray={"allOf", "anyOf", "oneOf"},
        in_subvalues={"definitions", "patternProperties", "properties"},
    ),
    anchors_in=_legacy_anchor_in_id,
)
DRAFT3 = Specification(
    name="draft-03",
    id_of=_legacy_id,
    subresources_of=_subresources_of_with_crazy_items_dependencies(
        in_value={"additionalItems", "additionalProperties"},
        in_subarray={"extends"},
        in_subvalues={"definitions", "patternProperties", "properties"},
    ),
    anchors_in=_legacy_anchor_in_id,
)


_SPECIFICATIONS: Registry[Specification[Schema]] = Registry(
    {  # type: ignore[reportGeneralTypeIssues]  # :/ internal vs external types
        dialect_id: Resource.opaque(specification)
        for dialect_id, specification in [
            ("https://json-schema.org/draft/2020-12/schema", DRAFT202012),
            ("https://json-schema.org/draft/2019-09/schema", DRAFT201909),
            ("http://json-schema.org/draft-07/schema#", DRAFT7),
            ("http://json-schema.org/draft-06/schema#", DRAFT6),
            ("http://json-schema.org/draft-04/schema#", DRAFT4),
            ("http://json-schema.org/draft-03/schema#", DRAFT3),
        ]
    },
)


def specification_with(
    dialect_id: URI,
    default: Specification[Any] = None,  # type: ignore[reportGeneralTypeIssues]  # noqa: E501
) -> Specification[Any]:
    """
    Retrieve the `Specification` with the given dialect identifier.

    Raises:

        `UnknownDialect`

            if the given ``dialect_id`` isn't known
    """
    resource = _SPECIFICATIONS.get(dialect_id)
    if resource is not None:
        return resource.contents
    if default is None:  # type: ignore[reportUnnecessaryComparison]
        raise UnknownDialect(dialect_id)
    return default


@frozen
class DynamicAnchor:
    """
    Dynamic anchors, introduced in draft 2020.
    """

    name: str
    resource: Resource[Schema]

    def resolve(self, resolver: _Resolver[Schema]):
        """
        Resolve this anchor dynamically.
        """
        last = self.resource
        for uri, registry in resolver.dynamic_scope():
            try:
                anchor = registry.anchor(uri, self.name)
            except LookupError:
                continue
            if isinstance(anchor, DynamicAnchor):
                last = anchor.resource
        return _Resolved(
            contents=last.contents,
            resolver=resolver.in_subresource(last),
        )


def lookup_recursive_ref(resolver: _Resolver[Schema]) -> _Resolved[Schema]:
    """
    Recursive references (via recursive anchors), present only in draft 2019.

    As per the 2019 specification (§ 8.2.4.2.1), only the ``#`` recursive
    reference is supported (and is therefore assumed to be the relevant
    reference).
    """
    resolved = resolver.lookup("#")
    if isinstance(resolved.contents, Mapping) and resolved.contents.get(
        "$recursiveAnchor",
    ):
        for uri, _ in resolver.dynamic_scope():
            next_resolved = resolver.lookup(uri)
            if not isinstance(
                next_resolved.contents,
                Mapping,
            ) or not next_resolved.contents.get("$recursiveAnchor"):
                break
            resolved = next_resolved
    return resolved
