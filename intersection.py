import csv, copy
from datetime import datetime

def read_interviewer(csv_file_location):
  csv.register_dialect('empDialect', skipinitialspace=True, strict=True)
  time_file = csv.DictReader(open(csv_file_location))
  time_list = []
  for data in time_file:
    time_list.append(data)
  return time_list



def get_empty(a_list):
    free_time_dict_of_set = dict()
    prev_date = datetime.strptime(a_list[0]['start'], "%Y-%m-%dT%H:%M:%S").date().strftime("%d-%m-%Y")
    empty_list = set()
    for a_dict in a_list:
        curr_date = datetime.strptime(a_dict['start'], "%Y-%m-%dT%H:%M:%S").date().strftime("%d-%m-%Y")
        if curr_date == prev_date:
            if a_dict["subject"] == "":
                start = datetime.strptime(a_dict['start'], "%Y-%m-%dT%H:%M:%S").time()
                end = datetime.strptime(a_dict['end'], "%Y-%m-%dT%H:%M:%S").time()
                empty_list.add(f"{start} - {end}")
        else:
            free_time_dict_of_set.update({str(prev_date) : copy.deepcopy(empty_list)})
            prev_date = curr_date
            empty_list.clear()
    free_time_dict_of_set[str(prev_date)] = empty_list
    return free_time_dict_of_set

def get_intersections(a1, a2, a3):
    common=dict()
    bordervalue = min(min(len(a1), len(a2)), len(a3))
    for i in range(0, bordervalue):
      common[list(a1.keys())[i]] = list(a1.values())[i].intersection(list(a2.values())[i], list(a3.values())[i])
    

def interview_time():
  pass


if __name__ == "__main__":  

  #delta = input("Duration of interview: ")
  ia1 = read_interviewer('IA1.csv')
  ia2 = read_interviewer('IA2.csv')
  ia3 = read_interviewer('IA3.csv')

  #ib1 = read_interviewer('IB1.csv')
  #ib2 = read_interviewer('IB2.csv')
  #ib3 = read_interviewer('IB3.csv')
  
  ia1_empty = get_empty(ia1)
  ia2_empty = get_empty(ia2)
  ia3_empty = get_empty(ia3)
  
  #ib1_empty = get_empty(ib1)
  #ib2_empty = get_empty(ib2)
  #ib3_empty = get_empty(ib3)

  get_intersections(ia1_empty, ia2_empty, ia3_empty)
  
  
  