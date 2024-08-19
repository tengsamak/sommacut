

# for auto genterate product code field 
import random
available_numbers = [x for x in range(10)] # number from 0 to 9
digit_code= 5 # product code have 5 digits

def generate_pro_code():
    new_number_list = [str(random.choice(available_numbers)) for _ in range(digit_code)]
    #new_number_list = str(random.randint(00000,99999))
    new_number_str = "".join(new_number_list)
    #new_number_str = new_number_list
    print("pro_code:",new_number_str)
    return new_number_str