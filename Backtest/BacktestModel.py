import pandas as pd

def convert_row_to_swap(row: dict, decimals0: int=18, decimals1: int=18): 
    """
    Convert a row from the swap data to clean swap data.
    """
    val = {
        "amount0": clean_bignumber(row["amount0"], decimals0),
        "amount1": clean_bignumber(row["amount1"], decimals1),
        "price": convert_sqrtprice(row["sqrtPriceX96"]) * 10 ** (decimals0 - decimals1),
        "timestamp": pd.to_datetime(row["timestamp"], format="%B %d, %Y, %I:%M %p"),
        "tick": clean_bignumber(row["tick"], decimals=1, lift=1, base=1)
    }

    val["swap_value"] = abs(val["amount0"] * val["price"])

    return val

class BacktestModel:
    def __init__(self, swap_data, decimals0: int=18, decimals1: int=18):
        self.raw_swap_data = swap_data
        self.swap_data = pd.DataFrame([convert_row_to_swap(row, decimals0, decimals1) for row in swap_data])

class FixedFeeModel(BacktestModel):
    def __init__(self, swap_data, decimals0: int=18, decimals1: int=18, fee:
                 Number=0.0005):
        super().__init__(swap_data, decimals0, decimals1)
        self.swap_data["earned_fees"] = self.swap_data["swap_value"] * fee

  
