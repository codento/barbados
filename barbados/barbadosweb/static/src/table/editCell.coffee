
{ replace } = require 'src/utils/dom.coffee!'
{ trans } = require 'src/utils/dict.coffee!'

@editCell = editCell = (value)->
  '.wrapper': (wrapperEl)->
    input: (inputEl)->
      value: value
      onBlur: ->
        wrapperEl.parentElement.setAttribute 'sortBy', inputEl.value
        replace wrapperEl, valueCell(inputEl.value)
      onKeyDown: (ev)->
        switch ev.keyCode
          when 13 then inputEl.blur()

@valueCell = valueCell = (value)->
  '.wrapper':
    if Array.isArray(value)
      onClick: ->
        console.log value
      span: trans('open') + ' ' + value.length
    else
      onClick: (ev)->
        wrapper = ev.currentTarget
        td = wrapper.parentElement
        replace wrapper, editCell(value)
        td.querySelector('input').select()
      span: value
      'I .edit-icon .fa .fa-pencil-square-o': ''
