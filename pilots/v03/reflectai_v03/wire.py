"""Strict transport schemas, with a lossless wire representation for scopes.

Only the declared Scope.match mapping is converted to an array. Decoding walks
the contract schema, so an unrelated object containing a ``match`` key is never
mistaken for a scope. Domain validation remains the contract's responsibility.
"""

from copy import deepcopy
from typing import Any

from grounded_reflection.models import Contract


def _strict(node: dict) -> None:
    node.pop('default', None)
    if 'const' in node:
        node['enum'] = [node.pop('const')]
    if node.get('type') == 'object':
        if node.get('additionalProperties') not in (None, False) or (
            'properties' not in node and node.get('additionalProperties') is not False
        ):
            raise ValueError('Open object mappings require a declared wire representation')
        properties = node.setdefault('properties', {})
        node['required'] = list(properties)
        node['additionalProperties'] = False
    for keyword in ('$defs', 'definitions', 'properties'):
        for child in node.get(keyword, {}).values():
            _strict(child)
    if isinstance(node.get('items'), dict):
        _strict(node['items'])
    for keyword in ('anyOf', 'oneOf', 'allOf', 'prefixItems'):
        for child in node.get(keyword, []):
            _strict(child)


def _scope_wire(scope: dict) -> None:
    scope['properties']['match'] = {
        'type': 'array', 'minItems': 1,
        'items': {
            'type': 'object',
            'properties': {
                'attribute': {'type': 'string', 'minLength': 1, 'pattern': r'\S'},
                'values': {
                    'type': 'array', 'minItems': 1,
                    'items': {'type': 'string', 'minLength': 1, 'pattern': r'\S'},
                },
            },
        },
    }


def strict_response_schema(contract: type[Contract]) -> dict:
    """Close every output object and require all properties, even defaults."""
    schema = deepcopy(contract.model_json_schema())
    for definition in schema.get('$defs', {}).values():
        if definition.get('title') == 'Scope':
            _scope_wire(definition)
    if schema.get('title') == 'Scope':
        _scope_wire(schema)
    _strict(schema)
    return schema


def _decode_scope(scope: Any) -> None:
    if not isinstance(scope, dict) or 'match' not in scope:
        return
    entries = scope['match']
    if not isinstance(entries, list):
        raise ValueError('Wire Scope.match must be an array of attribute/value entries')
    match = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {'attribute', 'values'}:
            raise ValueError('Scope entries must contain exactly attribute and values')
        attribute = entry['attribute']
        if not isinstance(attribute, str) or not attribute.strip():
            raise ValueError('Scope attribute must be a nonempty string')
        if attribute in match:
            raise ValueError(f'Duplicate scope attribute: {attribute}')
        match[attribute] = entry['values']
    scope['match'] = match


def decode_response(contract: type[Contract], response: Any) -> Any:
    """Decode declared scopes and check the strict object shape, without mutation.

This checks required/extra properties before Pydantic can fill defaults. Value
types, rule operations, scope values and domain invariants are then validated by
``contract.model_validate`` in the backend. No field name or value aliases are
inferred, and family/role remain distinct attributes.
"""
    schema = contract.model_json_schema()
    definitions = schema.get('$defs', {})
    decoded = deepcopy(response)

    def visit(value: Any, node: dict) -> None:
        if '$ref' in node:
            reference = node['$ref']
            if not reference.startswith('#/$defs/'):
                raise ValueError(f'Unsupported schema reference: {reference}')
            visit(value, definitions[reference.rsplit('/', 1)[1]])
            return
        if node.get('title') == 'Scope':
            if not isinstance(value, dict) or set(value) != {'match'}:
                raise ValueError('Scope must contain exactly match')
            _decode_scope(value)
            return
        if node.get('type') == 'object' and isinstance(value, dict):
            if node.get('additionalProperties') not in (None, False) or (
                'properties' not in node and node.get('additionalProperties') is not False
            ):
                # Unrelated canonical mappings are not scope containers.
                return
            properties = node.get('properties', {})
            if set(value) != set(properties):
                raise ValueError('Wire object properties differ from strict schema: '
                                 f'missing={sorted(set(properties) - set(value))}, '
                                 f'extra={sorted(set(value) - set(properties))}')
            for key, child in properties.items():
                visit(value[key], child)
        elif node.get('type') == 'array' and isinstance(value, list):
            for item in value:
                visit(item, node.get('items', {}))
        elif 'anyOf' in node or 'oneOf' in node:
            branches = node.get('anyOf', node.get('oneOf', []))
            if value is None and any(branch.get('type') == 'null' for branch in branches):
                return
            nonnull = [branch for branch in branches if branch.get('type') != 'null']
            if len(nonnull) == 1:
                visit(value, nonnull[0])
            elif any('$ref' in branch for branch in nonnull):
                raise ValueError('Ambiguous structured union requires an explicit discriminator')

    visit(decoded, schema)
    return decoded
