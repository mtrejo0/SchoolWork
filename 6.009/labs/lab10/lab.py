import sys
import doctest
from http009 import http_response

sys.setrecursionlimit(10000)

# NO ADDITIONAL IMPORTS!

CHUNK_SIZE = 8192


def download_file(loc, cache = None):
    """
    Yield the raw data from the given URL, in segments of CHUNK_SIZE bytes.

    If the request results in a redirect, yield bytes from the endpoint of the
    redirect.

    If the given URL represents a manifest, yield bytes from the parts
    represented therein, in the order they are specified.

    Raises a RuntimeError if the URL can't be reached, or in the case of a 500
    status code.  Raises a FileNotFoundError in the case of a 404 status code.
    """

    # Try implementing cache as dictionary mapping "url" -> file data

    # Hint: consider making another function to handle manifests
    # Hint: b''.decode("utf-8") decodes a bytestring to a python string
    #       use this when deciding what URLs in the manifest to download again
    redirect = {301,302,307}



    # catch if there is a runtime error when you do http request
    try:
        data = http_response(loc)
    except:
        raise RuntimeError()
    type = data.getheader('content-type')


    if data.status == 404:
        # not found
        raise FileNotFoundError
    elif data.status == 500:
        # runtime
        raise RuntimeError
    elif data.status in redirect:
        # go somewhere else and download from there
        new = data.getheader('location')
        yield from download_file(new)

    elif data.status == 200:
        # succesful
        if ".parts" in loc or type == 'text/parts-manifest':
            # we have a manifest to look through

            # decode so we can understand it
            decode = data.read().decode("utf-8")

            # separate all the parts
            parts = decode.split("--\n")
            poss = []
            store = False
            if cache == None:
                cache = {}

            for p in parts:
                # in each part get each url
                urls = p.split("\n")[:-1]

                if "(*)" in urls:
                    # we have to cache some things
                    store = True

                for u in urls:
                    if u in cache:
                        # if weve seen it before return what we already have
                        yield cache[u]
                        break
                    try:
                        if store:
                            # if we have to cache things remember this url response and save it
                            cache[u] = b''.join(download_file(u))
                            for x in urls:
                                cache[x] = cache[u]
                            yield cache[u]
                            break
                        else:
                            # regular no cache go fetch the response and yield it
                            yield from download_file(u)
                            break
                    except:
                        continue


        elif ".jpg" not in loc and "stream" in type:
            # if its a continuous stream always yield the data
            while True:
                yield  data.read(CHUNK_SIZE)
        else:
            # not a stream and we should return chunks until there isnt anything
            bytes = data.read(CHUNK_SIZE)
            while bytes != b'':
                # while there is stuff to return return it
                yield bytes
                bytes = data.read(CHUNK_SIZE)


def files_from_sequence(stream):
    """
    yield the files from the sequence in the order they are specified.

    stream: the return value (a generator) of a download_file
                        call that represents a file sequence
    """

    # get the first thing of the stream
    def newIndex(func):
        # calculates the length of the file
        ans = 0
        for i in range(4):
            ans += 256 ** (4-i-1) * func[i]
        return ans + 4
    sequence = next(stream)

    while True:
        # get the length from the first 4 items of output
        i = newIndex(sequence)

        try:
            # add to the output
            sequence += next(stream)

            if  i < len(sequence):
                # if we have more than the index we just return file and cut the output we care about
                # return the relevant info
                yield sequence[4:i]

                # cut everything up to index and continue
                sequence = sequence[i:]

        except:
            # yield everything except the first 4 items
            yield sequence[4:i]
            # cya
            break








if __name__ == '__main__':
    """
    Remember you can use python3 gui.py URL_NAME to test your images!
    """
    pass
