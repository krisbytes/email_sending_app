import csv
import xml.etree.ElementTree as ET
from typing import List, Dict 

class EmailSender:

    def read_csv_file(self, file_path: str) -> List[Dict[str, str]]: # Method to read csv files
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            return list(reader)
        
    def read_xml_file(self, file_path: str) -> ET.Element: # Method to read xml files
        tree = ET.parse(file_path)
        return tree.getroot()

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
        print(f"{indent}<{element.tag}> {element.text.strip() if element.text else ''}")
        if element.text and element.text.strip():
            print(f"{indent}  {element.text.strip()}")
        for child in element:
            self.send_xml(child, level + 1)
        print(f"{indent}</{element.tag}>")

if __name__ == "__main__":
    sender = EmailSender()
    sending_app= EmailSendingApp()
    
    rows = sender.read_csv_file("grades.csv")

    for row in rows:
        body = f"Hello {row['Name']}, here are your grades: {row}"
        email = sender.create_email(
            sender="teacher@school.com",
            recipient=f"{row['Name'].lower()}@school.com",
            subject="Your Grades Report",
            body=body
        )
        sending_app.send_csv(email)

    root = sender.read_xml_file("country_data.xml")
    sending_app.send_xml(root)
    