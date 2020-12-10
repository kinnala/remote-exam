import urllib.parse
import random

questions = []

def question1(seed):
    random.seed(seed)
    return r"""Ilmaise luvun 3 potenssina <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus(r"\frac{1}{" + str(int(3 ** random.randint(2, 3))) + r"\sqrt{3^{" + str(random.randint(3, 7)) + r"}}}"))

questions.append(question1)

def question2(seed):
    random.seed(seed)
    return r"""Mikä on funktion <img src="https://latex.codecogs.com/png.latex?{}" /> määrittelyjoukko?""".format(urllib.parse.quote_plus(r"f(x)=\sqrt[" + str(random.randint(2, 5) * 2) + r"]{1-x^" + str(random.randint(2, 5)) + r"}"))

questions.append(question2)


def question3(seed):
    random.seed(seed)
    return r"""Ratkaise yhtälö <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus(r"\sqrt{" + str(random.randint(2, 5)) + r"x-" + str(random.randint(1, 3)) + r"}=" + str(random.randint(2, 5)) + r"x-" + str(random.randint(3, 8))))

questions.append(question3)


def question4(seed):
    random.seed(seed)
    return r"""Derivoi <img src="https://latex.codecogs.com/png.latex?{}" />.""".format(urllib.parse.quote_plus(r"\sqrt[" + str(random.randint(3, 7)) + r"]{" + str(random.randint(2, 8)) + r"x+5}"))

questions.append(question4)
