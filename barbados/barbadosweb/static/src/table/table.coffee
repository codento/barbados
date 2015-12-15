

{ titelize } = require 'src/utils/string.coffee!'

{ addButton } = require './addRow.coffee!'
{ headerHtml, delHtml } = require './delRow.coffee!'
{ editCell, valueCell } = require './cell.coffee!'

@renderTable = (name, rows)->
  Section:
    h2: titelize name
    #'.tableWrapper':
    'table.tableSorter':
      'Thead':
        tr:
          (for key of rows[0]
            th:
              text: titelize key
          ).concat headerHtml
      'Tbody':
        for row in rows
          tr:
            (for key of row
              console.log key
              td: valueCell(key, row)
            ).concat delHtml
    me: addButton


{ bgColor, codentoColor } = require 'src/styles/colors.coffee!'

require('jsonCss').addStyles
    table:
      width: '100%'
      borderSpacing: 0
      borderCollapse: 'separate'
    h2:
      #textAlign: 'center'
      marginBottom: 5
      fontSize: 16
      marginLeft: 5
      color: 'white'
    '.sortArrowAscending':
      content: "'daa'" # '0x' + ("▲").charCodeAt(0)
#     table:
#       background: 'white'
    tr:
      background: 'white'
    th:
      color: codentoColor()
    td:
      cellPadding: 0
      border: 0
    'tbody': #:not(\:first-child)
      tr:
        lineHeight: cellHeight = 26
        height: cellHeight
        borderTop: '1px solid ' + bgColor
        overflow: 'hidden'
      td:
        height: cellHeight
        width: 200
        textAlign: 'center'
        cursor: 'pointer'
        '.wrapper':
          height: cellHeight
          overflowText: 'ellipsis'
        '&:hover .fa':
          opacity: 1
        '.edit-icon':
          position: 'absolute'
          right: 0
          top: 7
          #display: 'none'
          marginLeft: 4
          background: 'white'
          opacity: 0
          transition: '250ms'
        input:
          width: '100%'
