

@addButton =
  'I .add-new-row .fa .fa-plus-square': ''

{ addStyles } = require 'jsonCss'
addStyles
  '.add-new-row':
    color: 'white'
    fontSize: 16
    margin: '7px'
    transition: '400ms'
    cursor: 'pointer'
    '&:hover':
      transform: 'scale(1.3)'
