def navigation_options(request):
    return {
        'nav_options': [
            ('/', 'Home'),
            ('/cuoora/social/', 'Social'),
            ('/cuoora/topics_of_interest/', 'Topics of Interest'),
            ('/cuoora/news/', 'News'),
            ('/cuoora/popular_today/', 'Popular Today'),
        ]
    }

def topics(request): #TODO
    pass


