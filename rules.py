import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field


# Already implemented function for reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0


def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.
    """
    financial = data.get("financials")[financial_index]
    try:
        total_revenue = financial["pnl"]["lineItems"]["net_revenue"]
        return total_revenue
    except KeyError:
        return None  # Return None if net_revenue field doesn't exist


def total_borrowing(data: dict, financial_index):
    """
    Calculate the ratio of total borrowings to total revenue for the financial data.
    """
    financial = data.get("financials")[financial_index]
    try:
        total_revenue_value = total_revenue(data, financial_index)
        # Get long-term and short-term borrowings
        long_term_borrowings = financial["bs"]["lineItems"]["longTermBorrowings"]
        short_term_borrowings = financial["bs"]["lineItems"]["shortTermBorrowings"]
        total_borrowings = long_term_borrowings + short_term_borrowings
        
        # Calculate borrowing-to-revenue ratio
        if total_revenue_value and total_revenue_value > 0:
            return total_borrowings / total_revenue_value
        else:
            return None  # Return None if revenue is 0 or None
    except KeyError:
        return None  # Return None if required fields are missing


def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.
    """
    financial = data.get("financials")[financial_index]
    try:
        # Profit before interest and tax (PBIT)
        pbit = financial["pnl"]["lineItems"]["pbit"]
        # Depreciation
        depreciation = financial["pnl"]["lineItems"]["depreciation"]
        # Interest expense
        interest_expense = financial["pnl"]["lineItems"]["interestExpense"]

        # ISCR formula: (PBIT + Depreciation + 1) / (Interest expense + 1)
        iscr_value = (pbit + depreciation + 1) / (interest_expense + 1)
        return iscr_value
    except KeyError:
        return None  # Return None if any required field is missing


def iscr_flag(data: dict, financial_index):
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.
    """
    iscr_value = iscr(data, financial_index)
    if iscr_value is not None:
        return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED
    return FLAGS.WHITE  # If data is missing, return WHITE flag


def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.
    """
    revenue = total_revenue(data, financial_index)
    if revenue is not None:
        return FLAGS.GREEN if revenue >= 50_000_000 else FLAGS.RED
    return FLAGS.WHITE  # If data is missing, return WHITE flag


def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.
    """
    borrowing_ratio = total_borrowing(data, financial_index)
    if borrowing_ratio is not None:
        return FLAGS.GREEN if borrowing_ratio <= 0.25 else FLAGS.AMBER
    return FLAGS.WHITE  # If data is missing, return WHITE flag
