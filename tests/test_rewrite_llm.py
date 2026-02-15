import server.rewrite_llm as rllm


def test_llm_rewrite_uses_model_generate():
    out = rllm.rewrite_to_american_english("i'm name is john")
    assert isinstance(out, str)
    assert out.startswith("gpt4all-corrected:")


def test_llama32_prompt_contains_fields():
    p = rllm.llama32_prompt("SYSTEM", "USER")
    assert "SYSTEM" in p
    assert "USER" in p
    assert "<|start_header_id|>assistant" in p


def test_model_instance_receives_prompt():
    _ = rllm.rewrite_to_american_english("can you fix this?")
    assert hasattr(rllm.model, "last_prompt")
    assert "can you fix this?" in rllm.model.last_prompt
