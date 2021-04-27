int main()
{
int x, y, T_0, T_1, T_2, T_3;
L_0: 
L_1: scanf( '%d', x) // (inp	x	_	_	)
L_2: if( y<=0 ) goto L_4 // (<=	y	0	4	)
L_3: goto L_8 // (jump	_	_	8	)
L_4: return y // (retv	y	_	_	)
L_5: T_0 = x*2 // (*	x	2	T_0	)
L_6: y = T_0 // (:=	T_0	_	y	)
L_7: goto L_17 // (jump	_	_	17	)
L_8: if( x>0 ) goto L_10 // (>	x	0	10	)
L_9: goto L_15 // (jump	_	_	15	)
L_10: T_1 = y*3 // (*	y	3	T_1	)
L_11: printf( '%d', T_1 ) // (out	T_1	_	_	)
L_12: T_2 = x*2 // (*	x	2	T_2	)
L_13: y = T_2 // (:=	T_2	_	y	)
L_14: goto L_17 // (jump	_	_	17	)
L_15: T_3 = x*2 // (*	x	2	T_3	)
L_16: return T_3 // (retv	T_3	_	_	)
L_17: return x // (retv	x	_	_	)
L_18: return 0 // (halt	_	_	_	)
L_19: 
}