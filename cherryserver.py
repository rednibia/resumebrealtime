from cherrypy import config, expose, quickstart
from ConfigParser import ConfigParser
from server_log import log
from os import getcwd, path
from puzzle import puzzle_solver

configuration = ConfigParser()
configuration.read("config.ini")

ip = configuration.get('Server Settings', 'IP Address')
port = int(configuration.get('Server Settings', 'Port'))
resume_url = configuration.get('Resume Settings', 'Resume Values')
github_url = configuration.get('Resume Settings', 'Github Url')


def response_decider(question, description):

    responseDict = dict()
    responseDict[u'Ping'] = "OK"
    responseDict[u'Position'] = ("Software Engineer with Fullstack, Backend,"
                                 " Data or Frontend experience")
    responseDict[u'Name'] = "Andrew Aibinder"
    responseDict[u'Email Address'] = "andrewaibinder@gmail.com"
    responseDict[u'Phone'] = "(203) 470-2092"
    responseDict[u'Resume'] = resume_url
    responseDict[u'Years'] = ("Amateur: 24 years. Full time: 20 months. Part "
                              "Time: 5 years.")
    responseDict[u'Degree'] = ("Masters: Western Connecticut State University"
                               ", Bachelors at University of Connecticut. "
                               "Neither are CS degrees.")
    responseDict[u'Status'] = "Yes. (US Citizen)"
    responseDict[u'Referrer'] = ("Through Indeed.com - I was contacted by "
                                 "Jenny Gasparis.")
    responseDict[u'Source'] = github_url

    if question in responseDict.keys():
        return responseDict[question]
    elif question == u'Puzzle':
        return puzzle_solver(description)
    else:
        return "NO RESPONSE"


class ResumeServer(object):
    @expose
    def index(self, **kwargs):

        log("Recieving: {}".format(kwargs))

        if 'q' in kwargs and 'd' in kwargs:
            question = kwargs['q']
            description = kwargs['d']
            response = response_decider(question, description)
        else:
            response = "Hello World"

        log("Responding: {}".format(response))

        return response


def main():

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': path.abspath(getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    config.update(
        {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Access-Control-Allow-Origin',
                                                '*')],
            'server.socket_host': ip,
            'server.socket_port': port
        })

    quickstart(ResumeServer(), '/', conf)


if __name__ == '__main__':
    main()
