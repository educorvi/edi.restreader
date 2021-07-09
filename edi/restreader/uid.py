import random
import datetime

powder_successfulluid = False
while powder_successfulluid == False:
    random_number = str(random.randint(100000, 999999))
    print(random_number)

    fullyear = datetime.datetime.now().year
    shortyear = str(fullyear)[2:]
    print(shortyear)

    generated_uid = "PD"+shortyear+random_number
    print(generated_uid)
    powder_successfulluid = True