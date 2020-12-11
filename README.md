# remote-exam

A tool on top of `digabi/rich-text-editor` for remote exams.

Run by
```
python app.py
```
After starting, a route to
fetch the answers is printed in the console.
Periodically run
```
wget --content-disposition localhost:5000/<fetch path from console>
```
to save the answers.
