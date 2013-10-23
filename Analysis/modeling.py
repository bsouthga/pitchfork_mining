# Review Modeling
# Ben Southgate
# 10/19/13

import shelve
import pandas as pd

# Pull data from shelf
def import_data():
    storage = shelve.open(os.path.join(path,'Pitchfork_Data_Shelf'))
    data = storage['data frame']
    storage.close()
    return data


def main():
    
    data_frame = import_data()


if __name__ == "__main__":
    main()