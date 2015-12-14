

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

getPath = (type)->
  url = paths[type]
  throw Error "Invalid list type: #{type}" unless url
  url

@getList = getList = (type)-> $.get getPath(type), 'json'
getItem = (type, id)-> $.get (getPath(type) + '/' + id), 'json'


# @getList('club').then (res)->
#   console.log(res)


@getTableData = (type)->
  new Promise (resolve, reject)->
    getList(type).then((itemList)->
      for item in itemList
        delete item.url
      console.log 'edited item list', itemList
      resolve(itemList);
    )
