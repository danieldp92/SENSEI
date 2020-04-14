# ----------------------------------------------------------
# This is a template the Empire Market
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------
#ONLY VENDOR RIGHT NOW
# -- IMPORT
from datetime import datetime
from dateutil.parser import parse

# -- MAIN PAGE DATA
def pagetype(soup):
    """Define the type of the page.
    Find a part in the page that indicates that the page is a vendor or product page. For example: 'item info' indicates
    that the page is about an item, thus a product page."""
    # try:
    #     # example: if soup.find('div', {'class': "table_wrapper"}).find_all('th')[0].text == 'Item info:' :
    #     if x == y:  # Replace 'x == y'
    #         return 'product'
    # except:
    #     pass

    try:
        # example: if soup.find('table', {'class': "msgtable"}).find('th').text == 'Vendor stats:':
        if soup.find('h1', {'class': 'seth1'}).find('i').text == '| User Profile':
            return 'vendor'
    except:
        pass


# -- PRODUCT DATA
# def p_product_name(soup):
#     """ Return the name of the product as string """
#     # example: return soup.find('div',{"content grid-8-12"}).find('h3').text
#     return None  # replace None
#
#
# def p_vendor(soup):
#     """Return the name of the vendor as string"""
#     # example: return soup.find('div', {'class': "table_wrapper"}).find('a').text
#     return None  # replace None
#
#
# def p_ships_from(soup):
#     """Return the place from where the package is delivered as string"""
#     # example: return soup.find('div', {"table_wrapper"}).find_all('td')[3].text
#     return None  # replace None
#
#
# def p_ships_to(soup):
#     """Return where the package can be delivered to as string
#     If multiple; provide in a list"""
#     # example: return soup.find('div', {"table_wrapper"}).find_all('td')[5].text
#     return None  # replace None
#
#
# def p_price(soup):
#     """Return the price of the produc as string"""
#     # example: return soup.find('div', {'price_big_inner'}).text.split()[0]
#     return None  # replace None
#
#
# def p_info(soup):
#     """Return the info as string"""
#     # example: return soup.find('div', {'prod_info'}).text
#     return None  # replace None

# -- VENDOR DATA
def v_vendor_name(soup):
    """ Return the name of the vendor as string """
    # example: return soup.find('h3').text
    return soup.find('h1', {'class' : 'seth1'}).text.split(' |')[0]

def v_score(soup):
    """ Return the score of the vendor in one of these two options:
    1. The score in a tuple as first item (float/int) and second item as the scale (float/int).
    Example: a 4.95 of scale up to 5: (4.95, 5), 97.7%: (97.7, 100)
    2. When the item consists of positives and negatives and possibly neutrals. [positive, negative, neutral]
    example: 96 negative, no neutrals, 20 positives: [20, 96, 0]
    """
    # example: return soup.find_all('td')[5].text
    return (float(soup.find('p', {'class' : 'bold'}).find('b').text),100)

def v_registration(soup):
    """ Return the moment of registration as datetime object """
    # example: return None # DRUGS MARKET ONLY HAS A SINCE
    return parse(soup.find('span', {'class' : 'bold1'}).text)

def v_last_login(soup):
    """ Return the moment of last login as datetime object, or as str when the time is a 'since'"""
    # example: return None # DRUGS MARKET ONLY HAS A SINCE
    return parse(soup.find_all('tbody')[1].find_all('td')[7].text)

def v_sales(soup):
    """ Return the number of sales, also known as transactions or orders as int """
    # example: return int(soup.find_all('td')[7].text)
    s = soup.find('h3', {'class': 'user_info_mid_head'}).find('span').text
    return s[s.find("(") + 1:s.find(")")]

def v_info(soup):
    """ Return the information as a string """
    # example: return soup.find('div', {'class' : 'container container_large'}).text
    if soup.find('a', {'class' : 'tablinks focus'}).text == 'About':
        return soup.find('p', {'style' : "word-wrap: break-word; white-space: pre-wrap;"}).text

def v_pgp(soup):
    """ Returns the pgp as a string """
    if soup.find('a', {'class': 'tablinks focus'}).text == 'PGP':
        return soup.find('pre', {'style': "word-wrap: break-word; white-space: pre-wrap;"}).text

# -- VENDOR FEEDBACK DATA
# def v_feedback(soup):
#     """ Return the feedback for the vendors"""
#     feedback_list = []
#
#     #loop to walk through the feedback
#     for item in soup:
#
#         # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
#         score  =  None #fill in
#
#         # The message of the feedback in type str
#         message =  None #fill in
#
#         # The time in datetime object or time ago in type str
#         date = None #fill in
#
#         # Name of the product that the feedback is about (if any) in type str
#         product = None #fill in
#
#         # User, name of the user or encrypted user name (if any) in type str
#         user = None #fill in
#
#         # Deals by user (if any) in type int or str (if range)
#         deals = None #fill in
#
#
#         #in json format
#         feedback_json = {
#             'score' : score,
#             'message' : message,
#             'date' : date,
#             'product' : product,
#             'user' : user,
#             'deals' : deals
#         }
#         feedback_list.append(feedback_json)
#
#     return feedback_list

# -- PRODUCT FEEDBACK DATA
# def p_feedback(soup):
#     """ Return the feedback for the product"""
#     feedback_list = []
#
#     #loop to walk through the feedback
#     for item in soup:
#
#         # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
#         score  =  None #fill in
#
#         # The message of the feedback in type str
#         message =  None #fill in
#
#         # The time in datetime object or time ago in type str
#         date = None #fill in
#
#         # User, name of the user or encrypted user name (if any) in type str
#         user = None #fill in
#
#         #in json format
#         feedback_json = {
#             'score' : score,
#             'message' : message,
#             'date' : date,
#             'user' : user,
#         }
#         feedback_list.append(feedback_json)
#
#     return feedback_list




