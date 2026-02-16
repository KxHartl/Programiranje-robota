/PROG  MOVE_ZADATAK_01
/ATTR
OWNER		= MNEDITOR;
COMMENT		= "Z1-Paletizacija";
PROG_SIZE	= 450;
CREATE		= DATE 26-02-12  TIME 12:00:00;
MODIFIED	= DATE 26-02-12  TIME 12:00:00;
FILE_NAME	= ;
VERSION		= 0;
LINE_COUNT	= 10;
MEMORY_SIZE	= 850;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/APPL
/MN
   1:  !Postavljanje koordinatnog sustava ;
   2:  UFRAME_NUM=R[3:UFRAME] ;
   3:  UTOOL_NUM=1 ;
   4:  !HOME pozicija ;
   5:  !Pomak na odabrano paletno mjesto ;
   6:  !R[2] sadrzi ID PR registra ;
   7:  !R[1] sadrzi brzinu u % ;
  8:J PR[R[2:PosID]] R[1:Speed]% FINE    ;
  9:  WAIT 2.00(sec) ;
  10:J PR[1:HOME] R[1:Speed]% FINE    ;
  11:  !Kraj programa ;
/POS
/END
