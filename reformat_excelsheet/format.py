"""
Format:
&category
#item
//comment
qualifier
qualifier
qualifier
(repeat)
"""

from pyntree import Node
from uuid import uuid4

with open('formatme.txt', 'r') as file:
    data = file.read().split('\n')

new = Node()

for line in data:
    if line.startswith('&'):
        category_id = str(uuid4())
        new.set(category_id, {'_name': line[1:], 'items': {}})
        category = new.get(category_id).items
    elif line.startswith('#'):
        item_id = str(uuid4())
        category.set(item_id, {'_name': line[1:], 'comment': None, 'price': 0, 'qualifiers': []})
        item = category.get(item_id)
    elif line.startswith('//'):
        item.comment = line[2:]
    elif not line:
        pass
    else:
        item.qualifiers = item.qualifiers() + [line]

new.save('out.json')
