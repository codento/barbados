# general requires
require './styles/root.coffee!'
require 'tableSort'

{ getTableData } = require './utils/api.coffee!'

# { tables, hierarchic } = require './dummyData.coffee!' #

{ state, initTables } = require './uiState.coffee!'

{ renderTable } = require './table/table.coffee!'
{ trans } = require './utils/dict.coffee!'
{ createNode } = require 'jsonHtml'
$ = require 'jquery'


renderUi = ->
  document.body.appendChild createNode div: [
    for [tableName, tableVals] in state.tables
      Section: renderTable tableName, tableVals
  ]
  $('.tableSorter').tableSort() # sortBy: key

rootTable = 'club'
getTableData(rootTable).then (tableRows)->
  initTables [ [trans(rootTable), tableRows] ]
  renderUi()
