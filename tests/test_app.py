import os
import tempfile
import pytest
from email_app import EmailSender  

@pytest.fixture
def sender():
    return EmailSender()

@pytest.mark.parametrize(
    "csv_content,expected,case_id",
    [
        (
            "Name,Grade\nAlice,A\nBob,B\n",
            [
                {"Name": "Alice", "Grade": "A"},
                {"Name": "Bob", "Grade": "B"},
            ],
            "happy_path_two_rows",
        ),
        (
            "Name,Grade\n\n",
            [],
            "header_only_empty_row",
        ),
        (
            "",
            [],
            "empty_file",
        ),
        (
            "Name,Grade\nAlice,A\nBob,\n,Carlo\n",
            [
                {"Name": "Alice", "Grade": "A"},
                {"Name": "Bob", "Grade": ""},
                {"Name": "", "Grade": "Carlo"},
            ],
            "missing_values",
        ),
        (
            "col1,col2,col3\n1,2,3\n4,5,6\n",
            [
                {"col1": "1", "col2": "2", "col3": "3"},
                {"col1": "4", "col2": "5", "col3": "6"},
            ],
            "multiple_columns",
        ),
    ],
    ids=lambda x: x if isinstance(x, str) else None,
)
def test_read_csv_file_happy_and_edge_cases(sender, csv_content, expected, case_id):
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, newline="", encoding="utf-8") as tmp:
        tmp.write(csv_content)
        tmp.flush()
        tmp_path = tmp.name

    # Act
    result = sender.read_csv_file(tmp_path)

    # Assert
    assert result == expected

    # Cleanup
    os.remove(tmp_path)

@pytest.mark.parametrize(
    "bad_path,expected_exception,case_id",
    [
        ("nonexistent.csv", FileNotFoundError, "file_not_found"),
        ("/this/path/does/not/exist.csv", FileNotFoundError, "path_not_found"),
    ],
    ids=lambda x: x if isinstance(x, str) else None,
)
def test_read_csv_file_file_not_found(sender, bad_path, expected_exception, case_id):
    # Act & Assert
    with pytest.raises(expected_exception):
        sender.read_csv_file(bad_path)