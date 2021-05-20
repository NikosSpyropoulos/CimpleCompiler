#include <stdio.h>

int main()
{
int a, b, c, T_0;
L_0: 
L_1: T_0 = a+1; // (+	a	1	T_0	)
L_2: c = T_0; // (:=	T_0	_	c	)
L_3: return c; // (retv	c	_	_	)
L_4: ;
L_5: 
L_6: a = 1; // (:=	1	_	a	)
L_7: L_8: b = f; // (:=	f	_	b	)
L_9: return 0; // (halt	_	_	_	)
L_10: ;
}