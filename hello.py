import webapp2
import pages

app = webapp2.WSGIApplication(
    [('/', pages.IndexPage),
    ('/auth', pages.AuthPage),
    ('/howto', pages.HowtoPage),
    ('/now_playing', pages.NowPlayingPage),
    ('/user', pages.UserPage),
    ('/scrobble', pages.ScrobblePage),
    ('/user/secret', pages.ChangeSecretPage),
    ('/user/delete', pages.DeleteUserPage)],
    debug=False
)
