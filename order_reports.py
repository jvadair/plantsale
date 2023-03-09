from pyntree import Node
from md2pdf.core import md2pdf

orders = Node("orders.pyn")
options = Node("options.json")


def make_pdf(order_id):
    orders.file.reload()
    order = orders.get(order_id)()  # Get order Node, then its value (another Node)
    md_to_write = []
    print(f'Building report for {order.get("customer_name")()}')
    md_to_write.append(f"# {order.get('customer_name')()}")
    md_to_write.append('')
    md_to_write.append(f"## Phone: {order.get('phone')().national_number}")
    md_to_write.append('')
    md_to_write.append(f"ID: `{order_id}`")  # order.name is the name of the Node, aka the ID
    md_to_write.append('')
    md_to_write.append('---')
    md_to_write.append('')
    md_to_write.append('## Order summary')
    for item in order.items.values:
        item = order.items.get(item)
        type_string = f', {item.type()}' if item.has('type') else ''
        item_name = options.get(item.category()).items.get(item.name)._name()
        md_to_write.append(f"- ({item.quantity()}{type_string}) {options.get(item.category()).items.get(item.name)._name()}")  # (3, blue) Petunias
    md2pdf(f'order_reports/{order_id}.pdf', '\n'.join(md_to_write))


if __name__ == "__main__":
    for order_id in orders.values:
        make_pdf(order_id)