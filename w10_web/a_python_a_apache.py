# httpd.conf:
# přidat
# AddHandler cgi-script .py
# případně
# ScriptInterpreterSource Registry-Strict

# v xampp/htdocs pak přidat index.py:
#!C:\Users\stemb\AppData\Local\Programs\Python\Python311\python.exe
print("Content-Type: text/html\n\n")

print("Hello world! Python works!")