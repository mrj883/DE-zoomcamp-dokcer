import pandas as pd
import sys


print(sys.argv[1])

df = pd.DataFrame(
            {"A":[1,2], "B":[2,4]}
            )
df.to_parquet("file.parquet")