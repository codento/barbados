
lang = 'fi'
@setLang = (newLang)->
  throw Error "invalid language" unless dict[newLang]
  lang = newLang

@trans = (key)-> dict[lang][key]

dict =
  fi:
    club: 'klubi'
    harbours: 'satamat'
    name: 'nimi'
    open: 'avaa'

dict.en = {}
for key of dict.fi
  dict.en[key] = key
