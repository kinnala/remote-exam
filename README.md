# remote-exam

An attempt to build a tool on top of digabi/rich-text-editor for remote exams.

The idea is to run one server instance per student. The app will first ask for a
name and then show one question at a time with rich-text-editor below.  The
answer is stored over page reloads. Pushing a button below the text area will
store the final answer and show the next question.

Run by
```
flask run
```
