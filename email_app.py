import csv
import xml.etree.ElementTree as ET
from typing import List, Dict, Protocol, runtime_checkable

@runtime_checkable
class IFileFormatReader(Protocol):
    def handles(self, file_path: str) -> bool: ...
    def read(self, file_path: str): ...

class CsvReader:
    def handles(self, file_path: str) -> bool:
        return file_path.endswith(".csv")
    
    def read(self, file_path: str) -> List[Dict[str, str]]:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            return list(reader)
    
class XmlReader: 
    def handles(self, file_path: str) -> bool:
        return file_path.endswith(".xml")
    
    def read(self, file_path: str):
        tree = ET.parse(file_path)
        return tree.getroot()

class FileReaderService: 
    def __init__(self, readers: List[IFileFormatReader]):
        self.readers = readers

    def read_file(self, file_path: str):
        for reader in self.readers:
            if reader.handles(file_path):
                return reader.read(file_path)
        raise ValueError("Unsupported file format")
                    
    
class EmailSender:
    def create_email(self, sender, recipient, subject, body) -> Dict[str, str]:  # Method to create email
        return {"from": sender,
            "to": recipient,
            "subject": subject,
            "body": body}


class EmailSendingApp:
    def send_csv(self, email: Dict[str, str]) -> None: # Method to send csv file
        print(f"From: {email['from']}")
        print(f"To: {email['to']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")

    def send_xml(self, element: ET.Element, level=0): #method to send xml file
        indent = "  " * level
        text = element.text.strip() if element.text and element.text.strip() else ""
        print(f"{indent}<{element.tag}> {f'{text}' if text else ''}")
        for child in element:
            self.send_xml(child, level + 1)
        print(f"{indent}</{element.tag}>")

if __name__ == "__main__":
    file_reader_service = FileReaderService([CsvReader(), XmlReader()])
    sender = EmailSender()
    sending_app = EmailSendingApp()
    
    file_path = input("Enter the file path: ").strip()
    
    try:
        data = file_reader_service.read_file(file_path)
    
        if file_path.endswith(".csv"):
            for row in data:
                print(row)
        
        elif file_path.endswith(".xml"):
            print(f"Contents of {file_path}:")
            sending_app.send_xml(data)
        
    except Exception as e:
        print(f"Error: {e}")   
