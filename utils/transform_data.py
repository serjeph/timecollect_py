# transform_data.py

import datetime as dt
from utils.clean_data import delete_columns
from utils.get_week_types import get_name, set_types
from utils.project_helper import get_client


def transform_data(dataset, data_list, employee, project):
    """
    Transforms raw data into a structured format suitable for further processing.

    Args:
      data_list: A list of lists representing the raw data.
      object: An Employee object containing employee information.

    Returns:
      A list of dictionaries, where each dictionary represents a single entry
      with keys like 'employee_id', 'date', 'project_code', 'work_type', and 'hours'.
    """
    transformed_data = []

    if data_list and employee:
        # Add default values for missing columns at the end of row index 1
        data_list[0] = data_list[0] + ["0.00", "0.00", "0.00", "0.00"]

        # Remove unnecessary columns
        # TODO(developer): make this dynamic!!
        data = delete_columns(
            data_list, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
        )

        # Clean data: Replace first 9 elements of the second row with the first row
        data[1][:9] = data[0][:9]

        # Define work types
        # TODO(developer): change "['直接'] * 20" to "['直接'] * 40" for year 2025
        work_data = ["日付"] * 3 + ["間接"] * 7 + ["直接"] * 40

        # Clean project codes: Propagate project codes across relevant columns
        for i in range(3):
            for j in [11, 15, 19, 23, 27, 31, 35, 39, 43, 47]:
                data[0][i + j] = data[0][j - 1]

        # Structure data: Extract and organize data into a lists of lists
        for col in range(len(data[0]) - 3):
            for row in range(len(data) - 2):
                year = int(data[row + 2][0])
                month = int(data[row + 2][1])
                day = int(data[row + 2][2])
                employee_name = str(employee.nickname)
                employee_team = str(employee.team)
                week_type = str(get_name(dataset, year, month, day))
                task_type = str(data[1][col + 3])
                project_code = str(data[0][col + 3])
                work_type = str(work_data[col + 3])
                worked_hours = round(float(data[row + 2][col + 3]), 2)
                client = str(get_client(project_code, project))

                transformed_data.append(
                    [
                        client,
                        row + 1,
                        year,
                        month,
                        day,
                        week_type,
                        employee_name,
                        project_code,
                        task_type,
                        work_type,
                        employee_team,
                        worked_hours,
                    ]
                )

    return transformed_data


if __name__ == "__main__":

    datasets = set_types(2023, 12, 31)
