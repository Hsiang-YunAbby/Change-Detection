import unittest
#You can run this script using the command line below:
#python3 -m unittest test.py

def check_ans(inputkey,ans): #this is the custom block that we want to test
    if (inputkey == 'm'):
        if (ans == 1): 
            return 1 
        else: 
            return 0 
    elif (inputkey == "c"): 
        if (ans == 1):
            return 0
        else: 
            return 1 
    else: 
        return "NA"

class Test(unittest.TestCase):
    #This test tests the case in which the participant presses "m"(identical) and that the stimuli are identical. Thd function check_ans should return 1(correct) in this case.
    def test_check_ans1(self):  
        self.assertEqual(check_ans("m",1),1)
    
    #This test tests the case in which the participant presses "m"(identical) and that the stimuli are different. Thd function check_ans should return 0(incorrect) in this case.
    def test_check_ans2(self):
        self.assertEqual(check_ans("m",0),0)
    
    #This test tests the case in which the participant presses "c"(different) and that the stimuli are identical. Thd function check_ans should return 0(incorrect) in this case.
    def test_check_ans3(self):
        self.assertEqual(check_ans("c",1),0)

    #This test tests the case in which the participant presses "c"(different) and that the stimuli are different. Thd function check_ans should return 1(correct) in this case.   
    def test_check_ans4(self):
        self.assertEqual(check_ans("c",0),1)
    
     #This test tests the case in which the participant presses neither "m" nor "c." The function check_ans should return "NA," because the meaning of the pressed key is unclear. 
    def test_check_ans5(self):
        self.assertEqual(check_ans("k",1),"NA")
    

if __name__ == "__main__":
    unittest.main()
    