@titelize = (str)->
  str.replace(/[-_]/g, ' ')
     .replace(/(^| )(\w)/g, (full,s,firstChar)-> s + firstChar.toUpperCase())
     .replace /(\w)([A-Z])/g, (f,s,c)-> s + ' ' + c

@if = (arg, true_str=arg, false_str)->
  return true_str if arg
  if false_str?
  then false_str
  else ''
