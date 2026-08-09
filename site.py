from pathlib import Path

# Write your website text here
website_content = "hi harmless ppl"<!DOCTYPE html>
<html>
<head>
    <title>owned by /chrxmaticc</title>
</head>
<body>
    <h1>welcome to /chrxmaticc son</h1>
    <p>/chrxmaticc owns you!</p>
</body>
</html>"""

# Define the file path
file_path = Path("index.html")

# Write the content to the file
file_path.write_text(website_content, encoding="utf-8")

print("Website text file created successfully!")
