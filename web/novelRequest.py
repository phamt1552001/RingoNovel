from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re


class MeTruyenChu:
    def __init__(self, url):
        self.URL = 'https://metruyenchu.com.vn'
        self.url = url

        # Cấu hình Selenium với Chrome ở chế độ headless
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Không hiển thị trình duyệt
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")

        # Khởi tạo trình duyệt
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.driver.get(self.url)
        self.html = BeautifulSoup(self.driver.page_source, 'html.parser')

        self.img = None
        self.title = None
        self.description = None
        self.author = None
        self.genre = None
        self.status = None

    def getNovelDetail(self):
        """Lấy thông tin tiểu thuyết"""
        self.img = self.URL + self.html.select_one('div.book-info-pic img')['src']
        self.title = self.html.select_one('div.mRightCol h1').text
        self.author = self.html.select_one('div.book-info-text ul li a').text
        try:
            self.genre = self.html.select_one('div.book-info-text ul li.li--genres a').text
        except AttributeError:
            self.genre = "Tổng Hợp"
        try:
            self.description = self.html.select_one('div.scrolltext div').text
        except AttributeError:
            self.description = ''
        self.status = self.html.select_one('span.label-status').text

    def getChapterContent(self, url_chapter):
        """Lấy nội dung một chương"""
        self.driver.get(url_chapter)
        self.html = BeautifulSoup(self.driver.page_source, 'html.parser')  # Cập nhật lại self.html
        content = self.html.select_one('.truyen')  # Dùng BeautifulSoup thay vì Selenium
        return content.text if content else "Nội dung không tìm thấy"

    def getNovelChapter(self, _list=[]):
        """Lấy danh sách chương chưa có"""
        chapter_elements = self.html.select_one('#chapter-list div').select('a')
        new_chapters = []

        for chapter in chapter_elements:
            if chapter.text not in _list:
                chapter_content = self.getChapterContent(self.URL + chapter['href'])
                match = re.match(r"Chương (\d+): (.+)", chapter.text)
                if match:
                    chapter_number = int(match.group(1))  # Lấy số chương dưới dạng integer
                    chapter_title = match.group(2)        # Lấy tên chương
                else:
                    chapter_number = None
                    chapter_title = chapter.text  # Nếu không khớp, giữ nguyên tiêu đề ban đầu

                new_chapters.append([chapter_title, chapter_content, int(chapter_number)])

        return new_chapters

    def quit(self):
        """Đóng trình duyệt Selenium"""
        self.driver.quit()
