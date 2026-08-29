import re

patron_dpi = r'^[0-9]{13}$'

patron_nit = r'^[0-9]+-?[0-9kK]$'

if re.match(patron_dpi, '2547891230145'):
    print('DPI valido')


if re.match(patron_nit, '5487621-K'):
    print('NIT valido')
