import urllib.parse
import random
import os.path
from flask import Flask, request, session, redirect, url_for, send_from_directory


app = Flask(__name__)
app.secret_key = b'yaddayadda'


questions = [
    'Tervetuloa suorittamaan etäkoetta.  Järjestelmä näyttää yhden tehtävän kerrallaan.  Aikaisempaan tehtävään ei voi palata.  Kirjoita nimesi alla olevaan kenttään ja paina "Seuraava tehtävä".',
]
questions.append(r"""Ratkaise yhtälö <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus("3x^2+3x-18=0")))
questions.append(r"""Ratkaise epäyhtälö <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus("x^3<x")))
questions.append(r"""Sievennä <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus("\sqrt{40}")))
questions.append(r"""Sievennä <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus(r"\frac{x^2-1}{x+1}")))
questions.append(r"""Montako juurta on toisen asteen polynomilla, jonka diskriminantti on 3? (Pelkkä luku riittää.)""")
questions.append(r"""Montako juurta on polynomilla <img src="https://latex.codecogs.com/png.latex?{}" />? (Pelkkä luku riittää.)""".format(urllib.parse.quote_plus("x^2+2x+1")))


@app.route('/save', methods=['POST'])
def save_answer():
    if 'id' not in session:
        raise Exception("Question id not found!")
    if 'uid' not in session:
        raise Exception("User id not found!")
    qid = session['id']
    uid = session['uid']
    with open("answer_{}_{}.html".format(qid, uid), "w") as handle:
        handle.write(urllib.parse.unquote_plus(request.get_data()[7:].decode('utf-8')))
    return {}


@app.route('/done')
def finish():
    if 'id' not in session:
        raise Exception("Question id not found!")
    session['id'] = -1
    if 'uid' not in session:
        raise Exception("User id not found!")
    print("DONE uid {} finished exam.".format(session['uid']))
    return r"Koe on päättynyt. Voit sulkea välilehden."


@app.route('/next')
def load_next():
    if 'id' not in session:
        raise Exception("Question id not found!")
    if 'uid' not in session:
        raise Exception("User id not found!")
    uid = session['uid']
    remaining = []
    for itr in range(len(questions)):
        if not os.path.exists("answer_{}_{}.html".format(itr, uid)):
            remaining.append(itr)
    if len(remaining) == 0:
        return redirect(url_for('finish'))
    session['id'] = remaining[random.randint(0, len(remaining) - 1)]
    return redirect(url_for('index', uid=uid))


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def test():
    return "Yhteys koejärjestelmään toimii.  Odota, että saat opettajalta linkin varsinaiseen kokeeseen."


@app.route('/exam/<uid>')
def index(uid):
    if 'id' not in session:
        session['id'] = 0
        session['uid'] = uid
    if 'uid' in session:
        if not session['uid'] == uid:
            print('CHEAT uid {} accessing {}'.format(session['uid'], uid))
            return "Huijaamisyritys havaittu.  Molempien osapuolten koesuoritukset mitätöidään."
    if session['id'] < 0:
        return redirect(url_for('finish'))
    qid = session['id']
    question = questions[qid]
    fname = "answer_{}_{}.html".format(qid, uid)
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
  <title>Etäkoe</title>
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
    <h1>Etäkoe</h1>
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

  $(function () {
      $(".answer").on("keyup", function (e) {
        $.post("/save", {answer: $(".answer").html()});
      });
  });

  $(".confirm").on("click", function(event){
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
