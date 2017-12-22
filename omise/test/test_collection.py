import unittest

from .helper import _ResourceMixin


class CollectionTest(_ResourceMixin, unittest.TestCase):

    def _getTargetClass(self):
        from .. import Collection
        return Collection

    def _getAccountClass(self):
        from .. import Account
        return Account

    def _makeOne(self):
        return self._getTargetClass().from_data({
            'object': 'list',
            'data': [
                {'object': 'account', 'id': 'acct_test_1'},
                {'object': 'account', 'id': 'acct_test_2'},
                {'object': 'account', 'id': 'acct_test_3'},
                {'object': 'account', 'id': 'acct_test_4'},
            ]
        })

    def test_len(self):
        collection = self._makeOne()
        self.assertEqual(len(collection), 4)

    def test_iter(self):
        collection = self._makeOne()
        iterable = iter(collection)
        firstItem = next(iterable)
        self.assertTrue(isinstance(firstItem, self._getAccountClass()))
        self.assertEqual(firstItem.id, 'acct_test_1')
        self.assertEqual(next(iterable).id, 'acct_test_2')
        self.assertEqual(next(iterable).id, 'acct_test_3')
        self.assertEqual(next(iterable).id, 'acct_test_4')

        def _func():
            next(iterable)
        self.assertRaises(StopIteration, _func)

    def test_getitem(self):
        collection = self._makeOne()
        self.assertTrue(isinstance(collection[0], self._getAccountClass()))
        self.assertEqual(collection[0].id, 'acct_test_1')
        self.assertEqual(collection[3].id, 'acct_test_4')
        self.assertEqual(collection[-1].id, 'acct_test_4')

    def test_retrieve(self):
        collection = self._makeOne()
        firstItem = collection.retrieve('acct_test_1')
        self.assertTrue(isinstance(firstItem, self._getAccountClass()))
        self.assertEqual(firstItem.id, 'acct_test_1')
        self.assertEqual(collection.retrieve('acct_test_2').id, 'acct_test_2')
        self.assertEqual(collection.retrieve('acct_test_3').id, 'acct_test_3')
        self.assertEqual(collection.retrieve('acct_test_4').id, 'acct_test_4')
        self.assertEqual(collection.retrieve('acct_test_5'), None)

    def test_retrieve_no_args(self):
        collection = self._makeOne()

        def _extract_id(item):
            return item.id
        firstItem = collection.retrieve()[0]
        self.assertTrue(isinstance(firstItem, self._getAccountClass()))
        self.assertEqual(
            list(map(_extract_id, collection.retrieve())),
            list(map(_extract_id, list(collection)))
        )
