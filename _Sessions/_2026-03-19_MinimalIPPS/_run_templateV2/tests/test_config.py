"""Tests for pipeline config schema and loading (TK-001, TK-002)."""
import json
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "pipeline_config.json"


class TestPipelineConfigV2Schema:
    """TK-001: Validate V2 config format."""

    def setup_method(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def test_models_are_strings(self):
        """Model values must be plain strings, not objects."""
        models = self.config["models"]
        assert isinstance(models["mother"], str), f"mother is {type(models['mother'])}"
        assert isinstance(models["verifier"], str), f"verifier is {type(models['verifier'])}"

    def test_no_output_dir(self):
        """output_dir removed in V2."""
        assert "output_dir" not in self.config

    def test_reasoning_effort_present(self):
        assert "reasoning_effort" in self.config
        assert self.config["reasoning_effort"] in [
            "none", "minimal", "low", "medium", "high", "xhigh",
        ]

    def test_output_length_present(self):
        assert "output_length" in self.config

    def test_budget_warning_threshold(self):
        budget = self.config["budget"]
        assert "warning_threshold" in budget
        assert 0.0 <= budget["warning_threshold"] <= 1.0
        assert "warn_at_percent" not in budget

    def test_required_fields_present(self):
        """All required top-level fields exist."""
        required = [
            "source_dir", "models", "thresholds", "budget",
            "file_type_map", "include_patterns", "skip_patterns",
            "never_compress", "api_timeout_seconds",
        ]
        for field in required:
            assert field in self.config, f"Missing required field: {field}"

    def test_guardrails_unchanged(self):
        """source_dir, thresholds, include/skip/never_compress must not disappear."""
        assert "source_dir" in self.config
        assert self.config["thresholds"]["judge_min_score"] == 3.5
        assert "*.md" in self.config["include_patterns"]


class TestConfigLoading:
    """TK-002: Config loading from configs/ directory."""

    def test_config_loading_from_configs_dir(self):
        """TC-01: All 3 JSON config files load successfully."""
        from lib.llm_client import _MODEL_REGISTRY, _PARAMETER_MAPPING, _MODEL_PRICING
        assert len(_MODEL_REGISTRY.get("model_id_startswith", [])) > 0
        assert "effort_levels" in _PARAMETER_MAPPING or "effort_mapping" in _PARAMETER_MAPPING
        assert "pricing" in _MODEL_PRICING

    def test_config_missing_dir(self, tmp_path, monkeypatch):
        """TC-24: FileNotFoundError includes path when configs/ dir missing."""
        import lib.llm_client as mod
        monkeypatch.setattr(mod, "_CONFIGS_DIR", tmp_path / "nonexistent")
        with pytest.raises(FileNotFoundError, match="nonexistent"):
            mod._load_json_config("model-registry.json")

    def test_pricing_standard_tier(self):
        """Pricing tier is standard; opus-4-6 input >= $10/MTok."""
        configs_dir = PROJECT_ROOT / "configs"
        with open(configs_dir / "model-pricing.json", "r", encoding="utf-8") as f:
            pricing = json.load(f)
        assert pricing["_pricing_tier"] == "standard"
        opus = pricing["pricing"]["anthropic"]["claude-opus-4-6-20260204"]
        assert opus["input_per_1m"] >= 10.0
