# general requires
require './styles/root.coffee!'
require 'tableSort'

# init UI
{ addTable } = require './uiState.coffee!'
{ renderUI } = require './uiRender.coffee!'

rootTable = 'club'
addTable 0, (rootTable), rootTable
renderUI()
