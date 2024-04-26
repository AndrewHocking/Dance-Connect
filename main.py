from markupsafe import Markup
from website import create_app
from urllib.parse import quote_plus

app = create_app()


@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = quote_plus(s)
    return Markup(s)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8123)
    # app.run(host="0.0.0.0", port=8123, debug=True)
    # app.run(debug=True)
    app.jinja_env.filters['quote_plus'] = lambda x: quote_plus(
        str(x)) if x else ''
