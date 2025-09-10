import tempfile
import csv
from email_app import EmailApp

def test_read_csv_file():
    # create a temporary csv file
    with tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False) as tmpfile:
        writer = csv.DictWriter(tmpfile, fieldnames=["Name", "Math", "Science"])
        writer.writeheader()
        writer.writerow({"Name": "Alice", "Math": "90", "Science": "85"})
        tmpfile_name = tmpfile.name

    app = EmailApp()
    rows = app.read_csv_file(tmpfile_name)

    assert len(rows) == 1
    assert rows[0]["Name"] == "Alice"
    assert rows[0]["Math"] == "90"
    assert rows[0]["Science"] == "85"


def test_create_email():
    app = EmailApp()
    email = app.create_email("teacher@school.com", "alice@school.com", "Report", "Hi Alice")

    assert email["from"] == "teacher@school.com"
    assert email["to"] == "alice@school.com"
    assert email["subject"] == "Report"
    assert email["body"] == "Hi Alice"


def test_send_email(capsys):
    app = EmailApp()
    email = {"from": "teacher@school.com", "to": "alice@school.com", "subject": "Report", "body": "Hi Alice"}
    
    app.send_email(email)

    # capture printed output
    captured = capsys.readouterr()
    assert "teacher@school.com" in captured.out
    assert "alice@school.com" in captured.out
    assert "Report" in captured.out
    assert "Hi Alice" in captured.out
