import urllib.parse
import random
import secrets
import time
import zipfile
import logging
import os.path
from pathlib import Path
from io import BytesIO
from datetime import datetime
from flask import Flask, request, session, redirect, url_for, send_file
from exercises import questions


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.secret_key = secrets.token_bytes(10)
app.config.update(
    PERMANENT_SESSION_LIFETIME=36000  # 10 hours
)


@app.route('/save', methods=['POST'])
def save_answer():
    if 'id' not in session or 'uid' not in session:
        raise Exception("Session is broken.")
    qid = session['id']
    uid = session['uid']
    app.logger.info("{} saving status on answer {}".format(uid, qid))
    with open("answers/answer_{}_{}.html".format(qid, uid), "w") as handle:
        handle.write(urllib.parse.unquote_plus(request.get_data()[7:].decode('utf-8')))
    return {}


clear_route = secrets.token_urlsafe(10)
app.logger.info("Route for clearing the session cookie: /clear{}".format(clear_route))
@app.route('/clear{}'.format(clear_route))
def clear_session():
    session.clear()
    return r"Sessiokeksi tyhjennetty."


@app.route('/done')
def finish():
    if 'id' not in session or 'uid' not in session:
        raise Exception("Session is broken.")
    session['id'] = -1
    app.logger.info("DONE uid {} finished exam.".format(session['uid']))
    return r"<h1>Koe päättynyt</h1><p>Voit sulkea välilehden.</p>"


@app.route('/next')
def load_next():
    if 'uid' not in session:
        raise Exception("Session is broken")
    uid = session['uid']
    remaining = []
    for itr in range(len(questions)):
        if not os.path.exists("answers/answer_{}_{}.html".format(itr, uid)):
            remaining.append(itr)
    if len(remaining) == 0:
        return redirect(url_for('finish'))
    session['id'] = remaining[random.randint(0, len(remaining) - 1)]
    return redirect(url_for('index', uid=uid))


fetch_route = secrets.token_urlsafe(10)
app.logger.info("Route for fetching answers: /fetch{}".format(fetch_route))
@app.route('/fetch{}'.format(fetch_route))
def fetch_answers():
    pathlist = Path('answers').glob('*.html')
    files = [{
        'name': path.name,
        'data': path.read_text(),
    } for path in pathlist]
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for singlefile in files:
            data = zipfile.ZipInfo(singlefile['name'])
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, singlefile['data'])
    memory_file.seek(0)
    zipfilename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".zip"
    return send_file(memory_file, attachment_filename=zipfilename, as_attachment=True)


@app.route('/')
def test():
    return "<h1>Yhteystesti</h1><p>Yhteys koejärjestelmään toimii.  Odota, että saat opettajalta linkin varsinaiseen kokeeseen.</p>"


