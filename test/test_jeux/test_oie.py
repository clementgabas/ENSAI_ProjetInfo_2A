import unittest
from jeuxservice.jeuxApp import oie

class Test_Player_oie(unittest.Testcase):
    def test_is_instance_of_Player(self):
        tester = oie.Player()
        self.assertIsInstance(tester, oie.Player())

    def test_set_waitingturn(self):
        tester = oie.Player()
        tester.set_waitingturn(2)
        self.assertIs(tester._nbwaitingturn, 2)

    def test_get_waitingturn(self):
        tester = oie.Player()
        try:
            tester.set_waitingturn(1)
        except:
            return "erreur dans la méthode set_waitingturn"
        self.assertIs(tester.get_waitingturn(), 1)

    def test_test_waiting(self):
        tester = oie.Player()
        try:
            tester.set_waitingturn(1)
        except:
            return "erreur dans la méthode set_waitingturn"
        self.assertTrue(tester.test_waiting())
        try:
            tester.set_waitingturn(3)
        except:
            return "erreur dans la méthode set_waitingturn"
        self.assertFalse(tester.test_waiting())

    def test_freeze_waiting(self):
        tester = oie.Player()
        tester.freeze_waiting()
        self.assertIsEqual(tester._nbwaitingturn, -1)

    def test_set_actualbox(self):
        tester = oie.Player()
        tester.set_actualbox(10)
        self.assertIsEqual(tester._actualbox, 10)

    def test_get_actual_box(self):
        tester = oie.Player()
        try:
            tester.set_actualbox(10)
        except:
            return "erreur dans la méthode set_actualbox"
        self.assertIsEqual(tester.get_actualbox(), 10)

    def test_add_dice(self):
        tester = oie.Player()
        try:
            tester.set_actualbox(10)
        except:
            return "erreur dans la méthode set_actualbox"
        tester.add_dice(2)
        self.assertIsEqual(tester._actualbox, 12)





if __name__ == "__main__":
        unittest.main()