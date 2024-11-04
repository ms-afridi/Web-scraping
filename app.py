from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/review", methods=['POST'])
def review():
    if request.method == 'POST':
        try:
            # Get the product URL from the form
            product_link = request.form['content']

            # Set headers for the request
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
            }

            # Use Selenium to fetch the product page
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            # Get the product page content
            driver.get(product_link)
            product_html = bs(driver.page_source, 'html.parser')

            # Extract product name
            product_name = product_html.findAll("div", {"class": "C7fEHH"})[0].div.text

            # Extract all reviews
            comment_boxes = product_html.findAll("div", {"class": "RcXBOT"})

            reviews = []
            for comment_box in comment_boxes:
                try:
                    name = comment_box.div.div.find_all('p', {'class': '_2NsDsF AwS1CA'})[0].text
                except:
                    name = 'No Name'

                try:
                    rating = comment_box.div.div.div.div.text
                except:
                    rating = 'No Rating'

                try:
                    comment_head = comment_box.div.div.div.p.text
                except:
                    comment_head = 'No Comment Heading'

                try:
                    comment = comment_box.div.div.find_all('div', {'class': ''})[0].div.text
                except:
                    comment = 'No Comment'

                review_dict = {
                    "Name": name,
                    "Rating": rating,
                    "CommentHead": comment_head,
                    "Comment": comment
                }
                reviews.append(review_dict)

            driver.quit()

            # Render the template with product name and reviews
            return render_template('results.html', product_name=product_name, reviews=reviews)

        except Exception as e:
            print('The Exception message is:', e)
            return render_template('results.html', product_name=None, reviews=[], error=str(e))

if __name__ == "__main__":
    app.run(debug=True)




