#include <stdio.h>

int main()
{
int x, a, T_0, T_1, T_2, T_3;
L_0: 
L_1: x = 0; // (:=	0	_	x	)
L_2: a = 20; // (:=	20	_	a	)
L_3: if( x<300 ) goto L_5; // (<	x	300	5	)
L_4: goto L_15; // (jump	_	_	15	)
L_5: T_0 = a+x; // (+	a	x	T_0	)
L_6: x = T_0; // (:=	T_0	_	x	)
L_7: if( x<50 ) goto L_9; // (<	x	50	9	)
L_8: goto L_12; // (jump	_	_	12	)
L_9: T_1 = x+10; // (+	x	10	T_1	)
L_10: x = T_1; // (:=	T_1	_	x	)
L_11: goto L_14; // (jump	_	_	14	)
L_12: T_2 = a*2; // (*	a	2	T_2	)
L_13: a = T_2; // (:=	T_2	_	a	)
L_14: goto L_3; // (jump	_	_	3	)
L_15: T_3 = x-30; // (-	x	30	T_3	)
L_16: x = T_3; // (:=	T_3	_	x	)
L_17: printf( "%d", x ); // (out	x	_	_	)
L_18: return 0; // (halt	_	_	_	)
L_19: ;
}