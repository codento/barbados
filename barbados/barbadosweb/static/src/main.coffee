# general requires
require './styles/root.coffee!'
require 'tableSort'

# main module requires (to be moved to own file)
{ createNode } = require 'jsonHtml'
{ tables, hierarchic } = require './dummyData.coffee!' #
{ titelize } = require './utils/string.coffee!'
$ = require 'jquery'

document.body.appendChild createNode div: [
  for tableName, tableVals of tables
    Section:
      h2: titelize tableName
      '.tableWrapper':
        'table.tableSorter':
          'Thead':
            tr:
              for key of tableVals[0]
                th:
                  #'data-sortBy': key
                  text: titelize key

          'Tbody': for row in tableVals
            tr:
              for key, val of row
                td:
                  'span': val
                  'I .fa .fa-pencil-square-o': ''
  # section:
  #   h2: 'Relation hierarchy proto'
  #   '.hierarchic': inspect_object hierarchic
]

$('.tableSorter').tableSort sortBy: key
