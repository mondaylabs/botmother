def location_field(location):
    """ translate location format to google maps format """

    if not location:
        return

    return {
        'lon': location['longitude'],
        'lat': location['latitude']
    }
