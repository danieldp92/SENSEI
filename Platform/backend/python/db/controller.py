from db.mysql_connection import MySqlDB

DB_NAME = "anita"


class PseudonymizedVendorController:
    def __init__(self):
        self.db = MySqlDB()

    def get_vendors_alias(self):
        """
        Search for the alias-real_name key-value
        :return: Dict containing all alias-name of a vendor
        """

        query = f'SELECT * FROM {DB_NAME}.pseudonymized_vendors;'
        header, results = self.db.search(query)

        # Dict alias - vendor name
        vendor_alias = {}
        for row in results:
            alias = row[0]
            name = row[1]
            vendor_alias[alias] = name

        return vendor_alias


class ReviewController:
    def __init__(self):
        self.db = MySqlDB()

    def get_reviews(self):
        """
        Get the content of the review table
        :return: Review list
        """

        query = f'SELECT * FROM {DB_NAME}.reviews;'
        header, results = self.db.search(query)

        reviews = []
        for line in results:
            reviews.append(dict(zip(header, line)))

        return reviews

    def get_pseudonymized_reviews(self):
        """
        Get the content of the review table, with pseudonyms instead of real names
        :return: Pseudonyms review list
        """

        reviews_table = "reviews"
        pseudonymized_vendors_table = "pseudonymized_vendors"

        query = "SELECT {0}.feedback_id, {0}.id, {1}.pseudonym AS `name`, {0}.message, {0}.product, {0}.deals, " \
                "{0}.market, {0}.timestamp, {0}.macro_category FROM {2}.{0} JOIN {2}.{1} ON {0}.name = {1}.alias;"\
            .format(reviews_table, pseudonymized_vendors_table, DB_NAME)

        header, results = self.db.search(query)

        reviews = []
        for line in results:
            reviews.append(dict(zip(header, line)))

        return reviews

    def n_reviews_per_country(self):
        query = "SELECT ships_from, count(message) as n_reviews " \
                f"FROM {DB_NAME}.reviews JOIN {DB_NAME}.products_cleaned ON reviews.product = products_cleaned.name " \
                "WHERE ships_from is not NULL " \
                "GROUP BY ships_from;"

        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def n_sales_per_vendor(self):
        query = "SELECT reviews.name, COUNT(reviews.name) as n_sales " \
                f"FROM {DB_NAME}.reviews JOIN {DB_NAME}.`vendor-analysis` ON reviews.name = `vendor-analysis`.name " \
                "GROUP BY reviews.name;"

        header, results = self.db.search(query)

        n_sales = {}
        for row in results:
            n_sales[row[0]] = row[1]

        return n_sales

    def n_review_foreach_market(self):
        query = f"SELECT market, COUNT(DISTINCT(message)) FROM {DB_NAME}.reviews GROUP BY market;"

        header, results = self.db.search(query)

        market_reviews = {}
        for row in results:
            market_reviews[row[0]] = row[1]

        return market_reviews

    def n_review(self):
        market_reviews = self.n_review_foreach_market()

        tot_reviews = 0
        for market in market_reviews:
            tot_reviews += market_reviews[market]

        return tot_reviews


class ProductCleanedController:
    def __init__(self):
        self.db = MySqlDB()

    def get_distinct_timestamps(self):
        query = f"SELECT distinct products_cleaned.timestamp FROM {DB_NAME}.products_cleaned;"

        header, results = self.db.search(query)

        return [row[0] for row in results]

    def get_product_cleaned(self):
        query = f'SELECT * FROM {DB_NAME}.products_cleaned;'

        header, results = self.db.search(query)

        products = []
        for line in results:
            products.append(dict(zip(header, line)))

        return products

    def n_products_per_country(self):
        query = "SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, " \
                "count(name) as n_products " \
                f"FROM {DB_NAME}.ints, {DB_NAME}.`products_cleaned` " \
                "WHERE ships_from is not NULL " \
                "GROUP BY country;"

        query = f"SELECT DISTINCT(ships_from), COUNT(name) as n_products FROM {DB_NAME}.`products_cleaned` " \
                f"WHERE ships_from is not NULL GROUP BY ships_from ORDER BY n_products DESC;"

        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def best_vendor(self, country=None):
        """
        Takes the vendor with the higher number of product on the market
        """

        if not country:
            query = "SELECT vendor, COUNT(vendor) as n_products " \
                    f"FROM {DB_NAME}.products_cleaned " \
                    "GROUP BY vendor " \
                    "ORDER BY n_products DESC;"
            header, results = self.db.search(query)
        else:
            query = "SELECT vendor, COUNT(vendor) as n_products " \
                    f"FROM {DB_NAME}.products_cleaned " \
                    "WHERE ships_from = %s " \
                    "GROUP BY vendor " \
                    "ORDER BY n_products DESC;"
            value = (country,)
            header, results = self.db.search(query, value)

        if not results:
            return None

        best_vendor = results[0][0]
        return best_vendor

    def n_sales_per_country(self):
        query = f"SELECT ships_from, ROUND(SUM(price),2) FROM {DB_NAME}.products_cleaned GROUP BY ships_from;"

        header, results = self.db.search(query)

        countries_price = {}
        for row in results:
            countries_price[row[0]] = row[1]

        return countries_price

    def n_products_foreach_market(self):
        query = f"SELECT DISTINCT(market), COUNT(name) FROM {DB_NAME}.products_cleaned GROUP BY market;"

        header, results = self.db.search(query)

        market_products = {}
        for row in results:
            market_products[row[0]] = row[1]

        return market_products

    def n_products(self):
        market_products = self.n_products_foreach_market()

        tot_products = 0
        for market in market_products:
            tot_products += market_products[market]

        return tot_products


class VendorAnalysisController:
    def __init__(self):
        self.db = MySqlDB()

    def get_distinct_ships_from(self):
        query = "(SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country " \
                f"FROM {DB_NAME}.`ints`, {DB_NAME}.`vendor-analysis` " \
                "WHERE ships_from is not NULL) " \
                "UNION " \
                "(SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country " \
                f"FROM {DB_NAME}.`ints`, {DB_NAME}.`products_cleaned` " \
                "WHERE ships_from is not NULL) " \
                "ORDER BY country;"

        header, results = self.db.search(query)

        countries = [row[0] for row in results]

        return countries

    def n_vendors_per_country(self):
        query = "SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, " \
                "count(name) as n_vendors " \
                f"FROM {DB_NAME}.ints, {DB_NAME}.`vendor-analysis` " \
                f"WHERE ships_from is not NULL " \
                f"GROUP BY country"

        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def n_vendors_foreach_market(self):
        """
        Number of vendors for each market
        """

        query = f"SELECT market, COUNT(DISTINCT(name)) as n_vendors FROM {DB_NAME}.`vendor-analysis` GROUP BY market;"

        header, results = self.db.search(query)

        market_vendors = {}
        for row in results:
            market_vendors[row[0]] = row[1]

        return market_vendors

    def n_vendors(self):
        market_vendors = self.n_vendors_foreach_market()

        tot_vendors = 0
        for market in market_vendors:
            tot_vendors += market_vendors[market]

        return tot_vendors


def get_markets():
    db = MySqlDB()

    query = f"SELECT DISTINCT(market) from {DB_NAME}.products_cleaned " \
            "UNION " \
            f"SELECT DISTINCT(market) from {DB_NAME}.`vendor-analysis` " \
            "UNION " \
            f"SELECT DISTINCT(market) from {DB_NAME}.reviews;"

    header, results = db.search(query)

    return [row[0] for row in results]





