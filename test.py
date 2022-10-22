import unittest

from PaymentHandler import Item, PaymentHandler, ProcessType
from Models import PDT

class TestItem(unittest.TestCase):

    def test_getter_setter(self):
        item = Item("Id", "Box", 10, 1)

        self.assertEqual(item.item_id, "Id")
        self.assertEqual(item.item_name, "Box")
        self.assertEqual(item.unit_price, 10)
        self.assertEqual(item.item_quantity, 1)

        with self.assertRaises(ValueError):
            item.unit_price = -1
        
        with self.assertRaises(ValueError):
            item.item_quantity = -1


class IestPaymentHanler(unittest.TestCase):

    def test_add_item_cart(self):
        handler = PaymentHandler("SB1286", True)
        
        item1 = Item("Id-0", "box", 12, 1)
        item2 = Item("Id-1", "Cat", 20, 4)
        item3 = Item("Id-0", "box", 12, 1)

        handler.add_item(item1)
        handler.add_item(item2)
        handler.add_item(item3)

        expected = [{'itemId': 'Id-0', 'itemName': 'box', 'unitPrice': 12, 'quantity': 2}, {'itemId': 'Id-1', 'itemName': 'Cat', 'unitPrice': 20, 'quantity': 4}]
        
        self.assertEqual(handler.items, expected)
    
    def test_add_item_express(self):
        handler = PaymentHandler("SB1286", True)
        
        handler.checkout_process = ProcessType.Express

        item1 = Item("Id-0", "box", 12, 1)
        item2 = Item("Id-1", "Cat", 20, 4)
        item3 = Item("Id-0", "box", 12, 1)

        handler.add_item(item1)
        
        with self.assertRaises(Exception):
            handler.add_item(item2)

        handler.add_item(item3)

        expected = [{'itemId': 'Id-0', 'itemName': 'box', 'unitPrice': 12, 'quantity': 2}]
        
        self.assertEqual(handler.items, expected)
    
    def test_remove_item(self):
        handler = PaymentHandler("SB1286", True)
        
        item1 = Item("Id-0", "box", 12, 1)
        item2 = Item("Id-1", "Cat", 20, 4)
        item3 = Item("Id-0", "box", 12, 1)
        item4 = Item("Id-2", "Dog", 30, 2)

        handler.add_item(item1)
        handler.add_item(item2)
        handler.add_item(item3)
        handler.add_item(item4)

        handler.remove_item(item4.item_id)

        expected = [{'itemId': 'Id-0', 'itemName': 'box', 'unitPrice': 12, 'quantity': 2}, {'itemId': 'Id-1', 'itemName': 'Cat', 'unitPrice': 20, 'quantity': 4}]
        
        self.assertEqual(handler.items, expected)


class TestPDT(unittest.TestCase):

    def test_getter_setter(self):
        pdt = PDT("Q7kc5gDaHEyjBi")

        pdt.merchant_order_id = "order-id"
        self.assertEqual(pdt.merchant_order_id, "order-id")
        self.assertEqual(pdt.merchantOrderId, "order-id")

        pdt.transaction_id = "transaction-id"
        self.assertEqual(pdt.transaction_id, "transaction-id")
        self.assertEqual(pdt.transactionId, "transaction-id")

    def test_as_dict(self):
        pdt = PDT("Q7kc5gDaHEyjBi")
        
        self.assertEqual(pdt.as_dict(), {'requestType': 'PDT', 'pdtToken': 'Q7kc5gDaHEyjBi'})

        pdt.merchant_order_id = "order-id"
        pdt.transaction_id = "transaction-id"

        self.assertEqual(pdt.as_dict(), {'requestType': 'PDT', 'pdtToken': 'Q7kc5gDaHEyjBi', 'transactionId': 'transaction-id', 'merchantOrderId': 'order-id'})


if __name__ == "__main__":
    unittest.main()