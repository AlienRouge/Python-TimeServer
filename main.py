from datetime import datetime
import pytz as tz
from tzlocal import get_localzone
import json

from json import JSONDecodeError
from pytz import UnknownTimeZoneError

HTML = """
<!DOCTYPE html>
<html style='font-family: Timeis, "Arial Black", "Arial-BoldMT", "Arial Bold", Arial,
Helvetica, sans-serif; color: #333; background-color: #edeef0;'>
  <head>
    <meta charset="utf-8" />
    <title>Time Online</title>
    <link rel="stylesheet" href="style.css">
    <meta http-equiv="Refresh" content="1" /> <!--DELETE TAG FOR STOP REFRESH-->
  </head>
  <body style="margin: 0; padding: 0;">
    <div style="background: #c35; color: #fff; font-size: 30px; padding-left: 3em;">Time.what</div>
    <main style="display: flex; flex-direction: column; text-align: center;">
      <div id="locrow" style="font-weight: bold; font-size: 52px"
      >{locationbox} time</div>
      <div
        id="timerow"
        style='font-size: 130px; font-weight: bold; margin-top: -40px; font-size: 11vw;
        font-weight: 900;'
      >{timebox}</div>
      <div
        id="daterow"
        style="margin: -40px 0 0 10em; font-weight: bold; font-size: 52px"
      >{datebox}</div>
    </main>
  </body>
</html>
"""


def time_app(environ, start_response):
    def get_post_data(_environ):
        received_data = _environ['wsgi.input'].read().decode("utf-8")
        try:
            received_data = json.loads(received_data)
        except JSONDecodeError:
            return None, None, b'JSON parsing failed.'
        try:
            received_type = received_data['date_type']
        except KeyError:
            return None, None, b'Date type key not found.'
        try:
            received_zones = received_data['timezones']
        except KeyError:
            received_zones = None  # Server timezone
        return received_type, received_zones, None

    def accept_post_zones(_date_type, zones):
        accepted_zones = []
        if type(zones) != list:
            return None, b'Timezones should be in "list" format'
        if (_date_type == 'date' or _date_type == 'time') and len(zones) == 1:
            try:
                accepted_zones.append(tz.timezone(zones[0]))
            except UnknownTimeZoneError:
                return None, b'Unknown time zone.'
        elif _date_type == 'datediff':
            if len(zones) == 2:
                try:
                    accepted_zones.append(tz.timezone(zones[0]))
                except UnknownTimeZoneError:
                    return None, b'First time zone is unknown.'
                try:
                    accepted_zones.append(tz.timezone(zones[1]))
                except UnknownTimeZoneError:
                    return None, b'Second time zone is unknown.'
            else:
                return None, b'Incorrect number of elements in "timezones" list. For "datediff" date type - Need(2).'
        else:
            return None, b'Invalid "date" type'
        return accepted_zones, None

    status = '200 OK'
    if environ['REQUEST_METHOD'] == 'POST':
        date_type, date_zones, error = get_post_data(environ)
        if error:
            start_response(status, [('Content-Type', 'text/plain')])
            return [error]

        time_zones = None
        if date_zones:
            time_zones, error = accept_post_zones(date_type, date_zones)
        elif date_type != 'datediff':
            time_zones = [get_localzone()]
        else:
            error = b'"None" in "timezones" argument. For "datediff" expected: list(zone1,zone2).'
        if error:
            start_response(status, [('Content-Type', 'text/plain')])
            return [error]

        if date_type == 'time':
            server_answer = {'Time': datetime.now(time_zones[0]).strftime('%X'), 'timezone': str(time_zones[0])}
        elif date_type == 'date':
            server_answer = {'Date': datetime.now(time_zones[0]).strftime('%b %d %Y'), 'timezone': str(time_zones[0])}
        else:
            first_time = datetime.now(tz=time_zones[0]).replace(tzinfo=None)
            second_time = datetime.now(tz=time_zones[1]).replace(tzinfo=None)
            if first_time > second_time:
                server_answer = "-" + str(first_time - second_time)
            else:
                server_answer = str(second_time - first_time)
            server_answer = {'date_diff': str(server_answer), 'first_zone': str(time_zones[0]),
                             'second_zone': str(time_zones[1])}

        start_response(status, [('Content-Type', 'text/plain')])
        return [bytes(json.dumps(server_answer), encoding='utf-8')]
    else:
        date_zones = environ['PATH_INFO'][1:]
        if date_zones:
            try:
                timezone = tz.timezone(date_zones)
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
    serve(time_app)
