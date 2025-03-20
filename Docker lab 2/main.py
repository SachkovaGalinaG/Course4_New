import pandas as pd

def print_df(path_to_csv: str):
    df = pd.read_csv(path_to_csv)
    print(df)

if __name__ == "__main__":
    print_df("data.csv")