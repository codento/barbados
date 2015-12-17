
{ replace } = require 'src/utils/dom.coffee!'
{ trans } = require 'src/utils/dict.coffee!'

table = require './table.coffee!'
{ singular } = require 'src/utils/dict.coffee!'
{ titelize } = require './../utils/misc.coffee!'

{ renderNewTable } = require 'src/uiRender.coffee!'

titleValues = ['name', 'username']
getTitle = (row, tableType)->
  for key in titleValues
    if row[key]
      return titelize(tableType) + ' - ' + row[key]
  throw Error "No valid title found in row", row


idFromRow = (row)-> row.url.match(/\/([^\/]+)\/$/)[1]

@valueCell = valueCell = (key, row, tableType)->
  value = row[key]
  '.wrapper':
    if Array.isArray(value)
      if value.length
        onClick: renderNewTable.bind null, getTitle(row, key), singular(key), tableType, idFromRow(row)
        span: trans('open') + ' ' + value.length
      else
        null
    else
      onClick: (ev)->
        wrapper = ev.currentTarget
        td = wrapper.parentElement
        replace wrapper, editCell(key, row)
        td.querySelector('input').select()
      span: value
      'I .edit-icon .fa .fa-pencil-square-o': ''

# edit cell could be in its own module (especially once it's functional)
@editCell = editCell = (key, row)->
  value = row[key]
  '.wrapper': (wrapperEl)->
    input: (inputEl)->
      value: value
      onBlur: ->
        wrapperEl.parentElement.setAttribute 'sortBy', inputEl.value
        replace wrapperEl, valueCell(key, row)
      onKeyDown: (ev)->
        switch ev.keyCode
          when 13 then inputEl.blur()
