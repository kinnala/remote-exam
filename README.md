# remote-exam

A minimalistic Flask app for using [digabi/rich-text-editor](https://math-demo.abitti.fi/) in remote exams.

## Installing

Make sure that you have Python 3 and Flask, e.g.,
```
pip install flask
```
Then you can clone this repository:
```
git clone https://github.com/kinnala/remote-exam.git
```

## Starting the server

Run by
```
python app.py
```
Some important paths are printed to the console.
Periodically run
```
wget --content-disposition localhost:5000/<fetch-path-from-console>
```
to save the answers.

## Attending an exam

Each participant is given an url to a unique route, e.g.,
`/exam/mattimeikalainen1983298`.  The answers are saved to files
`answers/answer_<question-id>_mattimeikalainen1983298`.

## Creating questions

Modify `exercises.py` to add new questions.
