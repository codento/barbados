@titleize = @titelize = (str)->
  str.replace(/[-_]/g, ' ')
     .replace(/(^| )(\w)/g, (full,s,firstChar)-> s + firstChar.toUpperCase())
     .replace /(\w)([A-Z])/g, (f,s,c)-> s + ' ' + c
     #.replace(/ (\w)/g, (full,firstChar)-> ' ' + firstChar.toUpperCase())
  #str.titleize() # TODO: drom sugar req


@if = ifs = (arg, true_str, false_str)->
  true_str = arg unless true_str?
  if arg
  then true_str
  else (if false_str? then false_str else '')
#
# @capitalize = (str)-> str[0].toUpperCase() + str.slice(1)
# 
# @dasherize = (str)->
#   str.replace(/([A-Z])/g, (full, match)-> '-' + match.toLowerCase())
#      .replace(/ /g, '-')
#
#
# @parsesToNumber = @isNumber = (str)-> not Number.isNaN parseInt str
#
# @truncate = (str, limit, truncStr='...')->
#   if str.length > limit
#   then str[0...limit] + truncStr
#   else str
#
#
# @random = (limit=20)->
#   (Math.random()+'')[2..limit+1]
#
# @remove = (full, remove)-> full.replace remove, ''
#
# @reverse = (str)->
#   str.split("").reverse().join('')
