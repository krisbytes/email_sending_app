import csv
import xml.etree.ElementTree as ET
from typing import List, Dict 

class EmailSender:

    def read_csv_file(self, file_path: str) -> List[Dict[str, str]]:# Method to read csv files
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not file_path:
            raise FileNotFoundError("file_path is empty")
        
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            return list(reader)
        
    def read_xml_file(self, file_path: str): # Method to read xml files
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not file_path:
            raise FileNotFoundError("file_path is empty")
        
        tree = ET.parse(file_path)
        return tree.getroot()

    def create_email(self, sender, recipient, subject, body) -> Dict[str, str]:  # Method to create email (only for CSV files)
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
    sender = EmailSender()
    sending_app = EmailSendingApp()
    
    file_path = input("Enter the file path: ").strip()
    
    if file_path.endswith(".csv"):
        rows = sender.read_csv_file(file_path)
        for row in rows:
            print(row)
        
    elif file_path.endswith(".xml"):
        root = sender.read_xml_file(file_path)
        print(f"Contents of {file_path}:")
        sending_app.send_xml(root)
        
    else:
        print("Unsupported file type.")    
