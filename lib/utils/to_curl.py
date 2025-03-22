from _md5 import md5

# based on curlify https://github.com/ofw/curlify/pull/23/files

try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote


def to_curl(request, compressed=False, verify=True):
    """
    Returns string with curl command by provided request object

    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    """
    parts = [
        ('curl', None),
        ('-X', request.method),
    ]

    for k, v in sorted(request.headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, v))]

    if request.body:
        parts += [handle_body(request.body)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, request.url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(quote(k))
        if v:
            flat_parts.append(quote(v))

    return ' '.join(flat_parts)


def handle_body(body):
    """Return proper command part for request body
    Arguments:
        body {None|string|bytes} -- a request body
    Returns:
        tuple -- a command part
    """
    data_arg = '-d'
    if isinstance(body, bytes):
        try:
            body = body.decode('utf-8')
        # handle binary files
        except UnicodeDecodeError:
            body = f'@{md5(body).hexdigest()}'
            data_arg = '--data-binary'
    return (data_arg, body)
