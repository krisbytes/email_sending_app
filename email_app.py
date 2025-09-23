import csv
import xml.etree.ElementTree as ET
from typing import List, Dict, Union




    
class FormatReader:
    
    def read_file(self, file_path: str) -> Union[List[Dict[str, str]], ET.Element]:
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not file_path:
            raise FileNotFoundError("file_path is empty")
        
        if file_path.endswith(".csv"):
            return self.read_csv_file(file_path)
        elif file_path.endswith(".xml"):
            return self.read_xml_file(file_path)
        else:
            raise ValueError("Unsupported file format")
                    
    def read_csv_file(self, file_path: str) -> List[Dict[str, str]]:# Method to read csv files        
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            return list(reader)
        
    def read_xml_file(self, file_path: str): # Method to read xml files        
        tree = ET.parse(file_path)
        return tree.getroot()
    

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
    reader = FormatReader()
    sender = EmailSender()
    sending_app = EmailSendingApp()
    
    file_path = input("Enter the file path: ").strip()
    
    try:
        data = reader.read_file(file_path)
    
        if isinstance(data, list):
            for row in data:
                print(row)
        
        elif isinstance(data, ET.Element):
            print(f"Contents of {file_path}:")
            sending_app.send_xml(data)
        
    except Exception as e:
        print(f"Error: {e}")    
