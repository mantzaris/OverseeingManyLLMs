"""Load unmodified, pinned MIT-licensed retail tools without a hosted user simulator."""
import __future__
import importlib.util
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / 'third_party/tau_bench'
PACKAGE = VENDOR / 'tau_bench'
RETAIL = PACKAGE / 'envs/retail'
MUTATIONS = ('cancel_pending_order', 'modify_pending_order_items',
             'return_delivered_order_items', 'exchange_delivered_order_items')
READS = ('find_user_id_by_email', 'find_user_id_by_name_zip', 'get_user_details',
         'get_order_details', 'get_product_details')


def _load_tools():
    # Avoid upstream package initializers importing LiteLLM/external user providers.
    for name, path in [('tau_bench', PACKAGE), ('tau_bench.envs', PACKAGE / 'envs'),
                       ('tau_bench.envs.retail', RETAIL), ('tau_bench.envs.retail.tools', RETAIL / 'tools')]:
        if name not in sys.modules:
            module = types.ModuleType(name); module.__path__ = [str(path)]
            sys.modules[name] = module
    tool_name = 'tau_bench.envs.tool'
    if tool_name not in sys.modules:
        module = types.ModuleType(tool_name)
        # Deferred annotation evaluation supports host Python 3.8 without changing vendor bytes.
        exec(compile((PACKAGE / 'envs/tool.py').read_text(), str(PACKAGE / 'envs/tool.py'),
                     'exec', flags=__future__.annotations.compiler_flag), module.__dict__)
        sys.modules[tool_name] = module
    result = {}
    for name in READS + MUTATIONS:
        qualified = 'tau_bench.envs.retail.tools.' + name
        spec = importlib.util.spec_from_file_location(qualified, RETAIL / 'tools' / (name + '.py'))
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        classes = [v for v in vars(module).values() if isinstance(v, type)
                   and v.__module__ == qualified]
        assert len(classes) == 1
        result[name] = classes[0]
    return result


TOOLS = _load_tools()
POLICY = (RETAIL / 'wiki.md').read_text()


def load_database():
    return {name: json.loads((RETAIL / 'data' / (name + '.json')).read_text())
            for name in ('orders', 'users', 'products')}


def account_database(data, user_id):
    """Independent account state; retain every order and the complete product catalog."""
    import copy
    user = data['users'][user_id]
    return copy.deepcopy(dict(users={user_id: user},
        orders={k: v for k, v in data['orders'].items() if v['user_id'] == user_id},
        products=data['products']))


def invoke(data, action):
    return TOOLS[action['tool']].invoke(data=data, **action['arguments'])


def state_hash(data):
    # Same recursive sorted-dictionary/list-order-sensitive hash as upstream Env.
    from hashlib import sha256
    def to_hashable(value):
        if isinstance(value, dict): return tuple((k, to_hashable(v)) for k, v in sorted(value.items()))
        if isinstance(value, list): return tuple(to_hashable(v) for v in value)
        if isinstance(value, set): return tuple(sorted(to_hashable(v) for v in value))
        return value
    return sha256(str(to_hashable(data)).encode()).hexdigest()
