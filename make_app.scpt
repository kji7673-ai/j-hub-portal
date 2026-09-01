set appPath to POSIX path of (path to me)
set shellCommand to "cd \"$(dirname " & quoted form of appPath & ")\" && python3 book_server.py"

tell application "Terminal"
    activate
    do script shellCommand
end tell

delay 2
do shell script "open http://localhost:5051"
