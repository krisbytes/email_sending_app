import pytest
import xml.etree.ElementTree as ET
from email_app import EmailSender

# -------------------- read_csv_file tests --------------------

@pytest.mark.parametrize(
    "csv_content,expected,case_id",
    [
        (
            "name,email\nAlice,alice@example.com\nBob,bob@example.com\n",
            [
                {"name": "Alice", "email": "alice@example.com"},
                {"name": "Bob", "email": "bob@example.com"},
            ],
            "csv_happy_path_two_rows"
        ),
        (
            "name,email\nAlice,alice@example.com\n",
            [
                {"name": "Alice", "email": "alice@example.com"},
            ],
            "csv_happy_path_single_row"
        ),
        (
            "name,email\n",
            [],
            "csv_happy_path_header_only"
        ),
        (
            "name,email\nAlice,\n,Bob@example.com\n",
            [
                {"name": "Alice", "email": ""},
                {"name": "", "email": "Bob@example.com"},
            ],
            "csv_edge_missing_values"
        ),
        (
            "",
            [],
            "csv_edge_empty_file"
        ),
        (
            "name,email\nAlice,alice@example.com\nBob,\n",
            [
                {"name": "Alice", "email": "alice@example.com"},
                {"name": "Bob", "email": ""},
            ],
            "csv_edge_missing_email"
        ),
    ],
    ids=lambda param: param if isinstance(param, str) else None
)
def test_read_csv_file_happy_and_edge_cases(tmp_path, csv_content, expected, case_id):
    
    # Arrange
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content, encoding="utf-8")
    sender = EmailSender()

    # Act
    result = sender.read_csv_file(str(file_path))

    # Assert
    assert result == expected

@pytest.mark.parametrize(
    "file_path,expected_exception,case_id",
    [
        ("nonexistent.csv", FileNotFoundError, "csv_error_file_not_found"),
        (None, TypeError, "csv_error_none_file_path"),
        (123, TypeError, "csv_error_non_string_file_path"),
        ("", FileNotFoundError, "csv_error_empty_string_file_path"),
    ],
    ids=lambda param: param if isinstance(param, str) else None
)
def test_read_csv_file_error_cases(file_path, expected_exception, case_id):
    
    # Arrange
    sender = EmailSender()

    # Act & Assert
    with pytest.raises(expected_exception):
        sender.read_csv_file(file_path)

# -------------------- read_xml_file tests --------------------

@pytest.mark.parametrize(
    "xml_content,expected_tag,expected_attrib,expected_text,case_id",
    [
        (
            "<root><child>data</child></root>",
            "root",
            {},
            None,
            "xml_happy_path_simple"
        ),
        (
            "<root/>",
            "root",
            {},
            None,
            "xml_happy_path_empty_root"
        ),
        (
            "<root attrib='value'><child/></root>",
            "root",
            {"attrib": "value"},
            None,
            "xml_happy_path_with_attrib"
        ),
        (
            "<root>Text</root>",
            "root",
            {},
            "Text",
            "xml_edge_text_in_root"
        ),
    ],
    ids=lambda param: param if isinstance(param, str) else None
)
def test_read_xml_file_happy_and_edge_cases(tmp_path, xml_content, expected_tag, expected_attrib, expected_text, case_id):
    
    # Arrange
    file_path = tmp_path / "test.xml"
    file_path.write_text(xml_content, encoding="utf-8")
    sender = EmailSender()

    # Act
    root = sender.read_xml_file(str(file_path))

    # Assert
    assert root.tag == expected_tag
    assert root.attrib == expected_attrib
    if expected_text is not None:
        assert root.text == expected_text
    else:
        # .text may be None or whitespace depending on XML, so just check type
        assert root.text is None or isinstance(root.text, str)

@pytest.mark.parametrize(
    "xml_content,case_id",
    [
        ("<root><unclosed></root>", "xml_error_malformed"),
        ("<root><child></root>", "xml_error_mismatched_tag"),
        ("", "xml_error_empty_file"),
    ],
    ids=lambda param: param if isinstance(param, str) else None
)
def test_read_xml_file_parse_errors(tmp_path, xml_content, case_id):
    
    # Arrange
    file_path = tmp_path / "bad.xml"
    file_path.write_text(xml_content, encoding="utf-8")
    sender = EmailSender()

    # Act & Assert
    with pytest.raises(ET.ParseError):
        sender.read_xml_file(str(file_path))

@pytest.mark.parametrize(
    "file_path,expected_exception,case_id",
    [
        ("nonexistent.xml", FileNotFoundError, "xml_error_file_not_found"),
        (None, TypeError, "xml_error_none_file_path"),
        (123, TypeError, "xml_error_non_string_file_path"),
        ("", FileNotFoundError, "xml_error_empty_string_file_path"),
    ],
    ids=lambda param: param if isinstance(param, str) else None
)
def test_read_xml_file_file_errors(file_path, expected_exception, case_id):
    
    # Arrange
    sender = EmailSender()

    # Act & Assert
    with pytest.raises(expected_exception):
        sender.read_xml_file(file_path)

# -------------------- create_email tests --------------------

@pytest.mark.parametrize(
    "sender_addr,recipient,subject,body,expected,case_id",
    [
        (
            "alice@example.com", "bob@example.com", "Hello", "Hi Bob!",
            {"from": "alice@example.com", "to": "bob@example.com", "subject": "Hello", "body": "Hi Bob!"},
            "email_happy_path"
        ),
        (
            "", "", "", "",
            {"from": "", "to": "", "subject": "", "body": ""},
            "email_edge_all_empty"
        ),
        (
            "a"*1000, "b"*1000, "s"*1000, "body"*1000,
            {"from": "a"*1000, "to": "b"*1000, "subject": "s"*1000, "body": "body"*1000},
            "email_edge_long_strings"
        ),
        (
            None, None, None, None,
            {"from": None, "to": None, "subject": None, "body": None},
            "email_edge_all_none"
        ),
        (
            "alice@example.com", None, "Subject", "",
            {"from": "alice@example.com", "to": None, "subject": "Subject", "body": ""},
            "email_edge_some_none"
        ),
    ],
    ids=lambda param: param if isinstance(param, str) else None
)
def test_create_email(sender_addr, recipient, subject, body, expected, case_id):
    
    # Arrange
    email_sender = EmailSender()

    # Act
    result = email_sender.create_email(sender_addr, recipient, subject, body)

    # Assert
    assert result == expected
