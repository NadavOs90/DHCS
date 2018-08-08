import json
import re


def validate_date(date):
    solution = re.sub(r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) [0-3][0-9] [0-9][0-9][0-9][0-9]',
                      "", date)
    return True if solution == '' else False


def validate_location(loc):
    loc = loc.replace(' ', '') + ','
    solution = re.sub(r'([a-z]|[A-Z]|[0-9]|,)+,', "", loc)
    return True if solution == '' else False


def validate_concert(json_string):
    try:
        json.loads(json_string)
    except:
        return False
    json_string = json_string.replace("\t", "").replace("\n", "").replace(" ", "").replace('\r', '')
    # remove date from string
    solution = re.sub(r'{\"date":\"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[0-3][0-9][0-9][0-9][0-9][0-9]\",',
                      "", json_string)
    # remove location
    solution = re.sub(r'\"location\":\"([a-z]|[A-Z]|[0-9]|,)+\",', "", solution)
    # remove setlist
    solution = re.sub(r'\"setlist\":\[((\"([a-z]|[A-Z]|[0-9]|.)+\"),)+(\"([a-z]|[A-Z]|[0-9]|.)+\")\]\}', "", solution)
    return True if solution == '' else False


def validate_song(json_string):
    try:
        json.loads(json_string)
    except:
        return False
    json_string = json_string.replace("\t", "").replace("\n", "").replace(" ", "").replace('\r', '')
    # remove song title
    solution = re.sub(r'{\"song_title\":\"([a-z]|[A-Z]|[0-9]|.)+\",', "", json_string)
    # remove album
    solution = re.sub(r'\"album\":\"([a-z]|[A-Z]|[0-9])+\",', "", solution)
    # remove lyrics
    solution = re.sub(r'\"lyrics\":\[((\"([a-z]|[A-Z]|[0-9]|.)+\"),)+', "", solution)
    solution = re.sub(r'\"([a-z]|[A-Z]|[0-9]|.)+\"\]\}', "", solution)
    return True if solution == '' else False


def validate_album(json_string):
    try:
        json.loads(json_string)
    except:
        return False
    json_string = json_string.replace("\t", "").replace("\n", "").replace(" ", "").replace('\r', '')
    # remove album name
    solution = re.sub(r'{\"album_name\":\"([a-z]|[A-Z]|[0-9]|.)+\",', "", json_string)
    # remove release year
    solution = re.sub(r'\"release_year\":[0-9][0-9][0-9][0-9],', "", solution)
    # remove setlist
    solution = re.sub(r'\"songs\":\[((\"([a-z]|[A-Z]|[0-9]|.)+\"),)+(\"([a-z]|[A-Z]|[0-9]|.)+\")\]\}', "", solution)
    return True if solution == '' else False
