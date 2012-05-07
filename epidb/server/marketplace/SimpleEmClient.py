#!/usr/bin/python
# Simple EM Client
#
#


#imports
import os, urllib2, re, xml.dom.minidom, base64, pickle, sys, optparse, getpass, xml.etree.ElementTree, StringIO, time

from xml.etree.ElementTree import ElementTree

import xml.etree.ElementTree as ET

from optparse import OptionParser

from urllib2 import Request, urlopen, URLError, HTTPError

import subprocess
from subprocess import PIPE

#for tables
import locale
locale.setlocale(locale.LC_NUMERIC, "")

import sys
out = sys.stdout


#use the methods and classes defined in semc(backup).py
sys.path.append(os.getcwd())

collections = dict()
resources = dict()
user = None

resourceURL = None
collectionURL = None
RegexResourcePID = None
RegexCollectionPID = None
CollectionResourceXPath = None
loginURL = None


#
# User Class
#
#

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

#
# Resource Class
#
#

class Resource:
    def __init__(self, pid, folder, data=None, name=None):

        global resourceURL, RegexResourcePID

        regex = re.compile(RegexResourcePID)
        
        self.id = regex.findall(pid)[0]

        self.url = resourceURL.replace("$PID", self.id)

        if folder[-1] == "/":
            folder = folder[0:-1]

        if os.path.isdir(folder) == False :
            os.mkdir(folder)

        self.folder = folder
        
        self.data = data
        
        self.name = name

    def checkForUpdate(self):

        #Currently always returns true. Future updates will include checking the filenames in the folder.

        return True

    def getResource(self):
      try:
        file1 = getURL(user, self.url)

      except HTTPError, e:
        print "Resource Not Found!"
        print e
        print self.url
        sys.exit(0)

      #try with ElementTree
      xmlStr = ' '.join(file1.split())
      tree = ElementTree()

      xmlTree = tree.parse(StringIO.StringIO(xmlStr))

      #print ET.tostring(xmlTree)
      #print xmlStr

      titleList = xmlTree.findall("result/title/")

      if len(titleList) > 0:
        self.name = titleList[0].text

      #foreach <file>
      files = xmlTree.findall("result/file/")

      for f in files:
        #get <name>
        name = f.findall("name")[0].text

        #get <data>
        data = f.findall("content")[0].text

        #file2 open self.folder, name
        file2 = open(os.path.join(self.folder, name), "w")

        #file2.write(base64.decodestring(data))
        file2.write(base64.decodestring(data))

        #file2.close
        file2.close()

      metaDC = xmlTree.findall("result/metadata_DC")
      #if metadata_DC exists
      if len(metaDC) == 1 :
        metaElement = metaDC[0]

        #name = self.name + "_metadata_DC.xml"
        name = self.name + "_metadata_DC.xml"        

        #metadata = get <metadata_dc> childnodes to string
        metaChildren = metaElement.getchildren()
        
        if len(metaChildren) > 0 :
          metadataDC = metaChildren[0]
          metadataString = xml.etree.ElementTree.tostring(metadataDC)
        #file2 open self.folder, name
          file2 = open(os.path.join(self.folder, name), "w")

        #file2.write(metadata)
          file2.write(metadataString)

        #file2.close
          file2.close()


      metaEM = xmlTree.findall("result/metadata_EM")
      #if metadata_EM exists
      if len(metaEM) == 1 :
        metaElement = metaEM[0]

        #name = self.name + "_metadata_EM.xml"
        name = self.name + "_metadata_EM.xml"        

        #metadata = get <metadata_dc> childnodes to string
        metaChildren = metaElement.getchildren()
        
        if len(metaChildren) > 0 :
          metadataEM = metaChildren[0]
          metadataString = xml.etree.ElementTree.tostring(metadataEM)
        #file2 open self.folder, name
          file2 = open(os.path.join(self.folder, name), "w")

        #file2.write(metadata)
          file2.write(metadataString)

        #file2.close
          file2.close()


#
# Collection Class
#
#

