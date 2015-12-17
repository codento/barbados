

# TODO: add polyfills!
#require 'core-js' # Promise etc. polyfills

$ = require 'jquery'

paths =
  "club": "/api/club/",
  "harbour": "/api/harbour/",
  "jetty": "/api/jetty/",
  "berth": "/api/berth/"
  "boat": "/api/boat/",
  "user": "/api/user/",

pathFromType = (type)->
  url = paths[type]
  throw Error "Invalid list type: #{type}" unless url
  url

@fetchList = fetchList = (type, filterKey, filterVal)->
  url = pathFromType(type)
  url += "?#{filterKey}=#{filterVal}" if filterKey
  $.get url

@fetchItem = (type, id)->
  $.get (pathFromType(type) + '/' + id) #, 'json'

# delete values that are not to be show in UI
# sanitizeKeys = ['url', 'club', 'harbour']
# @sanitizeItem = sanitizeItem = (item)->
#   for key in sanitizeKeys
#     delete item[key] if item[key]?
#   return

@getTableDataPromise = (type, filterKey, filterVal)->
  #debugger
  fetchList(type, filterKey, filterVal);
  # new Promise (resolve, reject)->
  #   fetchList(type,filterKey,filterVal).then((itemList)->
  #     for item in itemList
  #       sanitizeItem item
  #     console.log 'fetched list', itemList
  #     resolve(itemList);
  #   )
