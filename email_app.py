import csv
from typing import List, Dict 




class EmailApp:

    def read_csv_file(self, file_path: str) -> List[Dict[str, str]]: # Method to read csv files
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            return list(reader)

    def create_email(self, sender, recipient, subject, body) -> Dict[str, str]:  # Method to create email
        return {"from": sender,
            "to": recipient,
            "subject": subject,
            "body": body}

    def send_email(self, email: Dict[str, str]) -> None: # Method to send email
        print(f"From: {email['from']}")
        print(f"To: {email['to']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")

if __name__ == "__main__":
    app = EmailApp()
    rows = app.read_csv_file("grades.csv")

    for row in rows:
        body = f"Hello {row['Name']}, here are your grades: {row}"
        email = app.create_email(
            sender="teacher@school.com",
            recipient=f"{row['Name'].lower()}@school.com",
            subject="Your Grades Report",
            body=body
        )
        app.send_email(email)
