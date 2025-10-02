import pytest
from typing import Protocol
import xml.etree.ElementTree as ET

from email_app import IFileFormatReader, FileReaderService, CsvReader, XmlReader

class DummyFileFormatReader:
    def __init__(self, handled_extensions=None, raise_on_read=False):
        self.handled_extensions = handled_extensions or []
        self.raise_on_read = raise_on_read
        
    def handles(self, file_path: str) -> bool:
        if file_path is None:
            raise ValueError("file_path cannot be None")
        return any(file_path.endswith(ext) for ext in self.handled_extensions)
    
    def read(self, file_path: str):
        if self.raise_on_read: 
            raise IOError("Failed to read file")
        return f"Contents of {file_path}"
    
@pytest.mark.parametrize(
    "handled_extensions, file_path, expected,desc",
    [
        ([".csv"], "data.csv", True, "csv handled"),
        ([".xml"], "data.xml", True, "xml handled"),
        ([".csv"], "data.xml", False, "csv reader unhandled xml"),
        ([".xml"], "data.csv", False, "xml reader unhandled csv"),
        ([], "data.csv", False, "no extensions handled"),
        ([".csv", ".xml"], "tree.xml", True, "multiple handled xml"),
        ([".csv", ".xml"], "tree.csv", True, "multiple handled csv"),
        ([".csv", ".xml"], "file.json", False, "unsupported extension"),
        ([".csv"], "", False, "empty file path"),
    ],
    ids=[
        "csv_lowercase",
        "xml_lowercase",
        "csv_reader_unhandled_xml",
        "xml_reader_unhandled_csv",
        "no_exts",
        "multi_xml",
        "multi_csv",
        "unsupported_ext",
        "empty_path"
    ],
)

def test_handles_extensions(handled_extensions, file_path, expected, desc):
    reader = DummyFileFormatReader(handled_extensions=handled_extensions)
    result = reader.handles(file_path)
    assert result is expected, f"Failed: {desc}"

@pytest.mark.parametrize(
    "file_path,expected_exception,desc",
    [
        (None, ValueError, "file_path is None"),
    ],
    ids=[
        "none_file_path",
    ]
)
def test_handles_error_cases(file_path, expected_exception, desc):
    reader = DummyFileFormatReader(handled_extensions=[".csv"])
    
    with pytest.raises(expected_exception):
        reader.handles(file_path)
        
@pytest.mark.parametrize(
    "file_path,raise_on_read,expected,desc",
    [
        ("data.csv", False, "Contents of data.csv", "read csv success"),
        ("tree.xml", False, "Contents of tree.xml", "read xml success"),
        ("data.csv", True, IOError, "read csv raises IOError"),
        ("tree.xml", True, IOError, "read xml raises IOError"),
    ],
    ids=[
        "read_csv_success",
        "read_xml_success",
        "read_csv_raises_ioerror",
        "read_xml_raises_ioerror",
    ]
)
def test_read_csv_and_xml_cases(file_path, raise_on_read, expected, desc):
    reader = DummyFileFormatReader(handled_extensions=[".csv", ".xml"], raise_on_read=raise_on_read)
    
    if raise_on_read:
        with pytest.raises(expected):
            reader.read(file_path)
    else:
        result = reader.read(file_path)
        
        assert result == expected, f"Failed: {desc}"

def test_protocol_structural_typing():
    class Impl:
        def handles(self, file_path: str) -> bool:
            return True
        def read(self, file_path: str):
            return "ok"
        
    impl = Impl()
    
    assert isinstance(impl, IFileFormatReader)
    assert impl.handles("data.csv") is True
    assert impl.read("tree.xml") == "ok"
    
def test_filereader_service_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")
    service = FileReaderService([CsvReader()])
    
    data = service.read_file(str(csv_file))
    assert data == [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    
def test_filereader_service_xml(tmp_path):
    xml_file = tmp_path / "data.xml"
    xml_file.write_text("<root><child>Hello</child></root>")
    service = FileReaderService([XmlReader()])
    
    root = service.read_file(str(xml_file))
    assert isinstance(root, ET.Element)
    assert root.tag == "root"
    assert root.find("child").text == "Hello"
    
def test_filereader_service_multiple_readers(tmp_path):
    csv_file = tmp_path / "data.csv"
    xml_file = tmp_path / "data.xml"
    csv_file.write_text("name,age\nTin,26")
    xml_file.write_text("<root><child>World</child></root>")
    service = FileReaderService([CsvReader(), XmlReader()])
    
    csv_data = service.read_file(str(csv_file))
    xml_data = service.read_file(str(xml_file))
    
    assert csv_data == [{"name": "Tin", "age": "26"}]
    assert xml_data.find("child").text == "World"
    
def test_filereader_unsupported_file():
    service = FileReaderService([CsvReader(), XmlReader()])
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        service.read_file("data.json")
    