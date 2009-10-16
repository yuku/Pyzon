# coding:utf8 -*-
import urllib2
import time
import hashlib, hmac
import base64
from xml.dom import minidom

class AmazonException(Exception):
    """Base class for all Amazon exceptions"""
    pass

class NoAccessKeyID(AmazonException): pass
class NoSecretAccessKey(AmazonException): pass
class BadLocale(AmazonException): pass

__supportedLocales = {
    'JP': 'ecs.amazonaws.jp',
    'US': 'ecs.amazonaws.com',
    'UK': 'ecs.amazonaws.co.uk',
    'DE': 'ecs.amazonaws.de',
    'FR': 'ecs.amazonaws.fr',
    'CA': 'ecs.amazonaws.cs',
} 

class Pyzon:
    # An Amazon Access Key ID used when quering Amazon servers
    _access_key_id = None
    # An Amazon Secret Acceess Key used when querying Amazon servers
    _secret_access_key = None
    # An Amazon Associate Tag used in the URL's so  a commision may be payed
    _associate_tag = None
    # A base URL used to build the query for the Amazon servers
    _urlhost = 'ecs.amazonaws.jp'
    # A service version
    _version = '2009-03-31'
    # The time that the Amazon took to process the request
    _processing_time = None
    # The raw result returned from the request
    _raw_result = None
    # Proxy server
    _proxy_host = None
    # Proxy port
    _proxy_port = None
    
    def __init__(self, access_key_id, secret_access_key, associate_tag=None):
        """Constructor
        """
        self.setAccessKeyID(access_key_id)
        self.setSecretAccessKey(secret_access_key)
        self.setAssociateTag(associate_tag)

    def getApiVersion(self):
        """Retrieves the current version of this classes API
        """
        return '0.0.1'

    def setAccessKeyID(self, access_key_id):
        """Sets an Access Key ID 
        """
        self._access_key_id = access_key_id

    def getAccessKeyID(self):
        """Gets an Access Key ID
        """
        if not self._access_key_id:
            raise NoAccessKeyID, ("Please get the license key from http://aws.amazon.com/")
        return self._access_key_id

    def setSecretAccessKey(self, secret_access_key):
        """Sets a Secret Access Key
        """
        self._secret_access_key = secret_access_key

    def getSecretAccessKey(self):
        """Gets a Secret Access Key
        """
        if not self._secret_access_key:
            raise NoSecretAccessKey
        return self._secret_accesskey

    def setAssociateTag(self, associate_tag):
        """Sets an Associate Tag
        """
        self._associate_tag = associate_tag

    def setAssociateID(self, associd):
        """Sets an Associate ID
        """
        self.setAssociateTag(associd)

    def setUrlHost(self, url_host):
        """Sets the URL's host
        """
        self._urlhost = url_host

    def setLocale(self, locale):
        """Sets the locale passed when making a query to Amazon
            Currently JP, US, UK, DE, FR, and CA are supported
            If unsupported locale is set, BadLocale is raised.
        """
        locale = locale.upper()
        if not locale in __supportedLocales:
            raise BadLocale, ("Unsupported locale. Locale must be one of: %s" % ', '.join([x for x in __supportedLocales.keys()])) 
        self.setUrlHost(__supportedLocales[locale])
        return True

    def setVersion(self, version):
        """Sets a version
        """
        self._version = version

    def setProxy(self, host, port=8080):
        """Sets a proxy
        """
        self._proxy_host = host
        self._proxy_port = port

    def BrowseNodeLookup(self, browsenode_id, **options):
        """Retrieves information about a browse node
        """
        params = options
        params['Operation'] = 'BrowseNodeLookup'
        params['BrowseNodeId'] = browsenode_id
        return self._sendRequest(params)

    def CartAdd(self, cart_id, hmac, item, **options):
        """Adds items to an existing remote shopping cart
        """
        params = options
        params['Operation'] = 'CartAdd'
        params['CartId'] = cart_id
        params['HMAC'] = hmac
        params.append(self._assembleItemParameter(item))
        return self._sendRequest(params)

    def CartClear(self, cart_id, hmac, **options):
        """Removes all the contents of a remote shopping cart
        """
        params = options
        params['Operation'] = 'CartClear'
        params['CartId'] = cart_id
        params['HMAC'] = hmac
        return self._sendRequest(params)

    def CartCreate(self, item, **options):
        """Creates a new remote shopping cart
        """
        params = options
        params['Operation'] = 'CartCreate'
        params.append(self._assembleItemParameter(item))
        return self._sendRequest(params)

    def CartGet(self, cart_id, hmac, **options):
        """Retrieves the contents of a remote shoping cart
        """
        params = options
        params['Operation'] = 'CartGet'
        params['CartId'] = cart_id
        params['HMAC'] = hmac
        return self._sendRequest(params)

    def CartModify(self, cart_id, hmac, item, **options):
        """Modifies the quantity of items in a cart and changes cart items to saved items
        """
        params = options
        params['Operation'] = 'CartModify'
        params['CartId'] = cart_id
        params['HMAC'] = hmac
        params.append(self._assembleItemParameter(item))
        return self._sendRequest(params)

    def CustomerContentLookup(self, customer_id, **options):
        """Retrieves publicly available content written by specific Amazon customers
        """
        params = options
        params['Operation'] = 'CustomerContentLookup'
        params['CustomerId'] = customer_id
        return self._sendRequest(params)

    def CustomerContentSearch(self, customer = None, **options):
        """Searches for Amazon customers by name or email address
        """
        params = options
        params['Operation'] = 'CustomerContentSearch'
        params.append(customer)
        return self._sendRequest(params)

    def Help(self, help_type, about, **options): 
        """Retrieves information about operations and response groups
        """
        params = options
        params['Operation'] = 'Help'
        params['HelpType'] = help_type
        params['About'] = about
        return self._sendRequest(params)

    def ItemLookup(self, item_id, **options):
        """Retrieves information for products
        """
        params = options
        params['Operation'] = 'ItemLookup'
        params['ItemId'] = item_id
        return self._sendRequest(params)

    def ItemSearch(self, search_index, **options):
        """Searches for products
        Each locale supports only a subset of all search index values.
        For example, JP locale supports below
              Apparel,Baby,Beauty,Blended,Books,Classical,DVD,Electronics,ForeignBooks,Grocery,HelthPersonalCare,Hobbies,Jewelry,Kitchen,Music,MusicTracks,Software
        """
        params = options
        params['Operation'] = 'ItemSearch'
        params['SearchIndex'] = search_index
        return self._sendRequest(params)

    def ListLookup(self, list_type, list_id, **options):
        """Retrieves products in a specific list
        """
        params = options
        params['Operation'] = 'ListLookup'
        params['ListType'] = list_type
        params['ListId'] = list_id
        return self._sendRequest(params)

    def ListSearch(self, list_type, keywords, **options):
        """Searches for wish list, baby registry, or wedding registry
        """
        params = options
        params['Operation'] = 'ListSearch'
        params['ListType'] = list_type
        params.append(keywords)
        return self._sendRequest(params)

    def SellerListingLookup(self, id_type, id, **options):
       """Retrieves information about Amazon zShops and Marketplace products
       """
       params = options
       params['Operation'] = 'SellerListingLookup'
       params['IdType'] = id_type
       params['Id'] = id
       return self._sendRequest(params)

    def SellerListingSearch(self, search_index, **options):
        """Searchs for Amazon zShops and Marketplace products
        """
        params = options
        params['Operation'] = 'SellerListingSearch'
        params['SearchIndex'] = search_index
        return self._sendRequest(params)

    def SellerLookup(self, seller_id, **options):
        """Retrieves information about specific sellers
        """
        params = options
        params['Operation'] = 'SellerLookup'
        params['SellerId'] = seller_id
        return self._sendRequest(params)

    def SimilarityLookup(self, item_id, **options):
        """Retrieves products that are similar to Amazon products
        """
        params = options
        params['Operation'] = 'SimilarityLookup'
        if type(item_id) is str:
            params['ItemId'] = item_id
        else:
            params['ItemId'] = ','.join(item_id)
        return self._sendRequest(parmas)

    def TagLookup(self, tag_name, **options):
        """Retrieves information about tags
        """
        params = options
        params['Operation'] = 'TagLookup'
        if type(tag_name) is str:
            params['TagName'] = tag_name
        else:
            params['TagName'] = ','.tag_name
        return self._sendReques(params)

    def TransactionLookup(self, transaction_id, **options):
        """Retrieves information about the status of financial transactions
        """
        params = options
        params['Operation'] = 'TransactionLookup'
        params['TransactionId'] = transaction_id
        return self._sendRequest(params)


    def VehiclePartLookup(self, **options):
        """Retrieves information about a car part
        """
        params = options
        parms['Operation'] = 'VehiclePartLookup'
        return self._sendRequest(params)

    def VehiclePartSearch(self, make_id, model_id, year, **options):
        """Searches the parts that work in the car
        """
        params = options
        params['Operation'] = 'VehiclePartSearch'
        params['MakeId'] = make_id
        params['ModelId'] = mnodel_id
        parmas['Year'] = year
        return self._sendRequest(params)

    def VehicleSearch(self, **options):
        """Searches all vehicles
        """
        params = options
        params['Operation'] = 'VehicleSearch'
        return self._sendRequest(params)

    def _assembleItemParameter(self, items):
        """Assembles the Item parameters
        """
        params = {}
        if type(items) is not list:
            items = [items]
        i = 1
        for item in items:
            for k in item.keys():
                params['Item.'+i+'.'+k] = item[k]
            i += 1
        return params

    def _buildUrl(self, params):
        """Builds a URL
        """
        params['Service'] = 'AWSECommerceSerivce'
        params['AWSAccessKeyId'] = self.getAccessKeyID()
        if self._associate_tag is not None:
            params['AssociateTag'] = self._associate_tag

        params['Version'] = self._version
        params['Timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        sorted_params = sorted(params.items())
        req_list = []
        for p in sorted_params:
            pair = "%s=%s" % (p[0], urllib2.quote(str(p[1]).encode('utf-8')))
            req_list.append(pair)
        urlencoded_reqs = '&'.join(req_list)
        string_to_sign = "GET\n%s\n/onca/xml\n%s" % (self._urlhost, urlencoded_reqs)
        hmac_digest = hmac.new(self._secret_access_key, string_to_sign, hashlib.sha256).digest()
        base64_encoded = base64.b64encode(hmac_digest)
        signature = urllib2.quote(base64_encoded)
        url = "http://%s/onca/xml?%s&Signature=%s" % (self._urlhost, urlencoded_reqs, signature)
        return url

    def _sendHttpRequest(self, url):
        """Sends a request
        """
        if self._proxy_host:
            proxy_handler = urllib2.ProxyHandler({'http':'http://%s:%s/'%(self._proxy_host, self._proxy_port)})
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Pyzon/%s'%self.getApiVersion())]
        return opener.open(url).read()
    
    def _sendRequest(self, params):
        """Sends the request to Amazon
        """
        url = self._buildUrl(params)
        result = self._sendHttpRequest(url)
        return result 

