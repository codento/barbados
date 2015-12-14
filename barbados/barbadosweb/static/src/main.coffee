# general requires
require './styles/root.coffee!'
require 'tableSort'

# main module requires (to be moved to own file)
{ createNode } = require 'jsonHtml'
{ tables, hierarchic } = require './dummyData.coffee!' #

{ renderTable } = require './table/table.coffee!'


$ = require 'jquery'

document.body.appendChild createNode div: [
  for tableName, tableVals of tables
    Section: renderTable tableName, tableVals

  # section:
  #   h2: 'Relation hierarchy proto'
  #   '.hierarchic': inspect_object hierarchic
]
#setTimeout ->
$('.tableSorter').tableSort() # sortBy: key
#, 1000

require 'core-js'
console.log(Object.isObject({}))
