"""Central configuration for the open-ended response scoring pipeline.

Keep API credentials in environment variables or the existing environment file;
do not place secrets in this file.
"""

import os


PROMPT_INJECTION_CONFIG = {
    # Stage 3b is a conservative rule-based screen applied after text cleaning
    # and long-format reshaping. Matches are exported for
    # human review and retained in the pipeline; they are not automatically
    # deleted, relabeled, or excluded from scoring.
    "enabled": True,
    "case_sensitive": False,
    "output_filename": "prompt_injection_flags.csv",
    "patterns": {
        "instruction_override": (
            r"\b(?:ignore|disregard|forget|override)\b.{0,80}"
            r"\b(?:previous|prior|above|system|developer|instructions?|prompts?|rules?)\b"
        ),
        "prompt_extraction": (
            r"\b(?:reveal|show|display|print|repeat|return|provide)\b.{0,80}"
            r"\b(?:system|developer|hidden|original)\s+(?:prompt|message|instructions?)\b"
        ),
        "role_manipulation": (
            r"\b(?:act as|pretend to be|you are now)\b.{0,80}"
            r"\b(?:system|developer|administrator|unrestricted|jailbroken)\b"
        ),
        "safety_bypass": (
            r"\b(?:bypass|disable|circumvent|ignore)\b.{0,80}"
            r"\b(?:safety|guardrails?|filters?|restrictions?|rules?)\b"
        ),
        "jailbreak_terms": r"\b(?:jailbreak|DAN\s+mode|developer\s+mode)\b",
    },
}


MODEL_CONFIG = {
    # Models used to summarize course content, screen responses, and generate rubrics.
    # Set OPENAI_MODEL in llm-compare.env if you want to change the OpenAI model
    # without editing the notebook.
    "module_summary_model": {
        "provider": "openai",
        "model": os.getenv("OPENAI_MODEL", "gpt-5.2"),
    },
    "screen_model": {
        "provider": "openai",
        "model": os.getenv("OPENAI_MODEL", "gpt-5.2"),
    },
    "rubric_model": {
        "provider": "openai",
        "model": os.getenv("OPENAI_MODEL", "gpt-5.2"),
    },
    # Models used to score responses classified as scorable.
    # Provider names must match the wrappers in call_model_json().
    "scoring_models": [
        {
            "name": "openai_gpt",
            "provider": "openai",
            "model": os.getenv("OPENAI_MODEL", "gpt-5.2"),
        },
        {
            "name": "bedrock_claude",
            "provider": "aws_bedrock_claude",
            "model": os.getenv(
                "AWS_BEDROCK_MODEL_ID",
                "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            ),
        },
        {
            "name": "vertex_gemini",
            "provider": "gcp_vertex_gemini",
            "model": os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview"),
        },
    ],
    # Shared model response limit.
    "max_output_tokens": 10000,
}


SCORE_CONFIG = {
    # Fixed three-level scoring scale used by the rubric and scoring schemas.
    "scale_min": 1,
    "scale_max": 3,
    "score_labels": {
        1: "Beginner",
        2: "Intermediate",
        3: "Advanced",
    },
    # Policy for responses classified as insufficient.
    "insufficient_score": 1,
    "insufficient_label": "Beginner",
    # Pilot-response sample used to generate each question-specific rubric.
    "rubric_sample_prop": 1.0,
    "rubric_sample_min_n": 0,
    "rubric_sample_max_n": 1000,
    "rubric_sample_random_state": 42,
    # Screening, scoring, agreement, and retry settings.
    "screen_batch_size": 80,
    "scoring_batch_size": 80,
    "agreement_threshold": 0.60,
    "sleep_between_calls_sec": 0.0,
    "max_workers": 3,
    "fallback_max_retries": 1,
    # Maximum teaching-text extraction per course notebook.
    "max_markdown_chars_per_notebook": 12000,
    "max_code_comment_chars_per_notebook": 2000,
    # Set these to True to regenerate saved artifacts after changing data,
    # models, prompts, or scoring settings.
    "overwrite_module_summaries": False,
    "overwrite_question_outputs": False,
}
