# -*- coding:utf-8 -*-

from pyse import Pyse, TestRunner
from time import sleep
import time
import unittest


class MeetingTest(unittest.TestCase):

	def test_book_meeting(self):
		''' 
		book meeting room
		'''
		email  = 'bjzhangjiwei'
		passwd = 'Zjw163163'
		
		date = self.get_date()
		if date is None: return
		driver = Pyse("chrome")
		driver.max_window()
		
		#login
		driver.open("http://meeting.oa.netease.com/oaMeeting/login.jsp#login")
		while not driver.get_display("class=>email-suffix"):
			driver.click_text(u"邮箱登录")
		driver.clear("name=>loginid")
		driver.type("name=>loginid", email)
		driver.clear("name=>userpassword")
		driver.type("name=>userpassword", passwd)
		driver.click_text(u"立即登录")
		sleep(3)
		self.assertEqual("http://meeting.oa.netease.com/oaMeeting/bjroom.jsp#home/city", driver.get_url())
		
		#输入筛选条件
		'''
		js = "document.getElementsByClassName('ac_selectCalendar')[0].getAttribute('value')"
		driver.js(js)
		today = driver.get_attribute("name=>date", 'value')
		tomorrow = today.split('-')[:2] + [str(int(today.split('-')[2]) + 1)]
		tomorrow = '-'.join(tomorrow)
		'''
		js = "document.getElementsByName('date')[0].setAttribute('value', '" + date + "')"
		driver.js(js)
		sleep(2)
		driver.click('class=>ac_settingFloor')
		sleep(1)
		driver.click("xpath=>//*[@id='jq-interactive-sprite']/table/tbody/tr[2]/td[2]/div/div[4]/div[1]/div[2]/ul/li[7]")
		sleep(1)
		driver.click("class=>ac_interactiveConfirm")
		sleep(2)
		
		#选择会议室
		driver.click('xpath=>//html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[3]/div/dl[2]/dd[1]/ul/li[6]')
		driver.click('xpath=>//html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[3]/div/dl[2]/dd[1]/ul/li[3]')
		driver.click('xpath=>//html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[4]/a')
		sleep(2)
		driver.click("xpath=>//*[@id='jq-interactive-sprite']/table/tbody/tr[2]/td[2]/div/div[4]/div/dl[4]/dd/div")
		while not driver.get_display("xpath=>//*[@id='neteaseUser']/div/div[3]/div[2]/div/div[1]/div/div[1]/ul/li[1]/strong"):
			sleep(2)
		driver.double_click("xpath=>//*[@id='neteaseUser']/div/div[3]/div[2]/div/div[1]/div/div[1]/ul/li[8]/strong")
		driver.click("xpath=>//*[@id='jq-interactive-MultiNeteaseUser']/table/tbody/tr[2]/td[2]/div/div[5]/em[1]/a")
		driver.type("xpath=>//*[@id='jq-interactive-sprite']/table/tbody/tr[2]/td[2]/div/div[4]/div/dl[5]/dd/input", 'Regular meeting')
		driver.click("xpath=>//*[@id='jq-interactive-sprite']/table/tbody/tr[2]/td[2]/div/div[5]/em[1]/a")
		sleep(2)
		
		#验证预定成功
		self.assertTrue(driver.get_display("class=>mine-booked"))
		driver.click("xpath=>//html/body/div[3]/div[1]/div[2]/a[2]")
		sleep(2)
		self.assertEqual("http://meeting.oa.netease.com/oaMeeting/bjroom.jsp#mine", driver.get_url())
		#js =" var str = ''; var arr = document.getElementsByClassName('time-item');for (var i in arr){str += arr[i].innerHTML;}"
		#print str(driver.js(js))
		row_len = len(driver.driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/div/div[2]/table/tbody/tr")) 
		datetime = ''
		for i in range(1, row_len + 1):
			datetime += driver.get_element('xpath=>//html/body/div[3]/div[2]/div/div/div/div[2]/table/tbody/tr[%d]/td[4]' % i).text.encode('utf-8')
		self.assertTrue(date in datetime)
		
		driver.quit()

	def get_date(self, timestamp = None):
		now = time.time() if timestamp is None else timestamp
		date = time.localtime( int(now) + 24*60*60*7 )
		if date[6] == 5 or date[6] == 6:
			return None
		return time.strftime("%Y-%m-%d", date)
		

if __name__ == '__main__':
	unittest.main()
