# Open-Ended Response Scoring Pipeline

This repository contains a reproducible, question-by-question workflow for screening and scoring de-identified open-ended educational responses with multiple large language models (LLMs).

## Workflow

1. **Inputs:** Load de-identified responses, question metadata, and course materials.
2. **Module summarization:** Generate module-specific scoring context and pause for human approval.
3. **Preprocessing:**
   - **3a.** Clean response text and reshape the data to long format.
   - **3b.** Apply configurable regular-expression rules to flag potential prompt-injection patterns for human review.
4. **Response screening:** Classify responses as `insufficient` or `scorable`.
5. **Rubric generation:** Generate and calibrate a question-specific three-level rubric with anchor examples.
6. **Multi-model scoring:** Independently score scorable responses with configured LLMs, calculate a majority-vote consensus, and flag low-agreement cases.
7. **Human review and QC:** Review flagged cases and optionally replace the consensus score with a human-adjudicated score.
8. **Exports:** Save question-level and combined scored datasets, review queues, rubrics, summaries, and API-usage logs.

Prompt-injection flags are audit indicators. A regex match does not automatically delete, exclude, relabel, or rescore a response.

## Repository contents

- `RubricAI_pipeline.ipynb`: main executable notebook, with outputs and execution counts cleared.
- `RubricAI_config.py`: model, scoring, retry, batching, and prompt-injection settings.
- `requirements.txt`: Python dependencies.
- `.env.example`: credential-variable template; copy it to `.env` and enter credentials locally.
- `input/Responses_clean.xlsx`: response-data template with the required `responses` sheet and header row.
- `input/question_info.csv`: question-metadata template with the required header row and one placeholder mapping.
- `input/course_folder/Module_1/module_content.ipynb`: minimal course-material notebook template.
- `input/README.md`: concise input instructions.
- `.gitignore`: prevents credentials, study data, generated results, caches, and notebook checkpoints from being committed.

## Requirements

- Python 3.10 or later
- Jupyter Notebook or JupyterLab
- Access credentials for the model providers enabled in `RubricAI_config.py`

Install dependencies in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`.
2. Enter only the credentials and provider settings you need.
3. Review `RubricAI_config.py`, particularly:
   - model identifiers;
   - batch sizes and concurrency;
   - the three-level score labels;
   - the insufficient-response policy;
   - agreement and retry thresholds; and
   - the prompt-injection regex rules.

Never commit `.env`, cloud service-account files, raw responses, or generated results.

## Input files

Create these paths locally:

```text
input/
├── Responses_clean.xlsx
├── question_info.csv
└── course_folder/
    ├── Module_1/
    │   └── module_content.ipynb
    └── ...
```

The supplied response workbook contains a sheet named `responses` with the headers `ID`, `pre_open1`, and `post_open1`. Add one de-identified participant per row and add or rename response columns as needed. Keep `question_info.csv` synchronized with those column names. See `input/README.md` for details.

Only de-identified data should be used. Confirm that free-text responses do not contain names, contact information, institutional identifiers, or other protected information before running the pipeline.

## Running the pipeline

Start Jupyter from the repository root so relative paths resolve correctly:

```bash
jupyter lab
```

Open `RubricAI_pipeline.ipynb` and run the cells in order. The notebook pauses after module summarization for human approval.

The notebook may call paid APIs. Review provider pricing, batch sizes, model identifiers, and concurrency settings before running it on a full dataset.

## Generated outputs

The notebook creates an `output/` directory containing:

```text
output/
├── module_summaries/
├── screen/
├── rubrics/
├── results/
├── review/
│   ├── prompt_injection_flags.csv
│   └── flagged_for_review.csv
└── qc/
    ├── api_usage_log.jsonl
    └── api_usage_<run_id>.csv
```

Generated outputs are excluded by `.gitignore` because they may contain response text and model outputs.

## Reproducibility and human oversight

- Saved module summaries and question outputs are reused unless the corresponding overwrite setting is enabled.
- Model/provider identifiers and token usage are recorded for new API calls.
- Potential prompt injection, insufficient responses, low model agreement, and human adjudication are retained as auditable fields.
- Regex screening identifies possible patterns; it is not a definitive security classification.
- The final consensus score should not be treated as a substitute for appropriate human oversight in high-stakes settings.

## Sharing checklist

Before pushing changes to a public repository:

1. Confirm the notebook has no outputs or execution counts.
2. Confirm `.env`, `llm-compare.env`, service-account files, and credentials are absent.
3. Confirm `input/` contains templates only—not study data.
4. Confirm `output/` and review files are absent.
5. Search the repository for participant responses, names, email addresses, access keys, and local absolute paths.

## License

RubricAI is released under the [MIT License](LICENSE). This permits reuse, modification, and distribution provided that the copyright and license notice are retained. The software is provided without warranty.
