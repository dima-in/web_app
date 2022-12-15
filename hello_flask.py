import mysql.connector
from DBcm import UseDatabase

from flask import Flask, render_template, request, escape
app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    dbconfig = {'host': '127.0.0.1', 'user': 'vsearch', 'password': 'vsearchpasswd', 'database': 'vsearchlogDB', }

    with UseDatabase(dbconfig) as cursor:

        _SQL = """insert into log (phrase, letters, ip, browser_string, results) values (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res))

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Вот результаты:'
    submit_data = 'Были введены следующие данные: '
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,
                           the_submit_data=submit_data, )


@app.route('/')
@app.route('/entry')
def enrty_page() -> 'html':
    return render_template('entry.html', the_title='Добро пожаловать на поиск букв в веб!',
                           the_invitation='Введите данные в поля:',
                           the_clickbutton='Когда будете готовы, нажмите эту кнопку:')


@app.route('/viewlog')
def view_the_log() -> 'html':

    with open('vsearch.log') as log:
        list_str = []
        for line in log:
            list_str.append([])
            for sep_str in line.split('|'):
                list_str[-1].append(escape(sep_str))
    titles = ('Данные формы', 'IP адрес', 'Браузер', 'Результаты')
    return render_template('viewlog.html', the_title='показать log',
                           the_row_titles=titles,
                           the_data=list_str,)


def search4letters(phrase: str, letter: str) -> set:
    return set(letter).intersection(set(phrase))


if __name__ == '__main__':
    app.run()
