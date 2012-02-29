Python + Amazon = Pyzon
=======================

This is a Python module which let you use Amazon Product Advertising API.

How to use
----------

Import **Pyzon** from *pyzon.py* and put Access Key ID, Secret Access Key, and Associate Tag to the class object.::

  from pyzon import Pyzon

  access_key_id = '***'
  secret_access_key = '***'
  associate_tag = '***-22'

  pyzon = Pyzon(access_key_id, secret_access_key, associate_tag)
  pyzon.setLocale('JP') # JP, US, UK, DE, FR, CA

The instance of **Pyzon** has some methods to access Product Advertising API. Each method accesses to corresponding API and returns the response XML as string object.

* BrowsNodeLookup
* CartAdd
* CartClear
* CartCreate
* CartGet
* CartModify
* CustomerContentLookup
* CustomerContentSearch
* Help
* ItemLookup
* ItemSearch
* ListLookup
* ListSearch
* SellerListingLookup
* SellerListingSearch
* SellerLookup
* SimilarityLookup
* TagLookup
* TransactionLookup
* VehiclePartLookup
* VehiclePartSearch
* VehicleSearch

Each method accepts arguments and required argument is represented in term_connected_with_underscore manner and optional arguments is same to original API. For example, speaking of *ItemSearch* API, *SearchIndex* is required by Amazon so it described as *search_index* and remaining optional parameters, such as *Keywords*, *ResponseGroup* etc. are not changed::

  xml = pyzon.ItemSearch(search_index='Books', Keywords=u'初めてのPython')

ItemLookup::

  xml = pyzon.ItemLookup(item_id=487311393938)

Licence
=======

MIT Licence
