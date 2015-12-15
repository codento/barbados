
{ replace } = require 'src/utils/dom.coffee!'
{ trans } = require 'src/utils/dict.coffee!'

# TODO: move elsewhere
{ createNode } = require 'jsonHtml'
{ sanitizeItem } = require 'src/utils/api.coffee!'

titleValues = ['name', 'username']
getTitle = (row)->
  for key in titleValues
    return row[key] if row[key]
  throw Error "No valid title found in row", row

openTable = (fromName, rows)->
  { renderTable } = require './table.coffee!'
  document.body.appendChild createNode renderTable fromName, rows



@valueCell = valueCell = (key, row, value=row[key])->
  '.wrapper':
    if Array.isArray(value)
      if value.length
        onClick: openTable.bind null, getTitle(row), value
        span: trans('open') + ' ' + value.length
      else
        null
    else
      onClick: (ev)->
        wrapper = ev.currentTarget
        td = wrapper.parentElement
        replace wrapper, editCell(value)
        td.querySelector('input').select()
      span: value
      'I .edit-icon .fa .fa-pencil-square-o': ''

@editCell = editCell = (value)->
  '.wrapper': (wrapperEl)->
    input: (inputEl)->
      value: value
      onBlur: ->
        wrapperEl.parentElement.setAttribute 'sortBy', inputEl.value
        replace wrapperEl, valueCell(null, null, inputEl.value)
      onKeyDown: (ev)->
        switch ev.keyCode
          when 13 then inputEl.blur()
