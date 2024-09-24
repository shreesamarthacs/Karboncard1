from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json


def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    lastest_financial_index_value = latest_financial_index(data)
    print(f"Latest Financial Index: {lastest_financial_index_value}")

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, lastest_financial_index_value
    )
    print(f"Total Revenue 5CR Flag: {total_revenue_5cr_flag_value}")

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, lastest_financial_index_value
    )
    print(f"Borrowing to Revenue Flag: {borrowing_to_revenue_flag_value}")

    iscr_flag_value = iscr_flag(data, lastest_financial_index_value)
    print(f"ISCR Flag: {iscr_flag_value}")

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }


if __name__ == "__main__":
    with open("data.json", "r") as file:
        content = file.read()
        data = json.loads(content)
        print("Data Loaded Successfully.")

        result = probe_model_5l_profit(data["data"])
        print("Final Flags Output:", result)