class Collection:
    def __init__(self, pid, folder, resources=dict()):

        global collectionURL, RegexCollectionPID, CollectionResourceXPath

        regex = re.compile(RegexCollectionPID)
        
        self.id = regex.findall(pid)[0]

        self.url = collectionURL.replace("$PID", self.id)


        if folder[-1] != "/" :
            folder = folder+"/"

        if os.path.isdir(folder) == False :
            os.mkdir(folder)
        
        self.folder = folder
        
        self.resources = resources

        self.name = None


    def getUpdates(self):
        #get list from url
        try:
            xml = getURL(user, self.url)

        except HTTPError, e:
          print "Collection Not Found!"
          sys.exit(0)
  
        xmlStr = ' '.join(xml.split())
        eleTree = ElementTree()

        tree = eleTree.parse(StringIO.StringIO(xmlStr))

        nameList = tree.findall("collection/header/title")

        if len(nameList) > 0:
          self.name = nameList[0].text

        resourceList = tree.findall(CollectionResourceXPath)

        for element in resourceList:
          resource = element.text
          regexID = re.compile("\d+$")

          resid = regexID.findall(resource)[0]

          if self.resources.has_key(resid) == False :
            regexPID = re.compile("\w+:\d+")
            rePID = regexPID.findall(resource)
            rePID = rePID[len(rePID)-1]
            self.resources[resid] = Resource(rePID, self.folder)

        savePickle()


    def getResources(self):
        #for each resource in dictionary 
        for k,v in self.resources.items():
            #if resource.checkForUpdate() == true
            if v.checkForUpdate():
                #getResource
                v.getResource()


#
# Get URL
#
#

def getURL(user, url):
    
    theurl = url
    username = user.username
    password = user.password
    # a great password
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, theurl, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `theurl` is a super-url
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
  
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)

    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
    #print "theurl", theurl
    pagehandle = urllib2.urlopen(theurl)
    # authentication is now handled automatically for us

    return pagehandle.read()

#
# POST to URL
#
#

def postToURL(user, url, content):

    username = user.username
    password = user.password
    # a great password
    
    #csantos code
    import socket
    # timeout in seconds
    timeout = 20
    socket.setdefaulttimeout(timeout)
    #end of csantos code

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, url, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which `url` is a super-url

    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler

    opener = urllib2.build_opener(authhandler)

    urllib2.install_opener(opener)


    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.

    
    #csantos code
    result = ""
    print "csantos: url: " + url + "\ncontent: "+content
    try:
      request = urllib2.Request(url, content)
      pagehandle = urllib2.urlopen(request)
    except HTTPError, e:
      result = result + 'The server couldn\'t fulfill the request.\n'
      result = result + 'Error code: ' + str(e.code) + '\n'
    except URLError, e:
      result = result + 'We failed to reach a server.\n'
      result = result + 'Reason: ', str(e.reason) + '\n'
    else: 
      print "Everything went better than expected"
      result = pagehandle.read()
    #end csantos code
    #previous code
    ##request = urllib2.Request(url, content)
    ##pagehandle = urllib2.urlopen(request)
    ##print pagehandle.read()
    ##return pagehandle.read()
    #end of previous code

    # authentication is now handled automatically for us
    return result

