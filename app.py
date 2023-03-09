# TODO: Allow users to edit their orders, Special requests, spreadsheet, real-time form generation, success page
from flask import Flask, render_template, request
from pyntree import Node
from uuid import UUID, uuid4
import phonenumbers
from order_reports import make_pdf

app = Flask(__name__)
options = Node('options.json')
orders = Node('orders.pyn', autosave=True)


def parse_order(order: Node) -> Node:
    parsed_order = Node()
    parsed_order.items = {}
    for i in order.values:
        try:
            UUID(i)  # If valid UUID
        except ValueError:  # Not an item
            if i.startswith('type:') or i.startswith('category:'):
                pass
            elif i == 'phone':
                parsed_order.set(i, phonenumbers.parse(order.get(i)(), 'US'))
            else:
                parsed_order.set(i, order.get(i)())
            continue

        if int(order.get(i)()) == 0:  # None ordered
            pass
        else:
            parsed_order.items.set(i, {})
            item = parsed_order.items.get(i)
            item.quantity = order.get(i)()
            item.set('category', order.get(f'category:{i}')())
            if order.has(f'type:{i}'):
                item.set('type', order.get(f'type:{i}')())
    return parsed_order


@app.route('/')
def index():
    return render_template('flower-form.html', options=options)


@app.route('/submit/flowers', methods=['POST'])
def collect_data():
    print(dict(request.form))
    data = parse_order(Node(dict(request.form)))
    print(repr(data))
    order_id = str(uuid4())
    orders.set(order_id, data)
    make_pdf(order_id)
    return 'OK!'


if __name__ == '__main__':
    app.run()
