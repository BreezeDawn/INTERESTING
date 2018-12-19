from app import App, render_template,request

app = App()


@app.route('/index')
def index(url):
    if request.method == 'POST':
        print(request.form)
    return render_template(url)


@app.route('/Not_yet_done')
def not_yet_done(url):
    return render_template(url)


if __name__ == '__main__':
    app.run()

