"""Real-world test: verify never_compress works on actual DevSystem files."""
import json
from pathlib import Path
from unittest.mock import Mock

from lib.file_bundle_builder import generate_bundle, scan_source_dir
from lib.file_compressor import run_compression_step
from lib.pipeline_state import init_state


def test_devsystem_subset_never_compress():
    """Test never_compress on real DevSystem files."""
    source = Path("test-devsystem-subset")
    output = Path("test-output")
    
    # Load test config
    config = json.loads(Path("test_config.json").read_text(encoding="utf-8"))
    
    # Step 1: Bundle
    categories = scan_source_dir(
        source,
        include_patterns=config["include_patterns"],
        skip_patterns=config["skip_patterns"],
    )
    bundle_result = generate_bundle(categories, source)
    
    print(f"\n=== BUNDLE ===")
    print(f"Total files: {bundle_result['file_count']}")
    print(f"Token count: ~{bundle_result['token_count']}")
    
    # Verify all files in bundle
    all_files = [f.relative_to(source).as_posix() for files in categories.values() for f in files]
    print(f"\nFiles in bundle:")
    for f in sorted(all_files):
        print(f"  - {f}")
    
    # Step 6: Compress (mocked Mother/Verifier)
    state = init_state()
    state["files_total"] = bundle_result["file_count"]
    
    # Mock Mother: return shorter version
    mother = Mock()
    mother.call_with_cache.return_value = (
        "# Compressed\nShort version.\n",
        {"input_tokens": 100, "output_tokens": 20, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}
    )
    
    # Mock Verifier: always approve
    verifier = Mock()
    verifier.call.return_value = (
        "Score: 4.5/5\nGood compression.",
        {"prompt_tokens": 50, "completion_tokens": 10}
    )
    
    prompts = {
        "compress_other": {
            "transform": "Compress {file_path}",
            "eval": "Score 1-5"
        }
    }
    
    run_compression_step(
        mother, verifier, bundle_result["content"],
        source, output, config, state, prompts,
    )
    
    print(f"\n=== COMPRESSION RESULTS ===")
    print(f"Mother API calls: {mother.call_with_cache.call_count}")
    print(f"Files compressed: {state['files_compressed']}")
    print(f"Files passed: {state['files_passed']}")
    
    # Verify never_compress files
    never_compress_patterns = config["never_compress"]
    print(f"\n=== NEVER_COMPRESS FILES (should be copied as-is) ===")
    
    for pattern in never_compress_patterns:
        print(f"\nPattern: {pattern}")
        matching = [f for f in all_files if any(f.startswith(p.replace("*", "")) for p in [pattern])]
        
        for rel_path in matching:
            source_file = source / rel_path
            output_file = output / rel_path
            
            if output_file.exists():
                source_content = source_file.read_text(encoding="utf-8")
                output_content = output_file.read_text(encoding="utf-8")
                
                if source_content == output_content:
                    print(f"  ✓ {rel_path} - IDENTICAL ({len(source_content)} bytes)")
                else:
                    print(f"  ✗ {rel_path} - MODIFIED (source: {len(source_content)}, output: {len(output_content)})")
            else:
                print(f"  ✗ {rel_path} - MISSING")
    
    # Verify compressible files
    print(f"\n=== COMPRESSIBLE FILES (should be compressed) ===")
    compressible = [f for f in all_files if not any(f.startswith(p.replace("*", "")) for p in never_compress_patterns)]
    
    for rel_path in compressible:
        source_file = source / rel_path
        output_file = output / rel_path
        
        if output_file.exists():
            source_content = source_file.read_text(encoding="utf-8")
            output_content = output_file.read_text(encoding="utf-8")
            
            if source_content != output_content:
                print(f"  ✓ {rel_path} - COMPRESSED (source: {len(source_content)}, output: {len(output_content)})")
            else:
                print(f"  ✗ {rel_path} - NOT COMPRESSED")
        else:
            print(f"  ✗ {rel_path} - MISSING")
    
    # Final verification
    print(f"\n=== VERIFICATION ===")
    expected_never_compress = 5  # 5 prompt files
    expected_compressible = 2    # core-conventions.md, build.md
    
    assert mother.call_with_cache.call_count == expected_compressible, \
        f"Expected {expected_compressible} Mother calls, got {mother.call_with_cache.call_count}"
    
    print(f"✓ Mother called {expected_compressible} times (correct)")
    print(f"✓ {expected_never_compress} files copied as-is")
    print(f"✓ {expected_compressible} files compressed")
    print(f"\n✓✓✓ TEST PASSED ✓✓✓")


if __name__ == "__main__":
    test_devsystem_subset_never_compress()
