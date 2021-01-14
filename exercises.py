import urllib.parse
import random

questions = []

def question1(seed):
    random.seed(seed)
    alkuluvut = [5, 7, 11, 13]
    alkuluku = random.choice(alkuluvut)
    return (r"""Määritä <img src="https://latex.codecogs.com/png.latex?{}" />."""
            .format(urllib.parse.quote_plus(r"4^{\log_{2}" + str(alkuluku) + r"}")))

questions.append(question1)

def question2(seed):
    random.seed(seed)
    luku1 = random.choice([2, 4, 6, 8, 10])
    luku2 = random.choice([3, 5, 7, 9, 11])
    return (r"""Perustele ilman laskinta kumpi on isompi: <img src="https://latex.codecogs.com/png.latex?{}" /> vai <img src="https://latex.codecogs.com/png.latex?{}" />?"""
            .format(
                urllib.parse.quote_plus(r"\log_{" + str(luku1) + r"}" + str(luku2)),
                urllib.parse.quote_plus(r"\log_{" + str(luku2) + r"}" + str(luku1))
            ))

questions.append(question2)


def question3(seed):
    random.seed(seed)
    kantaluku = random.choice([2, 3, 4, 5, 6])
    diffi = random.choice([4, 5, 6, 7])
    return (r"""Ratkaise yhtälö <img src="https://latex.codecogs.com/png.latex?{}" />."""
            .format(urllib.parse.quote_plus(r"\log_{" + str(kantaluku) + r"}(x-2)=1-\log_{" + str(kantaluku) + r"}(x-" + str(diffi) + r")")))

questions.append(question3)


def question4(seed):
    random.seed(seed)
    kantaluku = random.choice([2, 3, 4, 5])
    rhs = 4 * kantaluku
    return (r"""Ratkaise yhtälö <img src="https://latex.codecogs.com/png.latex?{}" />."""
            .format(urllib.parse.quote_plus(str(kantaluku) + r"^{x^2}=" + str(rhs))))

questions.append(question4)
