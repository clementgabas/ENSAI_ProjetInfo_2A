import unittest
from jeuxservice.jeuxApp import p4

class Test_Player_p4(unittest.Testcase):
    def test_is_instance_of_Player(self):
        tester = p4.Player()
        self.assertIsInstance(tester, p4.Player())

    def test_Set_Param(self):
        tester = p4.Player()
        tester.Set_Param("j1", "Jaune")
        self.assertIs(tester._color, "Jaune")
        self.assertIs(tester._name, "j1")

    def test_Get_Token(self):
        tester = p4.Player()
        self.assertIs(tester.Get_Token(), 0)

        tester.Set_Param("j1","Jaune")
        self.assertIs(tester.Get_Token(), 1)

        tester.Set_Param("j1","Rouge")
        self.assertIs(tester.Get_Token(), 2)

if __name__ == "__main__":
        unittest.main()