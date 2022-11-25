from flask import Flask, render_template, request

app = Flask(__name__)




@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Вот результаты:'
    submit_data = 'Были введены следующие данные: '
    results = str(search4letters(phrase, letters))
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


def search4letters(phrase: str, letter: str) -> set:
    return set(letter).intersection(set(phrase))


if __name__ == '__main__':
    app.run()