#Upload
def upload(FILE, collection, metadataPath, uploadURL):
    print "Entrei no upload"
    data = None

    if FILE != "" :

      dataFile = FILE

      #Open datafile
      dataContent = open(dataFile, "r")

      #create data -> content in base 64
      data = base64.encodestring(dataContent.read())

    else:

      data = ""
     
    collectionPID = collection

    #open EM metadata
    etree = ElementTree()

    emXML = etree.parse(metadataPath)

    #add the data to the description of the metadata
    ns = emXML.getiterator()[0].tag[1:].split("}", 1)[0]
    
    
    #COMMENTED - THIS REPLACED THE EXISTING DESCRIPTION. RESOLVED UNDER IT
    #emDesc = emXML.findall("{"+ns+"}generalDescription/{"+ns+"}description")[0]
    #emDesc.text = data

    # set this description as the base64 for the datastream
    #emDesc.set("base64", "true")

    newMetadata = xml.etree.ElementTree.tostring(emXML)
    newMetadata = newMetadata.replace("ns0", "em")

    em = xml.dom.minidom.parseString(newMetadata)


    if data != "":
      emTop = em.documentElement

      emGD = em.createElement("em:generalDescription")
    
      emDesc = em.createElement("em:description")
      emDesc.setAttribute("base64", "true")

      emDescText = em.createTextNode(data)
      emDesc.appendChild(emDescText)

      emGD.appendChild(emDesc)

      emTop.appendChild(emGD)
    
    

    #create RSS
    imp = xml.dom.minidom.getDOMImplementation()
    doc = imp.createDocument("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdf:RDF", None)
    #Add the Namespaces
    top_element = doc.documentElement
    top_element.setAttribute("xmlns:rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")  
    top_element.setAttribute("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    top_element.setAttribute("xmlns:dcterms", "http://purl.org/dc/terms/")
    top_element.setAttribute("xmlns:ore", "http://www.openarchives.org/ore/terms/")
    top_element.setAttribute("xmlns:foaf", "http://xmlns.com/foaf/0.1/")
    top_element.setAttribute("xmlns:em", "http://epiwork.di.fc.ul.pt/metadata/")
    #Description of the Aggregation
    #<!--About the Resource Map (this RDF/XML document) that describes the Aggregation -->
    desc = doc.createElement("rdf:Description")
    desc.setAttribute("rdf:about", "file://uploadRDF.xml")
    top_element.appendChild(desc)

    typeElement = doc.createElement("rdf:type")
    typeElement.setAttribute("rdf:resource", "http://www.openarchives.org/ore/terms/ResourceMap")
    desc.appendChild(typeElement)

    describes = doc.createElement("ore:describes")
    describes.setAttribute("rdf:resource", collectionPID)
    desc.appendChild(describes)

    #This would be used for DC metadata
    #describes2 = doc.createElement("ore:describes")
    #describes2.setAttribute("rdf:resource", collectionPID)
    #desc.appendChild(describes2)

    creator = doc.createElement("dcterms:creator")
    creator.appendChild(doc.createTextNode("Simple EM Client"))
    desc.appendChild(creator)

    created = doc.createElement("dcterms:created")
    created.setAttribute("rdf:datatype", "http://www.w3.org/2001/XMLSchema#dateTime")
    created.appendChild(doc.createTextNode(time.strftime("%Y-%m-%dT%H:%M:%SZ")))
    desc.appendChild(created)

    #Description of the Resource with EM metadata
    description = doc.createElement("rdf:Description")
    description.setAttribute("rdf:about", collectionPID)
    top_element.appendChild(description)

    resType = doc.createElement("rdf:type")
    resType.setAttribute("rdf:resource", "http://www.openarchives.org/ore/terms/Aggregation")
    description.appendChild(resType)

    description.appendChild(em.documentElement)

    xmlData = doc.toxml()

    #print xmlData

    upload = postToURL(user, uploadURL, xmlData)
    print "csantos: depois do upload"
    print "upload result:\n" + upload
    return True


# pickle
def savePickle():
    global collections
    global resources
    #creates pickles of session objects
    FILE1 = open(os.path.join(os.getcwd(), user.username+"Collections.data"), "w")
    pickle.dump(collections, FILE1)
    FILE1.close()
    
    FILE2 = open(os.path.join(os.getcwd(), user.username+"Resources.data"), "w")
    pickle.dump(resources, FILE2)
    FILE2.close()

def loadPickle():
    global collections
    global resources
    #opens pickles of session objects
    if os.path.isfile(os.path.join(os.getcwd(), user.username+"Collections.data")):
        FILE1 = open(os.path.join(os.getcwd(), user.username+"Collections.data"), "r")
        collections = pickle.load(FILE1)
        FILE1.close()


    if os.path.isfile(os.path.join(os.getcwd(), user.username+"Resources.data")):    
        FILE2 = open(os.path.join(os.getcwd(), user.username+"Resources.data"), "r")
        resources = pickle.load(FILE2)
        FILE2.close()


#tables

def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""

    try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)




def get_max_width(table, index):
    """Get the maximum width of the given column index"""

    return max([len(format_num(row[index])) for row in table])




