import logging

from ..controller.TableController import TableController

logger = logging.getLogger("Vendor Controller")

TABLE_NAME = "vendor"


class VendorController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

    def insert_platform_beans(self, beans):
        query = f"INSERT INTO `{self.db_name}`.`vendor-analysis` (`timestamp`, `market`, `name`, `registration_date`," \
                f" `normalized_score`) VALUES (%s, %s, %s, %s, %s)"

        values = []
        for bean in beans:
            value = (bean.timestamp, bean.market, bean.name, bean.registration, bean.score_normalized)

            values.append(value)

        self.mysql_db.insert(query, values)

    def insert_beans(self, beans):
        attributes = ["timestamp", "market", "name", "score", "score_normalized", "registration",
                      "registration_deviation", "last_login", "last_login_deviation", "sales", "info",
                      "feedback", "pgp"]

        # Retrieve the greatest feedback id

        new_beans = []
        for bean in beans:
            for attr in attributes:
                val = getattr(bean, attr)
                if isinstance(val, list):
                    val = ", ".join(str(elem) for elem in val)
                    setattr(bean, attr, val)
            new_beans.append(bean)

        super(VendorController, self).insert_beans(new_beans)

    def retrieve_markets(self):
        query = "SELECT {0}.market from {1}.{0} GROUP BY {0}.market".format(TABLE_NAME, self.db_name)
        header, results = self.mysql_db.search(query)

        markets = []
        for result in results:
            markets.append(result[0].lower())

        return markets

    def retrieve_vendors(self):
        query = "SELECT DISTINCT {0}.timestamp, {0}.market, {0}.name FROM {1}.{0} ORDER BY {0}.timestamp DESC"\
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        markets = {}

        for result in results:
            timestamp = result[0]
            market = result[1]
            name = result[2]

            if market not in markets:
                markets[market] = {}

            if str(timestamp) not in markets[market]:
                markets[market][timestamp] = []

            markets[market][timestamp].append(name)

        return markets

    def retrieve_vendor(self, vendor):
        query = "SELECT * FROM {1}.{0} WHERE {0}.name = %s ORDER BY {0}.timestamp DESC" \
            .format(TABLE_NAME, self.db_name)

        values = (vendor,)

        header, results = self.mysql_db.search(query, values)

        markets = {}

        for result in results:
            vendor = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                vendor[attribute] = value

            timestamp = vendor["timestamp"]
            market = vendor["market"]
            del vendor["timestamp"]
            del vendor["market"]

            if market not in markets:
                markets[market] = {}

            #if timestamp not in markets[market]:
            #    markets[market][timestamp] = []

            # Get a single vendor for each timestamp
            # MULTIPLE VENDOR: markets[market][timestamp].append(vendor)
            markets[market][timestamp] = vendor


        return markets

    def retrieve_vendor_by_pgp(self, pgp):
        query = "SELECT {0}.name, {0}.market, {0}.pgp FROM {1}.{0} WHERE {0}.pgp = %s".format(TABLE_NAME, self.db_name)
        values = (pgp,)

        header, results = self.mysql_db.search(query, values)

        pgp_graph = {}

        for result in results:
            vendor_name = result[0]
            market = result[1]

            pgp_graph[market] = vendor_name

        return pgp_graph

    def delete_dumps(self, market, timestamps):
        query = "DELETE FROM `{0}`.`{1}` WHERE (`market` = %s) AND (`timestamp` = %s)".format(self.db_name, TABLE_NAME)

        values = []
        for timestamp in timestamps:
            values.append((market, timestamp))

        self.mysql_db.delete(query, values)

    def get_vendor_filtered(self):
        """
        This function retrieves vendor data from MySql DB, based on the following attributes:
        timestamp, market, name, info,registration,score_normalized
        """
        query = f"SELECT timestamp, market, name, info, registration, score_normalized FROM {self.db_name}.{TABLE_NAME}"
        header, results = self.mysql_db.search(query)

        final_data = []
        for vendor_info in results:
            if vendor_info[3] == None:
                vendor_info_list = list(vendor_info)
                vendor_info_list[3] = ''
                vendor_info_tuple = tuple(vendor_info_list)
                final_data.append(vendor_info_tuple)
            else:
                final_data.append(vendor_info)

        return final_data

    def get_vendor_country(self):
        query = 'SELECT vendor.name, vendor.market, product.ships_from, product.ships_to FROM anita.vendor INNER JOIN' \
                ' anita.product ON vendor.name = product.vendor;'

        header, results = self.mysql_db.search(query)

        vendor_country = []
        for line in results:
            vendor_country.append(dict(zip(header, line)))

        return vendor_country