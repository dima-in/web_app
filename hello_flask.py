from flask import Flask, render_template, request, escape

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')
    print(sep='\n')


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
def view_the_log() -> 'str':
    with open('vsearch.log') as log:
        return escape(log.read())


def search4letters(phrase: str, letter: str) -> set:
    return set(letter).intersection(set(phrase))


if __name__ == '__main__':
    app.run()
