import csv
from pathlib import Path
from typing import List


def read_csv_file(file_name: str) -> List[List]:
    """
    Reads a CSV file into a List of rows, where each row is a List of fields
    """

    file_path = Path(file_name)

    if not file_path.exists():
        # Because the file does not exist, we will initialize an empty CSV file with the correct
        # headers and columns then read that initial file
        initial_rows = [["timestamp", "amount", "category"]]
        save_csv_file(file_name, initial_rows)

    contents = []
    with open(file_path.absolute(), mode="r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
        for row in csv_reader:
            contents.append(row)

    print("Loaded {} CSV rows".format(len(contents)))
    return contents


def save_csv_file(file_name: str, rows: List, overwrite_existing: bool = True) -> None:
    """
    Saves a CSV file to disk under the supplied file name
    """

    file_path = Path(file_name)

    if file_path.exists() and not overwrite_existing:
        print(
            (
                "Error when trying to save CSV to '{}' because it exists and the overwrite_existing "
                "flag is False"
            ).format(file_path.absolute())
        )
        return

    with open(file_path.absolute(), mode="w", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        for row in rows:
            csv_writer.writerow(row)


def get_categories_from_dataset(dataset: List) -> List[str]:
    """
    Gets a set of categories from the dataset by looking at the column named "category"
    """

    if dataset is None or len(dataset) == 0:
        return []

    # Loop over the first row (assume that the first row is the CSV header row) and find
    # the column that is lowercase equal to "category". Increment the index_of_category_column
    # by 1 each time we move to the next field until we find the name or finish all the columns
    index_of_category_column = -1
    header_row: List[str] = dataset[0]
    for field in header_row:
        index_of_category_column += 1
        if field.lower() == "category":
            break

    if index_of_category_column == -1:
        # The above loop looked at all the column headings (assuming that the first row of
        # the dataset are CSV column headings) and did not find any lowercase strings that
        # matched 'category', so we cannot continue as this is a logic error
        return []

    # At this point we know what our category column looks like, so iterate over the whole
    # dataset and look at only field at the position of the index to add only the unique,
    # distinct values from the category column.
    # Because the first row is the CSV heading or column names, start iterating from the 2nd
    # row which is at index 1, hence dataset[1:]
    found_categories = []
    for row in dataset[1:]:
        if row[index_of_category_column] not in found_categories:
            found_categories.append(row[index_of_category_column])

    # Sort alphabetically
    found_categories.sort()

    return found_categories
