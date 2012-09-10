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

The instance of **Pyzon** has some methods to access Product Advertising API.
Each method accesses to corresponding API and returns the response XML as string object.

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

Each API methods has several required and optional arguments.
Required arguments are represented in ``terms_connected_with_underscore`` manner, and the others are same to original API call.
For example, speaking of *ItemSearch* API, *SearchIndex* is required by Amazon so it described as *search_index* and remaining optional parameters, such as *Keywords* and *ResponseGroup* are *Keywords* and *ResponseGroup* respectively::

  xml = pyzon.ItemSearch(search_index='Books', Keywords=u'初めてのPython')

Speaking of *ItemLookup*, *ItemId* is mandatory::

  xml = pyzon.ItemLookup(item_id=487311393938)

Licence
=======

MIT Licence
