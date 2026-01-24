#!/usr/bin/env python3
"""
Test script for LLM parameter mapping.
Tests all model/parameter combinations with minimal API calls.
"""

import sys, json
sys.path.insert(0, r'E:\Dev\IPPS\DevSystemV3.2\skills\llm-evaluation')

from pathlib import Path

# Import the functions we need to test
script_dir = Path(r'E:\Dev\IPPS\DevSystemV3.2\skills\llm-evaluation')
sys.path.insert(0, str(script_dir))

# Load configs directly
def load_configs():
    mapping_file = script_dir / 'model-parameter-mapping.json'
    registry_file = script_dir / 'model-registry.json'
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    with open(registry_file, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    return mapping, registry


def get_model_config(model: str, registry: dict) -> dict:
    for entry in registry['model_id_startswith']:
        if model.startswith(entry['prefix']):
            return entry
    return None


def build_api_params(model: str, mapping: dict, registry: dict,
                     temperature: str, reasoning_effort: str,
                     output_length: str, seed: int = None) -> dict:
    model_config = get_model_config(model, registry)
    if not model_config:
        return None, None, None
    
    effort_map = mapping['effort_mapping']
    params = {}
    
    method = model_config.get('method', 'temperature')
    provider = model_config.get('provider', 'openai')
    
    if method == 'temperature':
        factor = effort_map[temperature]['temperature_factor']
        params['temperature'] = factor * model_config.get('temp_max', 2.0)
    elif method == 'reasoning_effort':
        params['reasoning_effort'] = effort_map[reasoning_effort]['openai_reasoning_effort']
    elif method == 'effort':
        params['effort'] = effort_map[reasoning_effort]['openai_reasoning_effort']
    elif method == 'thinking':
        factor = effort_map[reasoning_effort]['anthropic_thinking_factor']
        budget = int(factor * model_config.get('thinking_max', 100000))
        if budget > 0:
            params['thinking'] = {'type': 'enabled', 'budget_tokens': budget}
    
    output_factor = effort_map[output_length]['output_length_factor']
    max_output = model_config.get('max_output', 16384)
    params['max_tokens'] = int(output_factor * max_output)
    
    if seed is not None:
        if model_config.get('seed', False):
            params['seed'] = seed
    
    return params, method, provider


def test_param_mapping():
    """Test parameter mapping for all models and effort levels."""
    mapping, registry = load_configs()
    
    test_models = [
        'gpt-4o',           # OpenAI temperature model
        'gpt-5-mini',       # OpenAI reasoning model
        'claude-3.5-sonnet', # Anthropic temperature model
        'claude-sonnet-4',  # Anthropic thinking model
    ]
    
    effort_levels = ['none', 'minimal', 'low', 'medium', 'high', 'xhigh']
    
    print("=" * 80)
    print("PARAMETER MAPPING TESTS")
    print("=" * 80)
    
    all_passed = True
    
    for model in test_models:
        print(f"\n--- {model} ---")
        model_config = get_model_config(model, registry)
        if not model_config:
            print(f"  [FAIL] Model not found in registry")
            all_passed = False
            continue
        
        print(f"  Provider: {model_config.get('provider')}")
        print(f"  Method: {model_config.get('method')}")
        print(f"  Max output: {model_config.get('max_output')}")
        
        for effort in effort_levels:
            params, method, provider = build_api_params(
                model, mapping, registry, effort, effort, effort
            )
            
            if params is None:
                print(f"  [FAIL] {effort}: Could not build params")
                all_passed = False
                continue
            
            # Validate params
            if method == 'temperature':
                if 'temperature' not in params:
                    print(f"  [FAIL] {effort}: Missing temperature")
                    all_passed = False
                elif params['temperature'] < 0:
                    print(f"  [FAIL] {effort}: Negative temperature")
                    all_passed = False
                else:
                    print(f"  [PASS] {effort}: temp={params['temperature']:.2f}, max_tokens={params['max_tokens']}")
            elif method == 'reasoning_effort':
                if 'reasoning_effort' not in params:
                    print(f"  [FAIL] {effort}: Missing reasoning_effort")
                    all_passed = False
                else:
                    print(f"  [PASS] {effort}: reasoning_effort={params['reasoning_effort']}, max_tokens={params['max_tokens']}")
            elif method == 'thinking':
                thinking = params.get('thinking', {})
                budget = thinking.get('budget_tokens', 0)
                print(f"  [PASS] {effort}: thinking_budget={budget}, max_tokens={params['max_tokens']}")
            else:
                print(f"  [INFO] {effort}: method={method}, params={params}")
    
    print("\n" + "=" * 80)
    if all_passed:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
    print("=" * 80)
    
    return all_passed


def test_seed_handling():
    """Test seed parameter handling."""
    mapping, registry = load_configs()
    
    print("\n" + "=" * 80)
    print("SEED HANDLING TESTS")
    print("=" * 80)
    
    # Test seed on OpenAI model that supports it
    params, _, _ = build_api_params('gpt-4o', mapping, registry, 'medium', 'medium', 'medium', seed=42)
    if params.get('seed') == 42:
        print("[PASS] gpt-4o: Seed 42 passed through")
    else:
        print(f"[FAIL] gpt-4o: Expected seed=42, got {params.get('seed')}")
        return False
    
    # Test seed on model that doesn't support it (reasoning model)
    params, _, _ = build_api_params('gpt-5-mini', mapping, registry, 'medium', 'medium', 'medium', seed=42)
    if 'seed' not in params:
        print("[PASS] gpt-5-mini: Seed correctly ignored")
    else:
        print(f"[FAIL] gpt-5-mini: Seed should be ignored, got {params.get('seed')}")
        return False
    
    # Test seed on Anthropic model
    params, _, _ = build_api_params('claude-sonnet-4', mapping, registry, 'medium', 'medium', 'medium', seed=42)
    if 'seed' not in params:
        print("[PASS] claude-sonnet-4: Seed correctly ignored (Anthropic)")
    else:
        print(f"[FAIL] claude-sonnet-4: Seed should be ignored, got {params.get('seed')}")
        return False
    
    print("[PASS] All seed tests passed")
    return True


def test_output_length_calculation():
    """Test output length factor calculations."""
    mapping, registry = load_configs()
    
    print("\n" + "=" * 80)
    print("OUTPUT LENGTH TESTS")
    print("=" * 80)
    
    # gpt-4o has max_output=16384
    params, _, _ = build_api_params('gpt-4o', mapping, registry, 'medium', 'medium', 'none')
    expected = int(0.25 * 16384)  # none = 0.25 factor
    if params['max_tokens'] == expected:
        print(f"[PASS] gpt-4o none: max_tokens={params['max_tokens']} (expected {expected})")
    else:
        print(f"[FAIL] gpt-4o none: max_tokens={params['max_tokens']} (expected {expected})")
        return False
    
    params, _, _ = build_api_params('gpt-4o', mapping, registry, 'medium', 'medium', 'high')
    expected = int(1.0 * 16384)  # high = 1.0 factor
    if params['max_tokens'] == expected:
        print(f"[PASS] gpt-4o high: max_tokens={params['max_tokens']} (expected {expected})")
    else:
        print(f"[FAIL] gpt-4o high: max_tokens={params['max_tokens']} (expected {expected})")
        return False
    
    print("[PASS] All output length tests passed")
    return True


if __name__ == '__main__':
    passed = True
    passed = test_param_mapping() and passed
    passed = test_seed_handling() and passed
    passed = test_output_length_calculation() and passed
    
    print("\n" + "=" * 80)
    if passed:
        print("ALL UNIT TESTS PASSED")
        sys.exit(0)
    else:
        print("SOME UNIT TESTS FAILED")
        sys.exit(1)
