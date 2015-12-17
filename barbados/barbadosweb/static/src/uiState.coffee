
state = {
  tables: []
}

@addTable = (ind, name, type, filterKey, filterVal)->
  unless typeof ind is 'number' and name and type
    throw Error "Invalid table"
  # drop all tables afte this index
  state.tables.length = ind
  state.tables[ind] = { name, type, filterKey, filterVal }

# for debugging!
window.state = state
window.renderUI = @renderUI
# /for debugging
