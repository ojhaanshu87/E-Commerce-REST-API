import unittest
import server
from mongoengine import connect
from models import Users, Products
from flask import jsonify, session
import json


class TestFlaskRestApi(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.app = server.app.test_client()
		cls.app.testing = True
		cls.req_context = server.app.test_request_context()
		cls.req_context.push()
		connect('apitest', host='mongomock://localhost')

	def test02_register_user_customer(self):
		with self.app:
			response = self.app.post('/register', data=json.dumps(dict(
					username = 'anshu_customer',
					email='anshu_customer@gmail.com',
					password='password' 
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status': True, 'message': "successfully register"}).get_data(as_text=True)))

	def test03_register_user_seller(self):
		with self.app:
			response = self.app.post('/register', data=json.dumps(dict(
					username = 'anshu_seller',
					email='anshu_seller@gmail.com',
					password='password',
					is_admin=False,
					is_seller=True 
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status': True, 'message': "successfully register"}).get_data(as_text=True)))

	def test04_register_user_admin(self):
		with self.app:
			response = self.app.post('/register', data=json.dumps(dict(
					username = 'anshu_admin',
					email='anshu_admin@gmail.com',
					password='password',
					is_admin=True,
					is_seller=False 
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status': True, 'message': "successfully register"}).get_data(as_text=True)))

	def test05_login_failure(self):
		with self.app:
			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password='incorrect_password',
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status': False}).get_data(as_text=True)))
			self.assertNotIn('username', session)

	def test06_login_success(self):
		with self.app:
			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password='password',
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status': True}).get_data(as_text=True)))
			self.assertIn('username', session)
			session.clear()

	def test07_add_product_by_customer_with_login(self):
		with self.app:
			session.clear()
			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_customer',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			customer = Users.objects(username='anshu_customer').first()

			response = self.app.post('/addProduct', data=json.dumps(dict(
					title = 'Nike Football',
					description = 'Football game ball',
					price = 300,
					user_id = customer.user_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message':'Operation not permitted'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test08_add_product_by_seller_with_login(self):
		with self.app:
			session.clear()
			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			seller = Users.objects(username='anshu_seller').first()

			response = self.app.post('/addProduct', data=json.dumps(dict(
					title = 'Cricket Bat',
					description = 'Indian Cricket Bat',
					price = 1500,
					user_id = seller.user_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Item Added Successfully.'}).get_data(as_text=True)))
			self.assertIn('username', session)
			session.clear()

	def test09_add_product_by_admin_with_login(self):
		with self.app:
			session.clear()
			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			admin = Users.objects(username='anshu_admin').first()

			response = self.app.post('/addProduct', data=json.dumps(dict(
					title = 'TT Bat',
					description = 'Indian TT Bat',
					price = 600,
					user_id = admin.user_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Item Added Successfully.'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test10_search_items_not_in_database_by_id(self):
		with self.app:
			response = self.app.get('/searchProductById?prod_id=ABCD', follow_redirects=True)
			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message':'The Item is not available.'}).get_data(as_text=True)))

	
	def test11_update_product_not_in_database_by_seller_with_login(self):
		with self.app:
			session.clear()
			seller = Users.objects(username='anshu_seller').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.post('/updateProduct', data=json.dumps(dict(
					user_id=seller.user_id,
					product_id='ABCD',
					title = 'Cricket Bat',
					description = 'Updated description Indian Cricket Bat',
					price = 20000
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message':'No matching product found to Update'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test12_update_product_by_seller_without_ownership_with_login(self):
		with self.app:
			session.clear()
			seller = Users.objects(username='anshu_seller').first()
			product = Products.objects(title='TT Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.post('/updateProduct', data=json.dumps(dict(
					user_id=seller.user_id,
					product_id=product.product_id,
					title = 'TT Bat',
					description = 'Updated description Indian TT Bat',
					price = 2000
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message': 'Not Permitted because you did not add the product'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test13_update_product_by_seller_with_ownership_with_login(self):
		with self.app:
			session.clear()
			seller = Users.objects(username='anshu_seller').first()
			product = Products.objects(title='Cricket Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.post('/updateProduct', data=json.dumps(dict(
					user_id=seller.user_id,
					product_id=product.product_id,
					title = 'Cricket Bat',
					description = 'Updated description Indian Cricket Bat',
					price = 20000
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Item updated by Seller'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test14_update_product_not_in_database_by_admin_with_login(self):
		with self.app:
			session.clear()
			admin = Users.objects(username='anshu_admin').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.post('/updateProduct', data=json.dumps(dict(
					user_id=admin.user_id,
					product_id='ABCD',
					title = 'TT Bat',
					description = 'Updated description Indian TT Bat',
					price = 2000
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message':'No matching product found to update'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test15_update_product_by_admin_without_ownership_with_login(self):
		with self.app:
			session.clear()
			admin = Users.objects(username='anshu_admin').first()
			product = Products.objects(title='Cricket Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.post('/updateProduct', data=json.dumps(dict(
					user_id=admin.user_id,
					product_id=product.product_id,
					title = 'Cricket Bat',
					description = 'Updated description Indian Cricket Bat',
					price = 20000
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Item updated by Admin'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test16_update_product_by_admin_with_ownership_with_login(self):
		with self.app:
			session.clear()
			admin = Users.objects(username='anshu_admin').first()
			product = Products.objects(title='TT Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.post('/updateProduct', data=json.dumps(dict(
					user_id=admin.user_id,
					product_id=product.product_id,
					title = 'TT Bat',
					description = 'Updated description Indian TT Bat',
					price = 2000
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Item updated by Admin'}).get_data(as_text=True)))
			self.assertIn('username', session)

	
	def test17_delete_product_by_customer_with_login(self):
		with self.app:
			session.clear()
			customer = Users.objects(username='anshu_customer').first()
			product = Products.objects(title='Cricket Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_customer',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.delete('/deleteProduct', data=json.dumps(dict(
					user_id=customer.user_id,
					product_id=product.product_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message': 'Opearation not permitted'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test18_delete_product_not_in_database_by_seller_with_login(self):
		with self.app:
			session.clear()
			seller = Users.objects(username='anshu_seller').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.delete('/deleteProduct', data=json.dumps(dict(
					user_id=seller.user_id,
					product_id='ABCD'
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message':'No matching product found to delete'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test19_delete_product_by_seller_without_ownership_with_login(self):
		with self.app:
			session.clear()
			seller = Users.objects(username='anshu_seller').first()
			product = Products.objects(title='TT Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.delete('/deleteProduct', data=json.dumps(dict(
					user_id=seller.user_id,
					product_id=product.product_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message': 'Not Permitted because you did not add the product'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test20_delete_product_by_seller_with_ownership_with_login(self):
		with self.app:
			session.clear()
			seller = Users.objects(username='anshu_seller').first()
			product = Products.objects(title='Cricket Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_seller',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.delete('/deleteProduct', data=json.dumps(dict(
					user_id=seller.user_id,
					product_id=product.product_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Product Deleted'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test21_delete_product_not_in_database_by_admin_with_login(self):
		with self.app:
			session.clear()
			admin = Users.objects(username='anshu_admin').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.delete('/deleteProduct', data=json.dumps(dict(
					user_id=admin.user_id,
					product_id='ABCD'
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':False, 'message':'No matching product found to delete'}).get_data(as_text=True)))
			self.assertIn('username', session)

	

	def test22_delete_product_by_admin_with_ownership_with_login(self):
		with self.app:
			session.clear()
			admin = Users.objects(username='anshu_admin').first()
			product = Products.objects(title='TT Bat').first()

			response = self.app.post('/login', data=json.dumps(dict(
					username = 'anshu_admin',
					password = 'password'
				)), content_type='application/json', follow_redirects=True) 

			response = self.app.delete('/deleteProduct', data=json.dumps(dict(
					user_id=admin.user_id,
					product_id=product.product_id
				)), content_type='application/json', follow_redirects=True)

			self.assertEqual(json.loads(response.data), json.loads(jsonify({'status':True, 'message':'Product Deleted'}).get_data(as_text=True)))
			self.assertIn('username', session)

	def test23_logout(self):
		with self.app:
			response = self.app.get('/logout', follow_redirects=True)
			self.assertNotIn('username', session)

	@classmethod
	def tearDownClass(cls):
		for user in Users.objects:
			user.delete()

		for product in Products.objects:
			product.delete()

		cls.req_context.pop()


if __name__ == "__main__":
    unittest.main()