def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """

    col_paddings = []

    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out



#login
class Run:


    def __init__(self):

        global resourceURL, collectionURL, RegexResourcePID, RegexCollectionPID, CollectionResourceXPath, loginURL, uploadURL

        parser = OptionParser()
        parser.add_option("-U", "--username", dest="username",
                  help="Your Epidemic Marketplace username. If this is not given you will be prompted.")

        parser.add_option("-p", "--password", dest="password", help="Your Epidemic Marketplace password. If this is not given you will be prompted.")

        parser.add_option("-g", "--get-resource",
                  action="store_true", dest="getResource", default=False,
                  help="Get a resource from the Epidemic Marketplace. Syntax \"-g \"resourcePID\" \"folderPath\"\"")

        #parser.add_option("-a", "--add-resource",
        #          action="store_true", dest="addResource", default=False,
        #          help="Add a resource to the monitored resource list. Syntax \"-a \"resourcePID\" \"folderPath\"\"")

        #parser.add_option("-A", "--add-collection",
        #          action="store_true", dest="addCollection", default=False,
        #          help="Add a resource to the monitored resource list. Syntax \"-A \"collectionPID\" \"folderPath\"\"")

        #parser.add_option("-l", "--list-resources",
        #          action="store_true", dest="listResources", default=False,
        #          help="Lists all the currently monitored resources")

        #parser.add_option("-L", "--list-collections",
        #          action="store_true", dest="listCollections", default=False,
        #          help="Lists all the currently monitored collections")

        #parser.add_option("-r", "--remove-resource",
        #          action="store_true", dest="removeResource", default=False,
        #          help="Remove a resource from the monitored resource list. Syntax \"-r resourceID\"")

        #parser.add_option("-R", "--remove-collection",
        #          action="store_true", dest="removeCollection", default=False,
        #          help="Remove a collection from the monitored collection list. Syntax \"-R collectionID\"")

        parser.add_option("-u", "--upload",
                  action="store_true", dest="upload", default=False,
                  help="Submits a resource to the EM respository. Syntax \"-u \"filepath\" \"collectionName\" \"filepathToEMMetadata\"\"")

        #parser.add_option("-d", "--download-updates",
        #          action="store_true", dest="downloadUpdates", default=False,
        #          help="Downloads updates to the resources and collections in the monitored lists.")


        parser.add_option("-i", "--interactive",
                  action="store_true", dest="interactive", default=False,
                  help="Simple EM Client interactive mode. Use the client through a menu interface.")

        parser.add_option("-V", "--upload-URL",
              dest="uploadURL", default="http://api.epimarketplace.net/upload", help="URL for the upload web service. Default value: \"http://api.epimarketplace.net/upload\" .")

        parser.add_option("-z", "--resource-url",
                           dest="resourceURL", default="http://api.epimarketplace.net/fetch/pid/$PID", help="The URL used in fetching the resource, $PID is replaced by the resource PID. Default value: \"http://api.epimarketplace.net/fetch/pid/$PID\" .")

        #parser.add_option("-Z", "--collection-url",
        #      dest="collectionURL", default="http://api.epimarketplace.net/list/repositorytree/pid/$PID/level/2", help="The URL used in a collection's resource list, $PID is replaced by the collection PID. Default value: \"http://api.epimarketplace.net/list/repositorytree/pid/$PID/level/2\" .")

        parser.add_option("-n", "--resource-PID-Regex",
              dest="resourcePIDRegex", default=".*", help="The regex for the part of the PID that is used in the resource URL. Default expression: \" .* \"")

        #parser.add_option("-N", "--collection-PID-Regex",
        #      dest="collectionPIDRegex", default=".*", help="The regex for the part of the PID that is used in the collection URL. Default expression: \" .* \"")

        #parser.add_option("-x", "--resource-Xpath",
        #      dest="resourceXpath", default="collection/content/resource/header/download", help="Xpath expression for elements containing the resource PID in a collection's resource list. Default value: \"collection/content/resource/header/download\"")

        parser.add_option("-v", "--login-URL",
              dest="loginURL", default="http://api.epimarketplace.net/list/datastreams/pid/empid:1", help="URL to test your credentials. If the request fails, login fails. If the request succeeds your credentials will be used for the remaining requests.")
              #v1: "https://epiwork.di.fc.ul.pt/Mediator/resources/search/objects/identifier/ThisDoesNotExist"

        (options, args) = parser.parse_args()

        resourceURL = options.resourceURL
        #collectionURL = options.collectionURL
        RegexResourcePID = options.resourcePIDRegex
        #RegexCollectionPID = options.collectionPIDRegex
        #CollectionResourceXPath = options.resourceXpath
        loginURL = options.loginURL
        uploadURL = options.uploadURL


        self.username = None
        self.password = None


        if (options.getResource == True):
            if (len(args) != 2):
                print "-g requires 2 parameters. Syntax \"-a resourcePID folderPath\""
            else:
                if(options.username != None):
                    self.username = options.username

                else:
                    #ask for username:
                    self.username = raw_input("Username: ")


                if (options.password != None):
                    #ask for password
                    self.password = options.password

                else:
                    #ask for password:
                    self.password = getpass.getpass()

                #run login:
                self.login()
                getResource(False, args[0], args[1])

        #elif (options.addResource == True):
        elif False:
            if (len(args) != 2):
              print "-a requires 2 parameters. Syntax \"-a resourcePID folderPath\""
            else:
              if(options.username != None):
                self.username = options.username

              else:
                #ask for username:
                self.username = raw_input("Username: ")

              if (options.password != None):
                #ask for password
                self.password = options.password
              else:
                #ask for password:
                self.password = getpass.getpass()

              #run login:
              self.login()
              addResource(False, args[0], args[1])

        elif False:
        #elif (options.addCollection == True):
            if (len(args) != 2):
                print "-A requires 2 parameters. Syntax \"-A collectionPID folderPath\""
            else:
                if(options.username != None):
                    self.username = options.username

                else:
                    #ask for username:
                    self.username = raw_input("Username: ")


                if (options.password != None):
                    #ask for password
                    self.password = options.password

                else:
                    #ask for password:
                    self.password = getpass.getpass()

                #run login:
                self.login()
                addCollection(False, args[0], args[1])

        elif False:
        #elif (options.listResources == True):
            if(options.username != None):
                self.username = options.username

            else:
                #ask for username:
                self.username = raw_input("Username: ")


            if (options.password != None):
                #ask for password
                self.password = options.password

            else:
                #ask for password:
                self.password = getpass.getpass()

            #run login:
            self.login()
            showResources(False)

        elif False:
        #elif (options.listCollections == True):
            if(options.username != None):
                self.username = options.username

            else:
                #ask for username:
                self.username = raw_input("Username: ")


            if (options.password != None):
                #ask for password
                self.password = options.password

            else:
                #ask for password:
                self.password = getpass.getpass()

            #run login:
            self.login()
            showCollections(False)

        elif False:
        #elif (options.removeResource == True):
            if (len(args) != 1):
                print "-r requires 1 parameter. Syntax \"-r resourceID\""
            else:
                if(options.username != None):
                    self.username = options.username

                else:
                    #ask for username:
                    self.username = raw_input("Username: ")


                if (options.password != None):
                    #ask for password
                    self.password = options.password

                else:
                    #ask for password:
                    self.password = getpass.getpass()

                #run login:
                self.login()
                deleteResource(False, args[0])

        elif False:
        #elif (options.removeCollection == True):
            if (len(args) != 1):
                print "-R requires 1 parameter. Syntax \"-R collectionID\""
            else:
                if(options.username != None):
                    self.username = options.username

                else:
                    #ask for username:
                    self.username = raw_input("Username: ")


                if (options.password != None):
                    #ask for password
                    self.password = options.password

                else:
                    #ask for password:
                    self.password = getpass.getpass()

                #run login:
                self.login()
                deleteCollection(False, args[0])

        elif (options.upload == True):
            if (len(args) != 3):
                print "-u requires 3 parameters. Syntax \"-u filepath collectionName filepathToEMMetadata\""
            else:
                if(options.username != None):
                    self.username = options.username

                else:
                    #ask for username:
                    self.username = raw_input("Username: ")


                if (options.password != None):
                    #ask for password
                    self.password = options.password

                else:
                    #ask for password:
                    self.password = getpass.getpass()

                
                #run login:
                self.login()
                print "uploading in progress..."
                uploadResource(False, args[0], args[1], args[2])

        elif False:
        #elif (options.downloadUpdates == True):
            if(options.username != None):
                self.username = options.username

            else:
                #ask for username:
                self.username = raw_input("Username: ")


            if (options.password != None):
                #ask for password
                self.password = options.password

            else:
                #ask for password:
                self.password = getpass.getpass()

            #run login:
            self.login()
            downloadUpdates(False)
        elif (options.interactive == True):
            if(options.username != None):
                self.username = options.username

            else:
                #ask for username:
                self.username = raw_input("Username: ")


            if (options.password != None):
                #ask for password
                self.password = options.password

            else:
                #ask for password:
                self.password = getpass.getpass()

            #run login:
            self.login()
            Menu()
        else :
            print "Usage: .\\SimpleEMClient.py [-U username] [-p password] {-g|-a|-A|-l|-L|-r|-R|-u|-d|-i|-h|-z|-Z|-n|-N|-x|-v} [additional parameters] \n\n For more information on the available options: \"SimpleEMClient.py -h\".\n To run interactively: \"SimpleEmClient.py -i\""


    def login(self):
        #create user
        global user, loginURL
        user = User(self.username, self.password)

        loggedIn = False

        #verifying login
        #make a call to https://epiwork.di.fc.ul.pt/Mediator/resources/search/objects/identifier/ThisDoesNotExist
        try :
            dl = getURL(user, loginURL)

            dom = xml.dom.minidom.parseString(dl)
                
        except HTTPError, e:
          print "Unsuccessful auth!"
          if e.code != 200:
            print "HTTP response code: ", e.code
          sys.exit(0)

        loadPickle()
        print "Login successfull. Welcome "+user.username+"\n"



#present user with a list of options (1. show resources, 2. show collections, 3. add resource, 4. delete resource, 5.add collection, 6. delete collection, 7. Download Updates, 8. Upload)
class Menu:
    def __init__(self):
        loadPickle()

        print   """Menu:\ng. Get Resource\nl. Show Resource List\nL. Show Collection List\na. Add Resource\nA. Add Collection\nr. Remove Resource\nR. Remove Collection\nd. Download Updates\nu. Upload Resource\n"""
            
        choice = raw_input("Pick an option (\"e\" or \"q\" to leave): ")

        if choice =="g":
            getResource()
        elif choice == "l":
            showResources()
        elif choice == "L":
            showCollections()
        elif choice == "a":
            addResource()
        elif choice == "r":
            deleteResource()
        elif choice == "A":
            addCollection()
        elif choice == "R":
            deleteCollection()
        elif choice == "d":
            downloadUpdates()
        elif choice == "u":
            uploadResource()
        elif choice == "e" or choice=="q":
            exit()
        else :
            print "Unknown option. \n"
            Menu()

#if 1, print resources (id - name - URL - Folder)
class showResources:
   def __init__(self, menu = True):

    print "Resource List: \n"

    if len(resources) == 0:
        print "Empty.\n"
    else :
    
        rList = list()
        rList.append(["Id", "Name", "URL", "Folder"])
        
        for k,v in resources.items():
            rList.append([k, v.name, v.url, v.folder])

        pprint_table(out, rList)
    if (menu == True):
        Menu()


#if 2, print collection (id - name - URL - Folder)
class showCollections:
   def __init__(self, menu = True):

    print "Collection List: \n"

    if len(collections) == 0:
        print "Empty.\n"
    else :

        cList = list()

        cList.append(["Id", "Name", "URL", "Folder"])

        for k,v in collections.items():
            cList.append([k, v.name, v.url, v.folder])

        pprint_table(out, cList)
    if (menu == True):
        Menu()

#if 3 request URL and Folder, add the resource and download? (write cancel to cancel this action)
class addResource:
   def __init__(self, menu = True, resourcePID = None, folderPath = None):

    if (menu == True):
      print "To add a resource to the resource list provide the following data.\n"

      pid = raw_input("Resource PID (default example value: \"empid:227\"): ")

      if pid == "":
         pid = "empid:227"

      folder = raw_input("Folder path where to store the resource (default value: "+ os.getcwd() +" ): ")

      if folder == "":
         folder = os.getcwd()
            
      regex = re.compile("\d+$")
        
      resid = regex.findall(pid)[0]

      resources[resid] = Resource(pid, folder)

      print "Added resource "+resid+"\n"

      savePickle()

      Menu()

    else :
      pid = resourcePID

      folder = folderPath
            
      regex = re.compile("\d+$")
        
      resid = regex.findall(pid)[0]

      resources[resid] = Resource(pid, folder)

      print "Added resource "+resid+"\n"

      savePickle()

#if "g" request PID and Folder, and download the resource
class getResource:
   def __init__(self, menu = True, resourcePID = None, folderPath = None):

    if (menu == True):
      print "To get a resource provide the following data.\n"

      pid = raw_input("Resource PID (default example value: \"changeme:371\"): ")

      if pid == "":
         pid = "changeme:371"

      folder = raw_input("Folder path where to store the resource (default value: "+ os.getcwd() +" ): ")

      if folder == "":
         folder = os.getcwd()
            
      regex = re.compile("\d+$")
        
      resid = regex.findall(pid)[0]

      resource = Resource(pid, folder)

      print "Getting Resource "+resid+"..."

      resource.getResource()

      print "Done.\n"

      savePickle()

      Menu()

    else :
      pid = resourcePID

      folder = folderPath
            
      regex = re.compile("\d+$")
        
      resid = regex.findall(pid)[0]

      resource = Resource(pid, folder)

      print "Getting Resource "+resid+"..."

      resource.getResource()

      print "Done.\n"

      savePickle()


#if 4 request resource ID and delete the resource from the list (warn the user this will not remove the files from your hard drive)

class deleteResource:
   def __init__(self, menu = True, resourceID = None):
    if(menu == True):
        resid = raw_input("To remove a resource provide its Id (view Resource List): ")
        del resources[resid]
        print "Removed Resource "+resid+"\n"
        savePickle()
        Menu()
    else:
        resid = resourceID
        del resources[resid]
        print "Removed Resource "+resid+"\n"
        savePickle()

#if 5 request URL and Folder
class addCollection:
    def __init__(self, menu = True, collectionPID = None, folderPath = None):

        if(menu == True):
            print "To add a collection to the collection list provide the following data. \n"

            pid = raw_input("Collection PID (default example value: \"changeme:329\"): ")

            if pid == "":
               pid = "changeme:329"

            folder = raw_input("Folder path where to store the collection resources (default value: "+ os.getcwd() +" ): ")

            if folder == "":
               folder = os.getcwd()
        
            regex = re.compile("\d+$")
        
            collectionId = regex.findall(pid)[0]
            
            collections[collectionId] = Collection(pid, folder)
            
            print "Added collection "+collectionId+"\n"

            savePickle()

            Menu()

        else:

            pid = collectionPID

            folder = folderPath
            
            regex = re.compile("\d+$")
        
            collectionId = regex.findall(pid)[0]
            
            collections[collectionId] = Collection(pid, folder)
            
            print "Added collection "+collectionId+"\n"

            savePickle()


#if 6 request collection ID and remove collection from the list  (warn the user this will not remove the files from your hard drive)
class deleteCollection:
   def __init__(self, menu = True, collectionID = None):
    if(menu == True):
     colid = raw_input("To remove a collection provide its Id (view collection List): ")
     del collections[colid]
     print "Removed Collection "+colid+"\n"
     savePickle()
     Menu()
    else:
     colid = collectionID
     del collections[colid]
     print "Removed Collection "+colid+"\n"
     savePickle()


#if 7 For each collection, check for updates and download and For each Resource check for updates and download!
class downloadUpdates:
    def __init__(self, menu = True):
     if(menu == True):
        print "Downloading Updates. Please wait, this could take a few minutes... "

        for k,v in resources.items():
                if v.checkForUpdate():
                    v.getResource()

        savePickle()


        print "Resources Updated. \n Updating Collections..."
        for k,v in collections.items():
            v.getUpdates()
            v.getResources()
                
        savePickle()
        print "Done.\n"
        Menu()
     else:
        print "Downloading Updates. Please wait, this could take a few minutes... \n"

        for k,v in resources.items():
                if v.checkForUpdate():
                    v.getResource()

        savePickle()

        print "Resources Updated.\n Updating Collections..."
        for k,v in collections.items():
            v.getUpdates()
            v.getResources()
                
        savePickle()
        print "Done.\n"

#if 8 Ask for Filepath, CollectionName, Title, Identifier, Publisher and Upload.
class uploadResource:
    def __init__(self, menu = True, filePath = None, collectionName = None, metadataPath = None):

      global uploadURL

      if (menu == True):
        print "To upload a resource to the Epidemic Marketplace provide the following data: \n"

        filepath = raw_input("Filepath: ")
        collection = raw_input("Collection Name: ")
        metadataPath = raw_input("EM Metadata Path: ")

        print "Uploading..."

        uploading = upload(filepath, collection, metadataPath, uploadURL)

        print "Done.\n"

        Menu()
      else:
        filepath = filePath
        collection = collectionName

        print "Uploading..."

        uploading = upload(filepath, collection, metadataPath, uploadURL)

        print "Done.\n"



#print welcome to EM Client
print "Welcome to the Simple EM Client.\n"

#Run
Run()