@app.route('/exam/<uid>')
def index(uid):
    if 'id' not in session:
        session['uid'] = uid
        return redirect(url_for('load_next'))
    if 'uid' in session:
        if not session['uid'] == uid:
            app.logger.info('CHEAT uid {} accessing {}'.format(session['uid'], uid))
            return "<h1>Huijaamisyritys havaittu</h1><p>Molempien osapuolten koesuoritukset mitätöidään.</p>"
    if session['id'] < 0:
        return redirect(url_for('finish'))
    qid = session['id']
    question = questions[qid](int.from_bytes(uid.encode("utf-8"), byteorder="big"))
    fname = "answers/answer_{}_{}.html".format(qid, uid)
    if os.path.exists(fname):
        with open(fname, "r") as handle:
            answer = handle.read()
    else:
        answer = ""
        with open(fname.format(qid), "w") as handle:
            handle.write("")
    return r"""
<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <title>remote-exam v0.1.0</title>
  <link rel="stylesheet" type="text/css" href="//unpkg.com/@digabi/mathquill/build/mathquill.css">
  <link rel="stylesheet" type="text/css" href="//unpkg.com/rich-text-editor/dist/rich-text-editor.css"/>
  <script src="//code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/bacon.js/1.0.1/Bacon.min.js"></script>
  <script src="//unpkg.com/rich-text-editor/dist/rich-text-editor-bundle.js"></script>
  <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js">
  </script>
  <style>
    body { margin-top: 50px; font-family: sans-serif;}
    h1 {font-size: 2em; line-height: 2; margin-bottom: 4em;}
    .answer { border: 1px solid #aaa; padding: 5px; box-sizing: content-box; min-height: 100px; font: 17px "Times New Roman"; }
    .rich-text-editor img[src^="data:image/svg+xml"] { vertical-align: middle; margin: 4px; padding: 3px 10px; cursor: pointer; border: 1px solid transparent; }
    .rich-text-editor.rich-text-focused img[src^="data:image/svg+xml"],
    .rich-text-editor:focus img[src^="data:image/svg+xml"] { background: #EDF9FF; border: 1px solid #E6F2F8; }
    .rich-text-editor img[src*="data:image/png"] { margin: 4px; }
    .rich-text-editor:focus img[src*="data:image/png"],
    .rich-text-editor.rich-text-focused img[src*="data:image/png"] { box-shadow: 0 0 3px 1px rgba(0, 0, 0, .2); }
    .result { display: none; }
  </style>
</head>
<body>
<article>
  <section>
    <h1>Koe</h1>
    <h2>Kysymys</h2>
""" + question + r"""
    <h2>Vastaus</h2>
    <div class="answer" id="answer1">
""" + answer + r"""</div>
    <a class="confirm" href="/next">Seuraava tehtävä</a>
  </section>
</article>
<div class="result">\({}\)</div>
<script>
  MathJax.Hub.Config({
    jax: ["input/TeX", "output/SVG"],
    extensions: ["toMathML.js", "tex2jax.js", "MathMenu.js", "MathZoom.js", "fast-preview.js", "AssistiveMML.js", "a11y/accessibility-menu.js"],
    TeX: {
      extensions: ["AMSmath.js", "AMSsymbols.js", "noErrors.js", "noUndefined.js", "mhchem.js"]
    },
    SVG: {useFontCache: true, useGlobalCache: false, EqnChunk: 1000000, EqnDelay: 0, font: 'STIX-Web'}
  })

  const answer = document.querySelector('#answer1')
  makeRichText(answer, {
    screenshot: {
      saver: ({data}) =>
        new Promise(resolve => {
          const reader = new FileReader()
          reader.onload = evt => resolve(evt.target.result.replace(/^(data:image)(\/[^;]+)(;.*)/,'$1$3'))
          reader.readAsDataURL(data)
        })
    },
    baseUrl: 'http://localhost:5000',
    updateMathImg: ($img, latex) => {
      updateMath(latex, svg => {
        $img.prop({
          src: svg,
          alt: latex
        })
        $img.closest('[data-js="answer"]').trigger('input')
      })
    }
  })

  let math = null
  MathJax.Hub.queue.Push(() => {
    math = MathJax.Hub.getAllJax('MathOutput')[0]
  })

  function saveAnswer() {
    $.post("/save", {answer: $(".answer").html()});
    setTimeout(saveAnswer, 5000);
  }

  $(document).ready(function() {
    setTimeout(saveAnswer, 5000);
  });

  $(".confirm").on("click", function(event){
      $.post("/save", {answer: $(".answer").html()});
      if(confirm("Onko tehtävä varmasti valmis? Aikaisempiin tehtäviin ei voi palata.")){
         return true;
      } else {
          event.preventDefault();
          return false;
      }
  });
  
  const encodeMultibyteUnicodeCharactersWithEntities = (str) =>
    str.replace(/[^\x00-\xFF]/g, c => `&#${c.charCodeAt(0).toString(10)};`)

  const updateMath = function (latex, cb) {
    MathJax.Hub.queue.Push(['Text', math, '\\displaystyle{' + latex + '}'])
    MathJax.Hub.Queue(() => {
      if ($('.result svg').length) {
        const $svg = $('.result svg').attr('xmlns', "http://www.w3.org/2000/svg")
        $svg.find('use').each(function () {
          const $use = $(this)
          if ($use[0].outerHTML.indexOf('xmlns:xlink') === -1) {
            $use.attr('xmlns:xlink', 'http://www.w3.org/1999/xlink') //add these for safari
          }
        })
        let svgHtml = $svg.prop('outerHTML')
        //firefox fix
        svgHtml = svgHtml.replace(' xlink=', ' xmlns:xlink=')
        // Safari xlink ns issue fix
        svgHtml = svgHtml.replace(/ ns\d+:href/gi, ' xlink:href')
        cb('data:image/svg+xml;base64,' + window.btoa(encodeMultibyteUnicodeCharactersWithEntities(svgHtml)))
      } else {
        cb('data:image/svg+xml;base64,' + window.btoa(`<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="17px" height="15px" viewBox="0 0 17 15" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <title>Group 2</title>
    <defs></defs>
    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <g transform="translate(-241.000000, -219.000000)">
            <g transform="translate(209.000000, 207.000000)">
                <rect x="-1.58632797e-14" y="0" width="80" height="40"></rect>
                <g transform="translate(32.000000, 12.000000)">
                    <polygon id="Combined-Shape" fill="#9B0000" fill-rule="nonzero" points="0 15 8.04006 0 16.08012 15"></polygon>
                    <polygon id="Combined-Shape-path" fill="#FFFFFF" points="7 11 9 11 9 13 7 13"></polygon>
                    <polygon id="Combined-Shape-path" fill="#FFFFFF" points="7 5 9 5 9 10 7 10"></polygon>
                </g>
            </g>
        </g>
    </g>
</svg>`))
      }
    })
  }

  let studentDisplay = null
  MathJax.Hub.Queue(function () {
    studentDisplay = MathJax.Hub.getAllJax(document.querySelector('.result'))[0];
  })
  const trackError = (e = {}) => {
    const category = 'JavaScript error'
    const action = e.message
    const label = e.filename + ':' + e.lineno
  }

  if (window.addEventListener) {
    window.addEventListener('error', trackError, false)
  } else if (window.attachEvent) {
    window.attachEvent('onerror', trackError)
  } else {
    window.onerror = trackError
  }

  const reader = new FileReader()
  reader.onload = x => $('.answer').html(x.target.result)

</script>
</body>
</html>
"""

app.run(host= '0.0.0.0')
