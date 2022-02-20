from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post,Category
from django.contrib.auth.models import User
# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump=User.objects.create_user(username='trump',password='somepassword')
        self.user_obama=User.objects.create_user(username='obama',password='somepassword')
        
        self.category_fuka=Category.objects.create(name='fuka',slug='fuka')
        self.category_culture=Category.objects.create(name='culture',slug='culture')

        self.post_001= Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='후카좋아',
            category=self.category_fuka,
            author=self.user_trump
        )

        self.post_002= Post.objects.create(
            title='두 번째 포스트입니다.',
            content='문화좋아',
            category=self.category_culture,
            author=self.user_obama
        )

        self.post_003= Post.objects.create(
            title='세 번째 포스트입니다.',
            content='밀리애니 나와',
            author=self.user_obama
        )

    def category_card_test(self,soup):
        categories_card = soup.find('div',id='categories-card')
        self.assertIn('Categories',categories_card.text)
        self.assertIn(f'{self.category_fuka.name} ({self.category_fuka.post_set.count()}',categories_card.text)
        self.assertIn(f'{self.category_culture.name} ({self.category_culture.post_set.count()}',categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)
            
        

    def navbar_test(self,soup):
        navbar = soup.nav
        # 1.5 Blog, About Me라는 문구가 네비게이션 바에 있다.
        self.assertIn('Blog',navbar.text)
        self.assertIn('About me',navbar.text)


        logo_btn = navbar.find('a',text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'],'/')
        
        home_btn = navbar.find('a',text='Home')
        self.assertEqual(home_btn.attrs['href'],'/')
        
        blog_btn = navbar.find('a',text='Blog')
        self.assertEqual(blog_btn.attrs['href'],'/blog/')
        
        about_me_btn = navbar.find('a',text='About me')
        self.assertEqual(about_me_btn.attrs['href'],'/about_me/')
        


    def test_post_list(self):

        self.assertEqual(Post.objects.count(),3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        

        self.navbar_test(soup)
        self.category_card_test(soup)


        main_area=soup.find('div',id='main-area')
        #print(main_area)
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title,post_001_card.text)
        self.assertIn(self.post_001.category.name,post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title,post_002_card.text)
        self.assertIn(self.post_002.category.name,post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        
        self.assertIn('미분류',post_003_card.text)
        self.assertIn(self.post_003.title,post_003_card.text)

        
        self.assertIn(self.user_trump.username.upper(),main_area.text)
        self.assertIn(self.user_obama.username.upper(),main_area.text)
        

        #포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(),0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content,'html.parser')

    def test_post_detail(self):
        #1.1 포스트가 하나 있다.
        """post_000=Post.objects.create(
            title='첫 번째 포스트입니다.',
            content = 'Hello World, We are the world.',
            author=self.user_trump,
        )"""

        #1.2 그 포스트의 url은 '/blog/1/'이다.
        self.assertIn(self.post_001.get_absolute_url(),['/blog/1/','/blog/1'])

        #2. 첫 번째 포스트의 상세 페이지 테스트
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #2.1. 첫 번재 포스트의 url로 접근하면 정상적으로 작동한다(200)
        self.navbar_test(soup)
        #2.2. 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.

        self.category_card_test(soup)
        
        #2.3. 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title,soup.title.text)
        #2.4. 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div',id='main-area')
        post_area = main_area.find('div',id='post-area')
        self.assertIn(self.post_001.title,post_area.text)
        #2.5. 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(),post_area.text)

        #아직 작성 불가

        #2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content,post_area.text)
