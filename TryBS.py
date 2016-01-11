from bs4 import BeautifulSoup, element
import urllib2
import requests

prod='ZenBookASUS'
outFileAmazonInput = open('outFileinput'+prod+'.txt', 'w')
outFileAmazonOutput = open('outFileoutput'+prod+'.txt', 'w')

#outFileAmazonRaw = open('outFile'+prod+'Raw.txt', 'w')
outFileAmazonTitle = open('outFile'+prod+'Title.txt', 'w')
outFileAmazonText = open('outFile'+prod+'Text.txt', 'w')

#f = open('/Users/sanjanaagarwal/Desktop/outFileAmazon.xlsx')
# outFileAmazon = csv.reader(f, delimiter='\t')
errorFile = open('errorFile'+prod+'.txt', 'w')
x = 1
# To show end of reviews: a id="end-reviews"
# To show beginning of reviews: hr id="reviews-filter-bar"

#beginning = soup.find("hr", {"id": "reviews-filter-bar"})
#ending = soup.find("a", {"id": "end-reviews"})
while x < 74:
    #print(x)
    #http://www.amazon.com/Fire_Phone_13MP-Camera_32GB/product-reviews/B00EOE0WKQ/ref=cm_cr_pr_btm_link_2?ie=UTF8&showViewpoints=1&sortBy=byRankDescending&pageNumber=2
    url='http://www.amazon.com/Zenbook-UX305LA-13-3-Inch-Titanium-Windows/product-reviews/B013KKANTE/ref=cm_cr_pr_btm_link_4?ie=UTF8&showViewpoints=1&sortBy=byRankDescending&pageNumber=' + str(x)
    print(x)
    r=requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    tableCustomerReview = soup.find_all("div", {"class": "a-section review"})  # for the customer review table
    #tableCustomerReview.
    #tableHelpfulQuotient = soup.find_all("span", attrs={"class": "a-size-small a-color-secondary review-votes"})
    # How many people found it helpful
    #tableReviewTitle = soup.find_all("a", attrs={"class": "a-size-base a-link-normal review-title a-color-base a-text-bold"})
    #<i class="a-icon a-icon-star a-star-4 review-rating"><span class="a-icon-alt">
    #tableStarRating = soup.final_all("span", attrs={"class": "a-icon-alt"})

    for rev in tableCustomerReview:
        customerReview = rev
        #print(customerReview)
        reviewvotes = rev.find("span", attrs={"class": "a-size-small a-color-secondary review-votes"})
        if reviewvotes:
            reviewvotes = reviewvotes.string
            reviewvotes = reviewvotes.split(" ")
        else:
            reviewvotes=["null", "null", "null"]
        #class="a-icon-alt"
        #Title: "a" ///a-size-base a-link-normal review-title a-color-base a-text-bold
        title = rev.find("a", attrs={"class": "a-size-base a-link-normal review-title a-color-base a-text-bold"})
        title=title.string
        stars = rev.find("span", attrs={"class": "a-icon-alt"})
        stars=stars.string
        stars=stars.split(" ")

        #Verified Purcahse class="a-size-mini a-color-state a-text-bold"
        verifiedpurchase = rev.find("span", attrs={"class": "a-size-mini a-color-state a-text-bold"})
        if verifiedpurchase:
            verifiedpurchase="1"
        else:
            verifiedpurchase="0"
        #topsomething reviewer
        '''
        <span class="a-size-mini a-color-link c7yBadgeAUI c7yTopDownDashedStrike c7y-badge-text a-text-bold">TOP 500 REVIEWER</span>
        <span class="a-size-mini a-color-link c7yBadgeAUI c7yTopDownDashedStrike c7y-badge-text a-text-bold">VINE VOICE</span>
        '''
        badge = rev.find("span", attrs={"class": "a-size-mini a-color-link c7yBadgeAUI c7yTopDownDashedStrike c7y-badge-text a-text-bold"})
        if badge:
            badge=badge.string
        else:
            badge="null"
        #date of reivew:
        '''
        <span class="a-size-base a-color-secondary review-date">on October 22, 2015</span>
        '''
        date = rev.find("span", attrs={"class": "a-size-base a-color-secondary review-date"})
        date=date.string
        #print date
        date=date.split(",")
        #print date
        date[0]=date[0][3:]
        date=date[0]+date[1]
        #format for books:
        '''
        <a class="a-size-mini a-link-normal a-color-secondary" href="/Rogue-Lawyer-John-Grisham/product-reviews/0385539436/ref=cm_cr_pr_rvw_fmt?ie=UTF8&amp;sortBy=byRankDescending&amp;formatType=current_format">Format: Hardcover</a>
        '''
        format = rev.find("a", attrs={"class": "a-size-mini a-link-normal a-color-secondary"})
        if format:
            #if format.string:
            if format.string:
                format=format.string

                indexofsc=format.index(":")

                format=format[indexofsc+2:]
            else:
                format = "Unidentified"
        else:
            format = "Unidentified"
        #comments:
        #<span class="review-comment-total a-hidden">12</span>
        comments = rev.find("span", attrs={"class": "review-comment-total a-hidden"})
        comments=comments.string
        #print(tableHelpfulQuotient)
        #reviews:
        #print type(1)
        #span a-size-base review-text
        reviewtext=rev.find("span", attrs={"class": "a-size-base review-text"})
        for br in reviewtext.contents:

            if isinstance(br, element.NavigableString):
                outFileAmazonText.write(br.encode("UTF-8"))
                #print br
            elif isinstance(br, element.Tag):
                outFileAmazonText.write("<br/>".encode("UTF-8"))
                #print "<br/>"
        outFileAmazonText.write("\n")

        #print (reviewvotes[0]+","+reviewvotes[2]+","+stars[0]+","+verifiedpurchase+","+badge+","+date+","+format+","+comments)
        #print(title)
        try:
            #customerReview1 = tableCustomerReview.string.strip()  # REMOVE THIS STATEMENT
            #outFileAmazonRaw.write(str(customerReview))
            #outFileAmazonRaw.write("\n\n\n")
            outFileAmazonInput.write(stars[0]+","+verifiedpurchase+","+badge+","+date+","+format+","+comments)
            outFileAmazonInput.write("\n")
            #reviewvotes[0]+","+reviewvotes[2]+","+

            outFileAmazonOutput.write(reviewvotes[0]+","+reviewvotes[2])
            outFileAmazonOutput.write("\n")
            outFileAmazonTitle.write(title.encode("UTF-8"))
            outFileAmazonTitle.write("\n")

        except Exception as e:
            errorFile.write(str(x) + "***********" + str(e) + "***********" + '\n')
            pass


    x += 1
outFileAmazonInput.close()
#outFileAmazonRaw.close()
outFileAmazonTitle.close()
errorFile.close()
outFileAmazonText.close()
outFileAmazonOutput.close()
