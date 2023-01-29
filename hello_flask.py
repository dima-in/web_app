from DBcm import UseDatabase, ConnectionError, CredentialError, SQLError
from httpagentparser import detect
from flask import Flask, render_template, request, escape, session, copy_current_request_context
from checker import check_logged_in
from threading import Thread
from time import sleep

app = Flask(__name__)

app.secret_key = 'metallica'


@app.route('/login/')
def login() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout/')
def logout() -> str:
    session.pop('logged_in')  # ключ удаляется, чтобы избежать KeyError
    return 'You are now logged out'


app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }


@app.route('/')
@app.route('/entry')
def enrty_page() -> 'html':
    return render_template('entry.html',
                           the_title='Добро пожаловать на поиск букв в веб!',
                           the_invitation='Введите данные в поля:',
                           the_clickbutton='Когда будете готовы, нажмите эту кнопку:')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Вот результаты:'
    submit_data = 'Были введены следующие данные: '
    results = str(search4letters(phrase, letters))

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:

        with UseDatabase(app.config['dbconfig']) as cursor:
            sleep(15)
            _SQL = """insert into log (phrase, letters, ip, browser_string, results) 
            values (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL,
                           (req.form['phrase'],
                            req.form['letters'],
                            req.remote_addr,
                            detect(req.environ.get('HTTP_USER_AGENT'))['browser']['name'],
                            res,))

    try:
        log_thread = Thread(target=log_request, args=(request, results))
        log_thread.start()
    except ConnectionError as err:
        print('Ошибка подключения к базе данных', str(err))
    except SQLError as err:
        print('Ошибка SQL запроса', str(err))
    except Exception as err:
        print('Ошибка в do_serch: ', str(err))
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,
                           the_submit_data=submit_data,
                           )


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """ select phrase, letters, ip, browser_string, results from log """
            cursor.execute(_SQL)
            list_tuple = cursor.fetchall()
            titles = ('Фраза', 'Буквы', 'IP адрес', 'Браузер', 'Результаты')
            return render_template('viewlog.html',
                                   the_title='Show log',
                                   the_row_titles=titles,
                                   the_data=list_tuple, )
    except ConnectionError as err:
        print('База данных не подключена? Ошибка: ', str(err))
    except CredentialError as err:
        print('Неверный логин или пароль. Ошибка: ', str(err))
    except Exception as err:
        print('Обнаружена ошибка:', str(err))


def search4letters(phrase: str, letter: str) -> set:
    return set(letter).intersection(set(phrase))


if __name__ == '__main__':
    app.run()
