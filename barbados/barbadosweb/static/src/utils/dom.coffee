

{ createNode } = require 'jsonHtml'

@replace = (oldEl, newEl)->
  newEl = createNode newEl if typeof newEl is 'object'
  if (parentEl=oldEl.parentElement)?
  then parentEl.replaceChild newEl, oldEl # returns oldEl..
  else console.info "failed to replace node", newEl, oldEl
  newEl # don't work when newEl was object, since documentFragment will be empty



# NOT USED currently:

@get    = (selector, parentEl=document)-> parentEl.querySelector    selector
@getAll = (selector, parentEl=document)-> parentEl.querySelectorAll selector

@append = @addTo = (parent_element, content)->
  content = createNode content if typeof content is 'object'
  parent_element.appendChild content
  content

@prepend = (parentEl, content)->
  content = createNode content if typeof content is 'object'
  parentEl.insertBefore content, parentEl.firstChild

# IE supported way of removing element
# (for chrome, firefox: el.remove())
@remove = (element)->
  element = @get element if typeof element is 'string'
  if (parentEl=element?.parentElement)?
  then parentEl.removeChild element
  else console.info "failed to remove node", element

@removeChildren = (node)->
  while node.firstChild
    node.removeChild node.firstChild

@replaceChildren = (node, newContent)->
  @removeChildren node
  @append node, newContent
