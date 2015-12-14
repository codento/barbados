

{ bgColor } = require 'src/styles/colors.coffee!'

@headerHtml = 'th.remove': ''
@delHtml =
  'td.remove':
    'I .fa .fa-times': ''
    onClick: ->
      confirm "Haluatko varmasti poistaa rivin?"

{ bgColor } = require 'src/styles/colors.coffee!'

{ addStyles } = require 'jsonCss'
addStyles \
  '.tableSorter .remove':
    width: 50
    background: bgColor
    textAlign: 'left'
    paddingLeft: 10
    '.fa':
      #color: 'white'
      opacity: 0.3
      transition: 'opacity 400ms'
      '&:hover':
        opacity: 1
