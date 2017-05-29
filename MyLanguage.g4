grammar MyLanguage;		

commands	: command commands
			| EOF
			|
			;

command     : conditional
            | repeat
            | printexpr 
            | declaration
            | method
            ;

declaration : VAR ID 'as' expr SMCOLON
            | 'struct' ID ASSIGN 'new' STRUCTS SMCOLON
            ;

method      : ID '..' methods SMCOLON;

//1.Metodos que no contienen nada
//2.Metodos que reciben un parametro
methods     : var PIZQ PDER
            | vardos PIZQ expr PDER
            | METHOD PIZQ expr COLON expr PDER
            ;

var         : MTD | TAK ;
vardos      : MTH | REM ;

conditional : 'if' expr ROP expr 'then' commands postcond;
postcond    : ELSEIF expr ROP expr 'then' commands postcond
            | ELSE commands 'endif'
            | ENDIF
            ;
repeat		: 'repeat' expr 'times' commands 'endrepeat';
printexpr	: 'print' printwhat ;

printwhat   : expr SMCOLON | method;

expr:	expr MULOP expr
    |	expr SUMOP expr
    |	DOUBLE
    |	PIZQ expr PDER
    | 	ID
    ;



STRUCTS : 'stack' | 'queue' | 'list' ;
MTD     : 'len';
TAK     : 'take';
MTH     : 'put';
REM     : 'remove';
METHOD  : 'insert';

COMMENT 		: '/*' .*? '*/' -> skip ;
LINE_COMMENT 	: '//' ~[\r\n]* -> skip ;
WS		: [ \t\r\n]+ -> skip ;
ELSEIF  : 'elseif';
ELSE    : 'else';
ENDIF   : 'endif';
VAR		: 'var';
PIZQ	: '(' ;
PDER	: ')' ;
ASSIGN  : '=' ;
ROP		: ( '<' | '<=' | '>=' | '>' | '==' | '!=' ) ;
SMCOLON : ';' ;
COLON   : ',' ;
MULOP	: ( '*' | '/' );
SUMOP	: ('+' | '-') ;
DOUBLE	: [0-9]+( | [.][0-9]+);
ID 		: [a-zA-Z][a-zA-Z0-9_]* ;
