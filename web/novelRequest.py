from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# Cấu hình Selenium với Chrome ở chế độ headless
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Không hiển thị trình duyệt
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

class MeTruyenChu:
    def __init__(self, url):
        self.URL = 'https://metruyenchu.com.vn'
        self.url = url
        driver.get(self.url)
        self.html = BeautifulSoup(driver.page_source,'html.parser')
        
        self.img =None
        self.title = None
        self.description = None
        self.author = None
        self.genre = None
        self.status = None
    def getNovelDetail(self):
        self.img = self.URL + self.html.select_one('div.book-info-pic img')['src']
        self.title = self.html.select_one('div.mRightCol h1').text
        self.description = self.html.select_one('div.scrolltext div').text
        self.author = self.html.select_one('div.book-info-text ul li a').text
        try:
            self.genre = self.html.select_one('div.book-info-text ul li.li--genres a').text
        except AttributeError:
            self.genre = "Tổng Hợp"
        self.status = self.html.select_one('span.label-status').text
    def getChapterContent(self,url_chapter):
        driver.get(url_chapter)
        self.content = driver.find_element(By.CLASS_NAME, 'truyen')
        return self.content.text
    def getNovelChapter(self, _list = []):
        self.chapter_list = self.html.select_one('#chapter-list div').select('a')
        self.list = []
        for i in self.chapter_list:
            if i.text not in _list:
                self.list.append([i.text, self.getChapterContent(self.URL + i['href']),])
        
        
        return self.list
                
    def Quit(self):
        driver.close()
        
