"""Strict transport schemas without changing the frozen evidence contracts."""

from copy import deepcopy

from ..models import Contract
from .contracts import Preparation


def _strict(node: dict) -> None:
    node.pop('default', None)
    if node.get('type') == 'object':
        if node.get('additionalProperties') not in (None, False):
            raise ValueError('Open object mappings require an explicit transport representation')
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


def strict_response_schema(contract: type[Contract]) -> dict:
    """Require every property; represent only Scope.match as named entries.

    Nullable fields remain nullable. Domain validation still runs after decoding,
    including nonempty scope values and the existing uniqueness constraints.
    """
    schema = deepcopy(contract.model_json_schema())
    scope = schema.get('$defs', {}).get('Scope')
    if scope is not None:
        scope['properties']['match'] = {
            'type': 'array',
            'minItems': 1,
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
    _strict(schema)
    return schema


def _decode_scope(scope) -> None:
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
        if not isinstance(attribute, str):
            raise ValueError('Scope attribute must be a string')
        if attribute in match:
            raise ValueError(f'Duplicate scope attribute: {attribute}')
        match[attribute] = entry['values']
    scope['match'] = match


def decode_response(contract: type[Contract], response):
    """Convert wire scopes to canonical mappings without mutating raw output."""
    decoded = deepcopy(response)
    if contract is not Preparation or not isinstance(decoded, dict):
        return decoded
    requirements = decoded.get('requirements')
    if not isinstance(requirements, list):
        return decoded
    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        for field in ('rule', 'hypothesis'):
            owner = requirement.get(field)
            if isinstance(owner, dict):
                _decode_scope(owner.get('scope'))
    return decoded
