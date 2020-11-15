from datetime import datetime
import pytz as tz
from tzlocal import get_localzone
import json

from json import JSONDecodeError
from pytz import UnknownTimeZoneError

HTML = """
<!DOCTYPE html>
<html style="margin: 0; padding: 0; font-family: Arial">
  <head>
    <meta charset="utf-8" />
    <title>Time Online</title>
    <meta http-equiv="Refresh" content="1" /> <!--DELETE TAG FOR STOP REFRESH-->
  </head>
  <body>
    <main style="text-align: center; font-family: cursive; margin: auto">
      <div id="header" style="font-weight: bold; font-size: 36px"
      >{locationbox} time</div>
      <div
        id="timerow"
        style="font-size: 130px; font-weight: bold; margin-top: -30px"
      >{timebox}</div>
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


def app(environ, start_response):
    status = '200 OK'
    if environ['REQUEST_METHOD'] == 'POST':
        received_data = environ['wsgi.input'].read().decode("utf-8")
        try:
            received_data = json.loads(received_data)
        except JSONDecodeError:
            start_response(status, [('Content-Type', 'text/plain')])
            return [b'JSON parsing failed.']
        try:
            date_type = received_data['date_type']
        except KeyError:
            start_response(status, [('Content-Type', 'text/plain')])
            return [b'Date type key not found. ']
        try:
            set_timezone = received_data['timezones']
        except KeyError:
            set_timezone = None
        time_zones = []
        if set_timezone:
            if type(set_timezone) != list:
                start_response(status, [('Content-Type', 'text/plain')])
                return [b'Timezones should be in "list" format']
            if len(set_timezone) == 1:
                try:
                    time_zones.append(tz.timezone(set_timezone[0]))
                except UnknownTimeZoneError:
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [b'Unknown time zone.']
            else:
                try:
                    time_zones.append(tz.timezone(set_timezone[0]))
                except UnknownTimeZoneError:
                    start_response(status, [('Content-Type', 'text/plain')])
                    return [b'First time zone is unknown.']
                try:
                    time_zones.append(tz.timezone(set_timezone[1]))
                except UnknownTimeZoneError:
                    start_response(status, [('Content-Type', 'text/plain')])
                    return [b'Second time zone is unknown.']
        else:
            time_zones.append(get_localzone())
        if date_type == 'time':
            server_answer = {'Time': datetime.now(time_zones[0]).strftime('%X'), 'timezone': str(time_zones[0])}
        elif date_type == 'date':
            server_answer = {'Date': datetime.now(time_zones[0]).strftime('%b %d %Y'), 'timezone': str(time_zones[0])}

        elif date_type == 'datediff':
            if len(time_zones) < 2:
                start_response(status, [('Content-Type', 'text/plain')])
                return [b'Invalid number of "timezones" arguments for "datediff" - Need(2).']
            first_time = datetime.now(tz=time_zones[0]).replace(tzinfo=None)
            second_time = datetime.now(tz=time_zones[1]).replace(tzinfo=None)
            if first_time > second_time:
                server_answer = "-" + str(first_time - second_time)
            else:
                server_answer = str(second_time - first_time)
            server_answer = {'date_diff': str(server_answer), 'first_zone': str(time_zones[0]),
                             'second_zone': str(time_zones[1])}
        else:
            start_response(status, [('Content-Type', 'text/plain')])
            return [b'Invalid "date" type']
        start_response(status, [('Content-Type', 'text/plain')])
        return [bytes(json.dumps(server_answer), encoding='utf-8')]
    else:
        set_timezone = environ['PATH_INFO'][1:]
        if set_timezone:
            try:
                timezone = tz.timezone(set_timezone)
            except(tz.UnknownTimeZoneError, AttributeError):
                start_response(status, [('Content-type', 'text/plain; charset=utf-8')])
                return [b'Error. Unknown Timezone']
            city = str(timezone).split('/')[-1]
        else:
            timezone = get_localzone()
            city = "Server"
        output_date = datetime.now(tz=timezone)

        start_response(status, [('Content-type', 'text/html')])
        html = HTML.format(timebox=output_date.strftime('%X'), locationbox=city,
                           datebox=output_date.strftime('%b %d %Y'))
        html_as_bytes = html.encode('utf-8')
        return [html_as_bytes]


if __name__ == '__main__':
    from paste import reloader
    from paste.httpserver import serve

    reloader.install()
    serve(app)
