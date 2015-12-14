
@state = state = {
  tables: []
}

@initTables = (tables)->
  unless tables.length is 0 or (Array.isArray(tables[0]) and tables[0].length is 2)
    throw Error "Invalid tables"
  state.tables = tables
