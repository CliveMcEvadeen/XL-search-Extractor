import pandas as pd

def get_records():
    try:
        # Read data from the Excel file
        df = pd.read_excel('card.xlsx', sheet_name='ACTIVITIES', skiprows=1)
        
        # Filter out columns with all NaN values
        df_filtered = df.dropna(axis=1, how='all')
        df_filtered = df_filtered.iloc[2:]

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

# call to db insert
def overall_student_record():

    '''collecting student data and inserting it into the db'''

    for student_data in excell_to_db_var():
        name=student_data['name']
        lin=student_data['lin']
        gender=student_data['sex']
        stream=student_data['stream']

        subject_details={}

        for subject_data in student_data['subjects_data']:
            for subject, activities in subject_data.items():
                subject_details[subject]=activities
                
            # subject_and_activities={subject_details['subject']:subject_details['activity_vars']})
                c1=subject_details['activity_vars']['c1']
                c2=subject_details['activity_vars']['c2']
                c3=subject_details['activity_vars']['c3']
                c4=subject_details['activity_vars']['c4']

            print(c1)
            print(c2)
            print(c3)
            print(c4)
            print()

overall_student_record()
