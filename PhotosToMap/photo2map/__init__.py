from template import *
import gpsimage
import mimetypes
import json
import os
import string
import shutil
import webbrowser

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

def photos_to_map(folder, out_location, app_name='my_photos'):
    """generates a simple google map web page showing geotagged photos

    Required:
        folder -- folder containing geotagged photos
        out_location -- location where to store the web app

    Optional:
        app_name -- name of web app (will be folder name inside out_location)
    """

    # validate name
    bad = string.punctuation.replace('_',' ')
    for b in bad:
        app_name = app_name.replace(b, '_')

    new_folder = os.path.join(out_location, app_name)
    im_folder = os.path.join(new_folder, 'images')
    for fold in [new_folder, im_folder]:
        if not os.path.exists(fold):
            os.makedirs(fold)

    points = []
    x_coords = []
    y_coords = []
    for fl in os.listdir(folder):
        full_path = os.path.join(folder, fl)
        try:
            im_type = mimetypes.guess_type(fl)[0].split('/')[0].lower()

            if im_type == 'image':

                im = gpsimage.open(full_path)
                lon = im.geometry['coordinates'][0]
                lat = im.geometry['coordinates'][1]
                x_coords.append(lon)
                y_coords.append(lat)
                year, mo, day = map(int, im.timestamp.split()[0].split(':'))
                nice_time = '/'.join(map(str, [mo, day, year])) + ' ' + im.timestamp.split()[1]
                direction = get_direction(im.direction)
                style = 'width:{}px;height:{}px;'.format(*map(lambda x: x/10, im.size))
                img_tag = '<img src="images/{}" style="{}"></img>'.format(fl, style)
                label = '<span>{}</span>'.format('<br/>'.join(['<h3>Photo Name: {}</h3>'.format(fl),
                                                        'Date: {}'.format(nice_time),
                                                        'Latitude: {}'.format(round(lat, 3)),
                                                        'Longitude: {}'.format(round(lon, 3)),
                                                        'Direction: {}'.format(direction),
                                                        'Altitude: {}'.format(round(im.altitude, 3)),
                                                        'Phone Make: {}'.format(im.make),
                                                        'Phone Model: {}'.format(im.model)]))
                content = '<div>{}<br/><span>{}</span></div>'.format(label, img_tag)

                points.append({'lat': lat,
                               'lon': lon,
                               'img_title': fl,
                               'content' : content})

                shutil.copy(full_path, os.path.join(im_folder, fl))

        except:
            pass

    if points:
        points_json = json.dumps(points, indent=4, sort_keys=True)
        html = os.path.join(new_folder, 'index.htm')
        with open(html, 'w') as f:
            latlong = ', '.join(map(str, [sum(x_coords) / float(len(x_coords)),
                                         sum(y_coords) / float(len(y_coords))]))

            f.write(''.join([part1, points_json, part2, latlong, part3]))
        webbrowser.open(html)

if __name__ == '__main__':

    folder = r'C:\Users\calebma\Desktop\google_maps\images'
    out = r'C:\Users\calebma\Desktop'
    photos_to_map(folder, out, 'google_test')
