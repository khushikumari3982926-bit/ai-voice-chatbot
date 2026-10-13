
from pathlib import Path

import pandas as pd

# Locate the dataset relative to this Python file.
DATA_FILE = Path(__file__).parent / "data" / "qa_dataset.csv"


def load_dataset(file_path):
    """Load a CSV or Excel question-answer dataset."""

    suffix = file_path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(file_path)
    elif suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Please provide a CSV or Excel file.")

    return df


def prepare_dataset(file_path):
    """Validate and clean the question-answer dataset."""

    df = load_dataset(file_path)

    # Normalize column names.
    df.columns = df.columns.str.strip().str.lower()

    required_columns = {"question", "answer"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Dataset must contain 'question' and 'answer' columns."
        )

    # Keep only the columns needed by our application.
    df = df[["question", "answer"]].copy()

    # Remove rows with missing questions or answers.
    df = df.dropna(subset=["question", "answer"])

    # Convert values to strings and remove extra whitespace.
    for column in ["question", "answer"]:
        df[column] = df[column].astype(str).str.strip()

    # Remove empty questions and answers.
    df = df[
        (df["question"] != "")
        & (df["answer"] != "")
    ]

    # Remove duplicate question-answer pairs.
    df = df.drop_duplicates(
        subset=["question", "answer"]
    )

    # Reset row numbering after cleaning.
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid question-answer records found.")

    return df


if __name__ == "__main__":
    dataset = prepare_dataset(DATA_FILE)

    print("\nDataset loaded successfully!")
    print(f"Valid records: {len(dataset)}")

    print("\nPrepared dataset:")
    print(dataset.to_string(index=False))
