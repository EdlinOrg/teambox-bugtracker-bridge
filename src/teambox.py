import base64
import json
import urllib
import urllib2
import re

#import requests_oauthlib

import config


class Teambox():

    def __init__(self):
        self.teambox_projectid = config.TEAMBOX_PROJECTID
        self.teambox_tasklist_bugs = config.TEAMBOX_TASKLIST_ID
        self.teambox_tasklist_fixed = config.TEAMBOX_TASKLIST_FIXED_ID

        self.baseUrl = config.TEAMBOX_BASEURL
        self.baseUrl2 = config.TEAMBOX_BASEURL2
        self.teambox_username = config.TEAMBOX_USERNAME
        self.teambox_password = config.TEAMBOX_PASSWORD

    def connectionHelperGet(self, urlPart):
        # TODO: oauth2
        request = urllib2.Request(self.baseUrl + urlPart )

        base64string = base64.encodestring('%s:%s' % (self.teambox_username, self.teambox_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        data = response.read()
        return data

    def connectionHelperPost(self, urlPart, args, isPut):

        for k, v in args.iteritems():
            args[k] = unicode(v).encode('utf-8')

        enc_args = urllib.urlencode(args)

        # TODO: oauth2
        request = urllib2.Request(self.baseUrl + urlPart, enc_args )
        base64string = base64.encodestring('%s:%s' % (self.teambox_username, self.teambox_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        if(isPut):
            request.get_method = lambda: 'PUT'

        response = urllib2.urlopen(request)

        data = response.read()
        return data

    def connectionHelperApi2(self, urlPart, args, requestType):
        # TODO: oauth2

        if not 'GET' == requestType:
            for k, v in args.iteritems():
                args[k] = unicode(v).encode('utf-8')

            enc_args = urllib.urlencode(args)
            request = urllib2.Request(self.baseUrl2 + urlPart, enc_args )
        else:
            request = urllib2.Request(self.baseUrl2 + urlPart )

        base64string = base64.encodestring('%s:%s' % (self.teambox_username, self.teambox_password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

        if 'PUT' == requestType:
            request.get_method = lambda: 'PUT'

        if 'DELETE' == requestType:
            request.get_method = lambda: 'DELETE'

        response = urllib2.urlopen(request)

        data = response.read()
        return data

    def fetchTasks(self):
        data = self.connectionHelperGet('projects/' + self.teambox_projectid + '/task_lists/' + self.teambox_tasklist_bugs + '/tasks')
        ret = json.loads(data)
        return ret['objects']

    def fetchComments(self, task_id):
        data = self.connectionHelperGet('tasks/' + str(task_id) + '/comments')
        ret = json.loads(data)
        return ret

    def getTask(self, task_id):
        data = self.connectionHelperGet('projects/' + self.teambox_projectid + '/task_lists/' + self.teambox_tasklist_bugs + '/tasks/' + str(task_id) )
#        data= self.connectionHelperGet('tasks/' + str(task_id) )
        ret = json.loads(data)
        return ret

    def updateTask(self, taskId, data):
        urlPart = 'tasks/' + str(taskId)
        return self.connectionHelperPost(urlPart, data, True)

    def moveToResolved(self, taskId):
        urlPart = 'projects/' + self.teambox_projectid + '/task_lists/' + self.teambox_tasklist_fixed + '/tasks/reorder'
        data = { 'task_ids': taskId }
        return self.connectionHelperApi2(urlPart, data, 'PUT')

    def createComment(self, taskId, comment):
        args = { 'body': comment, 'project_id' : self.teambox_projectid }
        urlPart = 'tasks/' + taskId + '/comments#create'
        return self.connectionHelperPost(urlPart, args, False)

    def printTask(self, task):
        print "-----------------------------------"
        print "Id:\t\t" + str(task['id'])
        print "name:\t\t" + task['name']
        print "updated_at:\t" + task['updated_at']

    def prepareComment(self, aComment):
        str = aComment['text']
        url = 'https://teambox.com/#!/search/mt%3A'
        str = re.sub(r'#(\d+)(?!\w)' , r'#\1 (' + url + r'\1)', str)

        #add name of reporter first
        str = aComment['reporter']['name'] + ":\n" + str
        return str

    def deleteComment(self, id):
        urlPart = 'projects/' + self.teambox_projectid + '/comments/' + str( id )
        self.connectionHelperApi2(urlPart, {}, 'DELETE')
