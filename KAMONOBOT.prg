1 Open "COM1:" As #1
2 *MAIN
3 Mov P_Safe
4 *LOOPTESTE
5 Input #1, M0
6 If M0 = 0 Then *LOOPTESTE
7 Mov P1, -50
8 Mvs P1
9 Dly 1
10 Mvs P1, -50
11 Mov P2, -50
12 Mvs P2
13 Dly 1
14 Mvs P2, -50
15 Print #1, "FEITO"
16 Mov P_Safe
17 GoTo *MAIN
18 End
P1=(+49.75,+145.16,+37.19,+180.00,+0.00,+180.00)(7,0)
P2=(+49.75,-114.49,+37.19,+180.00,+0.00,+180.00)(7,0)
