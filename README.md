# Scrobbular

Scrobbular started out as a way to scrobble from [pianobar][], but it's really just a simple
interface that lets you scrobble and update now playing information. It can be used anywhere
that you can submit HTTP requests.

[pianobar]: https://github.com/PromyLOPh/pianobar

Scrobbular is hosted at [http://scrobbular.appspot.com/][s]. Anyone can sign up for an account with
Google credentials in a matter of seconds.

[s]: http://scrobbular.appspot.com/

Once a Scrobbular account has been created and authenticated with Last.fm, you can scrobble with an
HTTP request, like so:

    curl -X POST --data-urlencode "username=test@example.com" \
    --data-urlencode "s=secret" \
    --data-urlencode "track=Red Sky" \
    --data-urlencode "artist=Thrice" \
    --data-urlencode "album=Vheissu" \
    --data-urlencode "duration=258" \
    http://scrobbular.appspot.com/scrobble

More information can be found at the [Scrobbular howto page][howto].

[howto]: http://scrobbular.appspot.com/howto
