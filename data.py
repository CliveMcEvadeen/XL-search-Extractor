import pandas as pd

def get_records():
    try:
        # Read data from the Excel file
        df = pd.read_excel('card.xlsx', sheet_name='Sheet', skiprows=1)
        
        # Filter out columns with all NaN values
        df_filtered = df.dropna(axis=1, how='all')
        df_filtered = df_filtered.iloc[1:]

        subjects = df.iloc[1]
        # Dropping the first four columns
        column_drop = subjects[4:]

        # Dropping subjects with unnamed head labels
        subject_modified = column_drop.filter(regex=r'^(?!Unnamed)')
        subject_modified = pd.DataFrame(subject_modified)

        # List to store records
        records = []

        # Iterate through DataFrame rows 
        for index, row in df_filtered.iterrows():
            # Extract data from the row
            name = row['NAME']
            lin = row['LIN']
            stream = row['STREAM'] 
            sex = row['SEX']
            
            # Dictionary to store student data
            student_data = {'name': name, 'lin': lin, 'stream': stream, 'sex': sex, 'subjects': {}}
            
            # Iterate through subjects
            for subject in subject_modified.index:
                subject_data = {}

                # Get the index of the current subject column
                subject_index = df.columns.get_loc(subject)

                # Combine marks list and activities list
                activity_marks = []
                for i in range(subject_index, subject_index + 4):
                    cell_data = row.iloc[i]
                    if isinstance(cell_data, (int, float)):
                        activity_marks.append(round(cell_data, 1))
                    else:
                        activity_marks.append(cell_data)

                subject_data['activity_marks'] = activity_marks

                # Add subject data to the student's subjects dictionary
                student_data['subjects'][subject] = subject_data
            
            # Append student's data to the records list
            records.append(student_data)
            
        return records

    except FileNotFoundError:
        print("Error: File 'card.xlsx' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def excell_to_db(records=get_records()):
    if records:
        for idx, record in enumerate(records, start=1):
            print(f"Record {idx}:")
            print(f"Name: {record['name']}")
            for subject, data in record['subjects'].items():
                print(f"Subject: {subject}")
                print("Activities:")
                for idx, activity in enumerate(data['activity_marks'], start=1):
                    print(f"c{idx}: {activity}")
                print()
            print()
    else:
        print("No records found.")
        
# data test db variables
        
def excell_to_db_var(records=get_records()):
    data_list = []
    if records:
        for record in records:
            name = str(record['name'])
            lin=str(record['lin'])
            sex=str(record['sex'])
            stream=str(record['stream'])

            subjects_data = []
            for sub, data in record['subjects'].items():
                subject = sub
                activity_vars = {}
                for idx, activity in enumerate(data['activity_marks'], start=1):
                    activity_vars[f'c{idx}'] = activity
                subjects_data.append({'subject': subject, 'activity_vars': activity_vars})
            data_list.append({'name': name,'lin':lin, 'sex':sex, 'stream': stream, 'subjects_data': subjects_data})
    else:
        print("No records found.")
    
    return data_list

def combine_records(records):
    combined_records = {}

    for record in records:
        name = record['name']
        lin = record['lin']
        gender = record['sex']
        stream = record['stream']

        if name not in combined_records:
            # Initialize a new combined record for this->name
            combined_records[name] = {
                'name': name,
                'lin': lin,
                'gender': gender,
                'stream': stream,
                'subjects_data': {}
            }

        # Iterate through subjects in the current record
        for subject_data in record['subjects_data']:
            subject = subject_data['subject']
            activity_vars = subject_data['activity_vars']

            if subject not in combined_records[name]['subjects_data']:
                # Add subject and activities for this subject
                combined_records[name]['subjects_data'][subject] = activity_vars
            else:
                # Merge activities for existing subject
                combined_records[name]['subjects_data'][subject].update(activity_vars)

    return list(combined_records.values())

# Example usage:
def student_record():
    records = excell_to_db_var()
    combined_records = combine_records(records)

    for record in combined_records:
        name = record['name']
        lin = record['lin']
        gender = record['gender']
        stream = record['stream']

        print(f"Name: {name}, LIN: {lin}, Gender: {gender}, Stream: {stream}")
        
        for subject, activities in record['subjects_data'].items():
            c1 = activities['c1']
            c2 = activities['c2']
            c3 = activities['c3']
            c4 = activities['c4']
    
            print(f"Subject: {subject}, c1: {c1}, c2: {c2}, c3: {c3}, c4: {c4}")

        overall_student_data={}
        write_to_db={}

print(student_record())
