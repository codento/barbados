

{ addStyles } = require 'jsonCss'
sectionWidth = 900

addStyles
  '*':
    boxSizing: 'border-box'

  'body':
    fontFamily: 'arial'
    fontSize: 14

    background: 'hsl(0, 0%, 90%)'
    color: '#444'

    section:
      width: sectionWidth
      marginTop: 20
    '.tableWrapper':
      background: 'white'
      padding: "5px 10px"
      borderRadius: 7
    table:
      width: '100%'
    h2:
      #textAlign: 'center'
      marginLeft: 6
      marginBottom: 2
      marginTop: 0
      fontSize: 16

    '.sortArrowAscending':
      content: "'daa'" # '0x' + ("▲").charCodeAt(0)
    th:
      fontSize: 12
    'tbody': #:not(\:first-child)
      tr:
        lineHeight: cellHeight = 26
        height: cellHeight
        '&:not(:last-child)':
          borderBottom: '1px solid #ddd'
      td:
        height: cellHeight
        width: 200
        textAlign: 'center'
        cursor: 'pointer'
        '&:hover .fa':
          display: 'inline'
        '.fa':
          display: 'none'
          marginLeft: 4
      #'td:nth-child(4)': textAlign: 'right'
    '.hierarchic':
      width: '30%'
      marginLeft: '40%'
      fontSize: 16
      color: '#444 !important'
      lineHeight: 20
      '.inspect_object.rows .pointer:hover':
        background: 'white' # "hsla(0,0%,0%,0.05)"
