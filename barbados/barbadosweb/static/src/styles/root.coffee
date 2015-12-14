

{ bgColor } = require 'src/styles/colors.coffee!'

require('jsonCss').addStyles
  '*':
    boxSizing: 'border-box'
    position: 'relative'
  'body':
    fontFamily: 'arial'
    fontSize: 12
    # '*':
    #   boxSizing: 'content-box'
    background: bgColor #'white'
    color: '#444'
    section:
      width: sectionWidth
      marginTop: 20

      #'td:nth-child(4)': textAlign: 'right'
    '.hierarchic':
      width: '30%'
      marginLeft: '40%'
      fontSize: 16
      color: '#444 !important'
      lineHeight: 20
      '.inspect_object.rows .pointer:hover':
        background: 'white' # "hsla(0,0%,0%,0.05)"
