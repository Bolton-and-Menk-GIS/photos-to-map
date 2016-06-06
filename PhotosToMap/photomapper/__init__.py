from template import template, oms
import gpsimage
import mimetypes
import json
import os
import string
import shutil
import glob
import webbrowser
import thread
import ctypes

__all__ = ['map_photos']

def msg_box(text='hello world!', title='Message', style=0):
    """display a message box

    Required:
        title -- title for message box
        text -- display message

    Optional:
        style -- style of msg box

      Styles:
          0 : OK
          1 : OK | Cancel
          2 : Abort | Retry | Ignore
          3 : Yes | No | Cancel
          4 : Yes | No
          5 : Retry | No
          6 : Cancel | Try Again | Continue
    """
    return ctypes.windll.user32.MessageBoxA(0, text, title, style)


def launch_page(html):
    """launches a web page, tries to find Google Chrome first, then defaults to
    default browser

    Required:
        html -- html page to launch
    """
    # look for chrome path first
    try:
        CHROME = glob.glob(r'C:\Program Files*\Google\Chrome\Application\chrome.exe')[0]
        webbrowser.get(CHROME.replace(os.sep, '/') + ' %s').open(html)
    except IndexError:
        webbrowser.open(html)

def get_direction(d):
    """determine direction from iPhone photos

    South -- range 135-225
    West -- range 225-315
    North -- range 315-45
    East -- range 45-135
    """
    if d >= 135 and d < 225:
        return 'South'
    elif d >= 225 and d < 315:
        return 'West'
    elif d >= 315 or d < 45:
        return 'North'
    else:
        return 'East'

def map_photos(folder, out_location='', app_name='my_photos', portable=True):
    """generates a simple google map web page showing geotagged photos

    Required:
        folder -- folder containing geotagged photos
        out_location -- location where to store the web app (only used when portable is True)

    Optional:
        app_name -- name of web app (will be folder name inside out_location)
        portable -- option to create a portable app, if false, the html web page
            will be stored in the same location as the photos.  When True, this will
            create a new folder inside of the out_location with an index.htm page
            and a copy of all the photos for the app to linked with relative paths.
    """
    OMS_COMPILED_NAME = 'oms.min.js'

    # validate name
    bad = string.punctuation.replace('_',' ')
    for b in bad:
        app_name = app_name.replace(b, '_')

    if portable:
        new_folder = os.path.join(out_location, app_name)
        im_folder = os.path.join(new_folder, 'images')
        bin_folder = os.path.join(new_folder, 'bin')
        html = os.path.join(new_folder, 'index.htm')
        for fold in [new_folder, im_folder, bin_folder]:
            if not os.path.exists(fold):
                os.makedirs(fold)
    else:
        html = os.path.join(folder, app_name + '.htm')
        bin_folder = os.path.join(folder, 'bin')
        if not os.path.exists(bin_folder):
            os.makedirs(bin_folder)

    points = []
    x_coords = []
    y_coords = []
    for fl in os.listdir(folder):
        full_path = os.path.join(folder, fl)
        try:
            im_type = mimetypes.guess_type(fl)[0].split('/')[0].lower()

            if im_type == 'image':

                im = gpsimage.open(full_path)

                if portable:
                    shutil.copy(full_path, os.path.join(im_folder, fl))
                    web_path = 'images/{}'.format(fl)
                else:
                    web_path = fl

                lon = im.geometry['coordinates'][0]
                lat = im.geometry['coordinates'][1]
                x_coords.append(lon)
                y_coords.append(lat)
                year, mo, day = map(int, im.timestamp.split()[0].split(':'))
                nice_time = '/'.join(map(str, [mo, day, year])) + ' ' + im.timestamp.split()[1]
                direction = get_direction(im.direction)
                style = 'width:{}px;height:{}px;'.format(*map(lambda x: x/10, im.size))
                img_tag = '<img src="{}" style="{}"></img>'.format(web_path, style)
                fields = '<br/>'.join(['<h3>Photo Name:  {}</h3>'.format(fl),
                                       'Date:  {}'.format(nice_time),
                                       'Latitude:  {}'.format(round(lat, 3)),
                                       'Longitude:  {}'.format(round(lon, 3)),
                                       'Direction:  {}'.format(direction),
                                       'Altitude:  {}'.format(round(im.altitude, 3)),
                                       'Phone Make:  {}'.format(im.make),
                                       'Phone Model:  {}'.format(im.model)])
                label = '<span>{}</span>'.format(fields)
                content = '<div>{}<br/><span>{}</span></div>'.format(label, img_tag)

                points.append({'lat': lat,
                               'lon': lon,
                               'img_title': fl,
                               'content' : content})

        except:
            pass

    if points:
        oms_file = os.path.join(bin_folder, OMS_COMPILED_NAME)
        points_file = os.path.join(bin_folder, 'points.js')

        with open(points_file, 'w') as f:
            f.write('points = ' + json.dumps(points, indent=2))

        with open(html, 'w') as f:
            f.write(template)

        with open(oms_file, 'w') as f:
            f.write(oms)

        thread.start_new_thread(launch_page, (html,))

    else:
        msg_box('Did not find any Geotagged Photos!', 'Warning')
