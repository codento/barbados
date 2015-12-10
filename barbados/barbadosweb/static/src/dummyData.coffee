
rand = (nums=2)-> Math.random().toFixed(nums).slice(2)

@tables =
  boats:
    for i in [1..4]
      'id': rand(4)
      'name':          'na'.repeat(i)
      'boat_type':     'type-' + rand(2)
      'model':         'model-' + rand(3)
      'manufacturer':  'ma'.repeat(i)
      'registration_number': 'reg-'+rand(3)
      'length': rand(1) + ' m'
      'height': '1.'+rand(1) + ' m'
      'weight': rand(3) + 'kg'
  users:
    for i in [1..3]
      'username': 'me'.repeat(i)
      'first_name': 'fi'.repeat(i)
      'last_name': 'la'.repeat(i)
      'email': 'fi'.repeat(i) + '@' + 'la'.repeat(i) + '.me'


@hierarchic =
  'Kalle':
    boats:
      'Silvia':
        length: '10 m'
        "reg-number": "reg-175"
      'Maria':
        length: '7 m'
        "reg-number": "reg-311"
