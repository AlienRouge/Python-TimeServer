from datetime import datetime
import pytz as tz

HTML = """
<!DOCTYPE html>
<html style="margin: 0; padding: 0; font-family: Arial">
  <head>
    <meta charset="utf-8" />
    <title>Time Online</title>
  </head>
  <body>
    <main style="text-align: center; font-family: cursive; margin: auto">
      <div class="header" style="font-weight: bold; font-size: 36px">
        {locationbox} time
      </div>
      <div
        class="timerow"
        style="font-size: 130px; font-weight: bold; margin-top: -30px"
      >
        {timebox}
      </div>
      <div
        class="footer"
        style="margin: -1em 0 0 10em; font-weight: bold; font-size: 40px"
      >
       {datebox}
      </div>
    </main>
  </body>
</html>
"""


def simple_app(environ, start_response):
    status = '200 OK'
    print(environ['REQUEST_METHOD'])

    set_timezone = environ['PATH_INFO'][1:]
    if set_timezone:
        try:
            timezone = tz.timezone(set_timezone)
        except(tz.UnknownTimeZoneError, AttributeError):
            start_response(status, [('Content-type', 'text/plain; charset=utf-8')])
            return [b'Error. Unknown Timezone']
        city = str(timezone).split('/')[1]
    else:
        timezone = None
        city = "Server"
    output_date = datetime.now(tz=timezone)

    start_response(status, [('Content-type', 'text/html')])
    html = HTML.format(timebox=output_date.strftime('%X'), locationbox=city, datebox=output_date.strftime('%b %d %Y'))
    html_as_bytes = html.encode('utf-8')
    return [html_as_bytes]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    with make_server('', 9090, simple_app) as httpd:
        print("Serving on http://localhost:9090/.")
        httpd.serve_forever()
