import feedparser
from flask import Flask, render_template, request
 
 
app = Flask(__name__)
 
# (1-2)定義RSS源
RSS_FEEDS = {
    '自由時報 Business': "https://news.ltn.com.tw/rss/business.xml",
    '自由時報 World': "https://news.ltn.com.tw/rss/world.xml",
    '經濟部 本部新聞': "https://www.moea.gov.tw/Mns/populace/news/NewsRSSdetail.aspx?Kind=1",
    '經濟部 即時新聞澄清': "https://www.moea.gov.tw/Mns/populace/news/NewsRSSdetail.aspx?Kind=9",
    'Yahoo 最新新聞': "https://tw.stock.yahoo.com/rss?category=news",
    'Yahoo 台股動態': "https://tw.stock.yahoo.com/rss?category=tw-market",
    'Yahoo 國際財經': "https://tw.stock.yahoo.com/rss?category=intl-markets",
}
 
@app.route('/')
def index():
    articles = []
    # (1-2)從多個RSS源中抓取文章並將它們存入articles列表
    # items()方法會返回字典中的每個鍵值對，source是RSS源的名稱，feed是RSS源的URL。
    for source, feed in RSS_FEEDS.items():
        # 解析RSS源的URL，返回一個包含解析後資料的物件
        parsed_feed = feedparser.parse(feed)
        # 提取文章條目
        entries = [(source, entry) for entry in parsed_feed.entries]
        # 將entries列表中的所有元組添加到articles列表中
        articles.extend(entries)
    # 按降序排序
    articles = sorted(articles, key=lambda x: x[1].published_parsed, reverse=True)
    # 從請求參數中獲取當前頁數，如果沒有指定頁數，則默認為第1頁。
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    # 計算當前頁的起始和結束索引
    start = (page-1) * per_page
    end = start + per_page
    # 存儲當前頁的文章，通過切片操作articles[start:end]獲取。
    paginated_articles = articles[start:end]
    # 使用整數除法//計算總頁數，並加1以確保即使文章數量不是整數倍，也能正確顯示總頁數
    total_pages=total_articles // per_page + 1
 
    return render_template('index.html', 
            articles=paginated_articles, page=page, total_pages=total_pages)

@app.route('/search')
def search():
    # (1-3)從URL的查詢參數中獲取名為q的值，並將其存儲在變數query中。例如，如果URL是/search?q=python，那麼query的值將是python
    query = request.args.get('q')
 
    # 用來存儲從RSS源中獲取的文章
    articles = []
    # 用feedparser解析每個RSS源，並將解析後的條目與其來源一起存儲在entries列表中，
    # 然後將entries列表中的所有條目添加到articles列表中
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)
    # 過濾articles列表，只保留標題中包含查詢字串（不區分大小寫）的文章，並將結果存儲在results列表中
    results = [article for article in articles if query.lower() in article[1].title.lower()]
     
    return render_template('search_results.html',
            articles=results, query=query)
 
if __name__ == '__main__':
    app.run(debug=True)