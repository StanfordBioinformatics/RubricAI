# Input files

Do not commit study data to a public repository. The included files are minimal structural templates only.

## `Responses_clean.xlsx`

The supplied workbook already contains:

- a worksheet named `responses`; and
- the first-row headers `ID`, `pre_open1`, and `post_open1`.

Enter one de-identified participant per row. Add one response column for every additional pre/post question and use the exact same column names in `question_info.csv`.

Example structure:

| ID | pre_open1 | post_open1 | pre_open2 | post_open2 |
|---|---|---|---|---|
| P001 | ... | ... | ... | ... |

## `question_info.csv`

Required columns:

- `question_id`: stable question identifier, such as `Q1`;
- `topic`: short topic name;
- `pre_col`: matching pre-response column in the response workbook;
- `post_col`: matching post-response column;
- `question_text`: complete question wording;
- `module_id`: stable module identifier, such as `M1`; and
- `module_folder`: course-material folder name. If omitted, the pipeline uses `module_id`.

The supplied `question_info.csv` contains the required header row and one placeholder question mapping. Replace the placeholder values and add one row for each question.

## `course_folder/`

The supplied `course_folder/Module_1/module_content.ipynb` is a minimal placeholder. Replace its text with the actual module material and create one folder per additional module:

```text
course_folder/
├── Module_1/
│   ├── lesson_1.ipynb
│   └── lesson_2.ipynb
└── Module_2/
    └── lesson_1.ipynb
```

Remove credentials, participant information, and unrelated sensitive content from all notebooks before use or sharing.
