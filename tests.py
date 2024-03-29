from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from unittest import skip
import sys




class FunctionalTest(StaticLiveServerTestCase):
	
	@classmethod
	def setUpClass(cls): 
		for arg in sys.argv: 
			if 'liveserver' in arg: 
				cls.server_url = 'http://' + arg.split('=')[1] #
				return 
		super().setUpClass()
		cls.server_url = cls.live_server_url
		
	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		#self.browser.implicitly_wait(1)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes
		#to check out its homepage
		self.browser.get(self.live_server_url)
		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#self.fail('Finish the test!')
		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'), 
			'Enter a to-do item'
			)
		# She types "Buy peacock feathers" into a text box (Edith's hobby
		# is tying fly-fishing lures)
		inputbox.send_keys('Buy peacock feathers')
		# When she hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a toto-do list table
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		#table = self.browser.find_element_by_id('id_list_table')
		#rows = table.find_elements_by_tag_name('tr')
		#self.assertIn('1: Buy peacock feathers',[row.text for row in rows])
		# There is still a textbox inviting her to add another item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		#self.fail('Finish the Test!')
		# The page updates again, and now shows both items on her list
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		self.assertIn(
			'2: Use peacock feathers to make a fly' , 
			[row.text for row in rows]
			)
		#The page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		#Now a new user, Francis, comes along to the site.

		##We use a new browser session to make sure that no information
		##ofEdith's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Francis visits the home page. There is no sign of Edith's
		#list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		#Francis starts a new list by entering a new item. He
		#is less interesting than Edith...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		#Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#Agian, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		#Satisfied, they both go back to sleep
		#self.fail('Finish the test!')
		# She visits that URL - her to-do list is still there.

		# Satisfied, she goes back to sleep
class LayoutAndStylingtest(FunctionalTest):

	def test_layout_and_styling(self):
		#Edith goes to the homepage
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024,768)

		#She notices the input box is nicely centered
		# She starts a new list and sees the input is nicely
		# centered there too
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
		inputbox.location['x'] + inputbox.size['width'] / 2,
		512,
		delta=5)

		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
		inputbox.location['x'] + inputbox.size['width'] / 2,
		512,
		delta=5)


class ItemValidationTest(FunctionalTest):
	@skip
	def test_cannot_add_empty_list_items(self):
		#Edith goes to the home page and accidentally tries to submit
		#an empty list item. She hits Enter on the empty input box

		#The homepage refreshes, and there is an error message saying
		#that list items cannot be blank

		#She tries again with some text for the item, which now works

		#Perversely, she now decides to submit a second blank list item

		#She receives a similar warning on the list page

		#And she can correct it by filling some text in
		self.fail('Write me!')
