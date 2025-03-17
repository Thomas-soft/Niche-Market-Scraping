import utils.errors as error


def check_args(args):
    """
    Check the arguments passed to the script.

    args:
        args : list : The list of arguments passed to the script.

    return:
        search_query : str : The search query to be used on Google.
        number_of_sites : int : The number of sites to scrape.
        latitude (optional) : float : The latitude of the location to search from.
        longitude (optional) : float : The longitude of the location to search
    """

    if len(args) not in [3, 5]:
        error.usage_error()

    search_query = args[1]

    try:
        number_of_sites = int(args[2])
    except ValueError:
        error.must_be_integer_error()

    latitude = None
    longitude = None

    if len(args) == 5:
        try:
            latitude = float(args[3])
            longitude = float(args[4])
        except ValueError:
            error.must_be_float_error()
    
    return search_query, number_of_sites, latitude, longitude