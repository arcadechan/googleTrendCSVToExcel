import os
import glob
import pandas as pd

# os.chdir('')
cwd = os.getcwd()
print("You've started the script in the following directory.: " + cwd)
response = input('Does this look correct? Yes (Y), No (N)? ').lower()

if response == 'y':
    print()
    pass
elif response == 'n':
    print('Make sure I (this script) and the files you want to merge are together in the same directory. \nExiting program!')
    quit()
else:
    print('I don\'t  recognize that response. Exiting program!')
    quit()

def find(list, needle):
    for index in range(len(list)):
        if needle in list[index]:
            return index
    return -1

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

if len(all_filenames) > 1:
    print('Found the following files:')
    for file in all_filenames:
        print(file)

    to_excel_array = []
    excel_headers = []

    csv_data = pd.read_csv(all_filenames[0])

    # Loop over first CSV and grab ALL columns to allow for next CSV match to this date
    count = 0
    for i in csv_data.itertuples():
        if count == 0:
            excel_headers.extend((i[0], i[1]))
            count = count + 1
            continue

        to_excel_array.append([i[0], i[1]])
        count = count + 1


    for i in range(1, len(all_filenames)):
        csv_data = pd.read_csv(all_filenames[i])
        count = 0

        for j in csv_data.itertuples():
            if count == 0:
                excel_headers.append(j[1])
                count = count + 1
                continue

            index = find(to_excel_array, j[0])

            if index >= 0:
                to_excel_array[index].append(j[1])

            count = count + 1

    df = pd.DataFrame(to_excel_array, columns=excel_headers)
    writer = pd.ExcelWriter(os.getcwd() + '\Trend Data.xlsx')
    df.to_excel(writer, header = excel_headers, sheet_name='Sheet 1', index=False)

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column)) + 2
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet 1'].set_column(col_idx, col_idx, column_width)

    writer.save()
else:
    print('I only found one file. I need at least two to merge their contents!')