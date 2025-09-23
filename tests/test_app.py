import os
import tempfile
import xml.etree.ElementTree as ET
import pytest

from email_app import FormatReader

happy_path_cases = [
    ("name,age\nAlice,30\nBob,25\n", ".csv",
     [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}],
     "csv_two_rows"),
    ("name,age\n", ".csv", [], "csv_header_only"),
    ("name,age\nNiño,30\nBób,25\n", ".csv",
     [{"name": "Niño", "age": "30"}, {"name": "Bób", "age": "25"}],
     "csv_special_characters"),
    ("<root><child name='foo'/></root>", ".xml", "root", "xml_root_one_child"),
    ("<root/>", ".xml", "root", "xml_only_root"),
]
@pytest.mark.parametrize(
    "file_content, file_ext, expected, test_id",
    happy_path_cases,
    ids=[case[-1] for case in happy_path_cases]
)
def test_read_file_happy_paths(file_content, file_ext, expected, test_id):
    # Arrange
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext, mode="w", encoding="utf-8") as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    reader = FormatReader()

    # Act
    if file_ext == ".csv":
        result = reader.read_file(tmp_path)
    else:
        xml_root = reader.read_file(tmp_path)
        result = xml_root.tag

    # Assert
    assert result == expected

    os.remove(tmp_path)

error_cases = [
    (None, TypeError, "file_path must be a string", "file_path_none"),
    (123, TypeError, "file_path must be a string", "file_path_int"),
    ("", FileNotFoundError, "file_path is empty", "file_path_empty"),
    ("file.unsupported", ValueError, "Unsupported file format", "unsupported_extension"),
]
@pytest.mark.parametrize(
    "file_path, expected_exception, expected_message, test_id",
    error_cases,
    ids=[case[-1] for case in error_cases]
)
def test_read_file_error_cases(file_path, expected_exception, expected_message, test_id):
    reader = FormatReader()

    # Act & Assert
    with pytest.raises(expected_exception) as exc_info:
        reader.read_file(file_path)
    assert expected_message in str(exc_info.value)


@pytest.mark.parametrize(
    "csv_content, expected, test_id",
    [
        # Edge: CSV with empty lines
        (
            "name,age\n\nAlice,30\n\nBob,25\n\n",
            [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}],
            "csv_with_empty_lines"
        ),
        # Edge: CSV with missing values
        (
            "name,age\nAlice,\n,Bob\n",
            [{"name": "Alice", "age": ""}, {"name": "", "age": "Bob"}],
            "csv_missing_values"
        ),
        # Edge: CSV with extra columns
        (
            "name,age,city\nAlice,30,Paris\nBob,25,London\n",
            [{"name": "Alice", "age": "30", "city": "Paris"}, {"name": "Bob", "age": "25", "city": "London"}],
            "csv_extra_columns"
        ),
    ],
    ids=lambda param: param[-1]
)
def test_read_csv_file_edge_cases(csv_content, expected, test_id):
    # Arrange
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    reader = FormatReader()

    # Act
    result = reader.read_csv_file(tmp_path)

    # Assert
    assert result == expected

    os.remove(tmp_path)


@pytest.mark.parametrize(
    "xml_content, expected_tag, test_id",
    [
        # Edge: XML with nested children
        (
            "<root><parent><child/></parent></root>",
            "root",
            "xml_nested_children"
        ),
        # Edge: XML with attributes
        (
            "<root attr='value'><child attr2='v2'/></root>",
            "root",
            "xml_with_attributes"
        ),
        # Edge: XML with namespaces
        (
            "<root xmlns:ns='http://example.com/ns'><ns:child/></root>",
            "root",
            "xml_with_namespace"
        ),
    ],
    ids=lambda param: param[-1]
)
def test_read_xml_file_edge_cases(xml_content, expected_tag, test_id):
    # Arrange
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8") as tmp:
        tmp.write(xml_content)
        tmp_path = tmp.name

    reader = FormatReader()

    # Act
    root = reader.read_xml_file(tmp_path)

    # Assert
    assert root.tag == expected_tag

    os.remove(tmp_path)


def test_read_csv_file_file_not_found():
    # Arrange
    reader = FormatReader()
    fake_path = "nonexistent_file.csv"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        reader.read_csv_file(fake_path)


def test_read_xml_file_file_not_found():
    # Arrange
    reader = FormatReader()
    fake_path = "nonexistent_file.xml"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        reader.read_xml_file(fake_path)


def test_read_xml_file_invalid_xml():
    # Arrange
    reader = FormatReader()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8") as tmp:
        tmp.write("<root><unclosed></root>")
        tmp_path = tmp.name

    # Act & Assert
    with pytest.raises(ET.ParseError):
        reader.read_xml_file(tmp_path)

    os.remove(tmp_path)
