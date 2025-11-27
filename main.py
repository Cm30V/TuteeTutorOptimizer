import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment

tutees_df = pd.read_csv(r"")
tutors_df = pd.read_csv(r"")


def split_to_list(cell_value):
    if pd.isna(cell_value):
        return []
    return [item.strip() for item in str(cell_value).split(",")]

tutors_df['course_list'] = tutors_df["Classes you feel comfortable tutoring:"].apply(split_to_list)
tutors_df['times_list'] = tutors_df["Availability "].apply(split_to_list)


unmatched_tutors = tutors_df[tutors_df['Matched'] == False].reset_index(drop=True)
unmatched_tutees = tutees_df[tutees_df['Matched'] == False].reset_index(drop=True)



unmatched_tutees['course_list'] = unmatched_tutees["Math class"].apply(split_to_list)
unmatched_tutees['times_list'] = unmatched_tutees["Availability"].apply(split_to_list)

num_tutors = len(unmatched_tutors)
num_tutees = len(unmatched_tutees)



weight_matrix = np.zeros((num_tutors, num_tutees))



for i in range(num_tutors):
    tutor_courses = unmatched_tutors.loc[i, 'course_list']
    tutor_times = unmatched_tutors.loc[i, 'times_list']
    for j in range(num_tutees):
        tutee_courses = unmatched_tutees.loc[j, 'course_list']
        tutee_times = unmatched_tutees.loc[j, 'times_list']
        score = 0
        courseIntersections = set(tutor_courses) & set(tutee_courses)
        courseIntersections = len(courseIntersections)

        availabilityIntersections = set(tutor_times) & set(tutee_times)
        availabilityIntersections = len(availabilityIntersections)
        
        if courseIntersections == 0 or availabilityIntersections == 0:
            weight_matrix[i,j] = -99999
        else:
            weight_matrix[i,j] = availabilityIntersections*5 + courseIntersections*50

        

size = max(num_tutors, num_tutees)
padded_matrix = np.full((size, size), -99999)
padded_matrix[:num_tutors, :num_tutees] = weight_matrix

row_ind, col_ind = linear_sum_assignment(-padded_matrix)


for tutor_id, tutee_id in zip(row_ind, col_ind):

    if tutor_id >= num_tutors or tutee_id >= num_tutees:
        continue
    

    tutor_name = unmatched_tutors.loc[tutor_id, "name (first, last)"]
    tutee_name = unmatched_tutees.loc[tutee_id, "student name \nLast, First"]

    tutor_email = unmatched_tutors.loc[tutor_id, "Email Address*"]
    tutee_email = unmatched_tutees.loc[tutee_id, "student email"]

    tutor_phone = unmatched_tutors.loc[tutor_id, "Phone Number\n"]
    tutee_phone = unmatched_tutees.loc[tutee_id, "student cell"]

    score = weight_matrix[tutor_id, tutee_id]

    if score == -99999:
        continue
    
    print(f"{tutor_name} is matched with {tutee_name} Score: {score}")
    print(f"Tutor Email & Number: {tutor_email}, {tutor_phone} ")
    print(f"Tutee Email & Number: {tutee_email}, {tutee_phone} ")
    print()
