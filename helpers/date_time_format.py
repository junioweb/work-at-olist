def strfdelta(tdelta, fmt):
    hours, rem = divmod(tdelta.total_seconds(), 3600)
    minutes, seconds = divmod(rem, 60)
    d = {
        'hours': '%.f' % hours,
        'minutes': '%.f' % minutes,
        'seconds': '%.f' % seconds,
    }
    return fmt.format(**d)
