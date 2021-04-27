#include <stdio.h>

int main()
{
int x, T_0, T_1, T_2, T_3;
L_0: 
L_1: i = 1; // (:=	1	_	i	)
L_2: T_0 = 1; // (:=	1	_	T_0	)
L_3: if( i<=10 ) goto L_5; // (<=	i	10	5	)
L_4: goto L_9; // (jump	_	_	9	)
L_5: T_0 = 0; // (:=	0	_	T_0	)
L_6: T_1 = num*i; // (*	num	i	T_1	)
L_7: num = T_1; // (:=	T_1	_	num	)
L_8: printf("%s", "num "); // (out	num	_	_	)
L_9: if( i>=50 ) goto L_11; // (>=	i	50	11	)
L_10: goto L_14; // (jump	_	_	14	)
L_11: T_0 = 0; // (:=	0	_	T_0	)
L_12: T_2 = i+10; // (+	i	10	T_2	)
L_13: i = T_2; // (:=	T_2	_	i	)
L_14: if( i>=100 ) goto L_16; // (>=	i	100	16	)
L_15: goto L_19; // (jump	_	_	19	)
L_16: T_0 = 0; // (:=	0	_	T_0	)
L_17: T_3 = i-20; // (-	i	20	T_3	)
L_18: i = T_3; // (:=	T_3	_	i	)
L_19: if( T_0==0 ) goto L_2; // (=	T_0	0	2	)
L_20: ;
L_21: 
L_22: scanf( "%d", &x); // (inp	x	_	_	)
L_23: L_24: L_25: return 0; // (halt	_	_	_	)
L_26: ;
}